import logging
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
from collections import defaultdict
from singleton_decorator import singleton
from ..utils import Utils
from .lemma_info import LemmaInfo
from .word_info import WordInfo
from .word_utils import WordUtils

@singleton
class WordManager(object):
    """
    Manages the collection of available words.

    Loads words from a number of sources, including:
    - The Brown tagged-words corpus
    - A file of English words

    Helps find the part of speech (pos) for a word, and creates pos forms of words
    from the lemma (root form) and a pos indicator.
    """

    def __init__(self):
        """
        Constructor.
        """
        # Collection of WordInfo, keyed by the word itself...
        self.word_infos = defaultdict(WordInfo)

        # Collection of LemmaInfo, keyed by the lemma string. Lets you look up pos
        # word forms for the lemma...
        self.lemma_infos = defaultdict(LemmaInfo)

        # Converts words to their lemmas...
        self._lemmatizer = WordNetLemmatizer()

        # Loads all words, and finds their pos mappings...
        self._load_all_words()
    
    def get_words(self, length=None):
        """
        Returns all words of the length requested. Or all words if the length is not specified.
        """
        if length is None:
            return self.word_infos.keys()
        else:
            return (word for word in self.word_infos if len(word) == length)

    def get_pos_tags(self, word):
        """
        Returns the collection of pos-tags for the word.
        """
        return self.word_infos[word].pos_tags

    def get_part_of_speech(self, lemma, pos_tag):
        """
        Returns a word corresponding to the lemma and pos-tag specified.
        If we cannot find a word for the pos-tag, we return the lemma itself.
        """

        # We check if we have info for this lemma...
        if lemma not in self.lemma_infos:
            return lemma  # We do not have info for the lemma, so we just return it

        # We have info for this lemma - so we check if we have a form for the 
        # pos-tag requested...
        lemma_info  = self.lemma_infos[lemma]
        if pos_tag not in lemma_info.word_forms:
            return lemma  # We do not have a word-form for the requested pos-tag, so we return the lemma

        # We have a word-form for the lemma and pos-tag requested...
        return self.lemma_infos[lemma].word_forms[pos_tag]

    def _load_all_words(self):
        """
        Loads a collection of all English words and creates maps:
        - word -> part-of-speech indicators 
        - lemma -> (part-of-speech-indicator -> word)
        """
        self._load_words_from_corpus(nltk.corpus.brown)
        self._load_words_from_corpus(nltk.corpus.treebank)
        self._load_words_from_file()
        self._map_lemmas_to_words()

    def _load_words_from_corpus(self, corpus):
        """
        Loads words from a tagged corpus.
        """
        logging.info("Loading words from corpus: {0}".format(str(corpus.root)))
        for (word, pos_tag) in corpus.tagged_words():
            # We clean up the word, removing punctuation, whitespace etc...
            clean_word = WordUtils.clean_word(word)
            if clean_word == "": continue
            
            # We add the word and its tag to the map of word -> pos-tags...
            word_info = self.word_infos[clean_word]
            word_info.pos_tags.add(pos_tag)

    def _load_words_from_file(self):
        """
        Loads words from a file and attempts to infer pos info for them.
        """
        # We read all lines from the file, removing whitespace...
        filename = "words_alpha.txt"
        logging.info("Loading words from {0}".format(filename))
        path = Utils.path_relative_to_module(__file__, filename)
        with open(path, "r") as file:
            words = sorted([x.strip() for x in file.readlines()])

        # We add these words to our collection, if we do not already have them...
        active_first_letter = ""
        for word in words:
            clean_word = WordUtils.clean_word(word)
            if clean_word in self.word_infos: continue  # We already have this word from a different source

            # We log when as we process each letter...
            first_letter = clean_word[0]
            if first_letter != active_first_letter:
                active_first_letter = first_letter
                logging.info(".. loading words starting with '{0}'".format(first_letter))

            # We find the pos tags for the word, and store the WordInfo for this word...
            pos_tags = self._infer_pos_tags(clean_word)
            self.word_infos[clean_word].pos_tags = set(pos_tags)

    def _infer_pos_tags(self, word):
        """
        Returns a collection of pos tags for the word passed in.
        """
        results = set()

        # For the moment we just return the main tag provided by nltk. We may later try to do this
        # better, eg by trying the word in various sentences...
        pos_tags = nltk.pos_tag([word])
        pos_tag = pos_tags[0][1]
        results.add(pos_tag)

        return results

    def _map_lemmas_to_words(self):
        """
        Finds the lemma for each (word, pos-tag) we have found and maps the 
        lemma to it.
        """
        logging.info("Mapping lemmas to (word, pos-tag).")
        for (word, word_info) in self.word_infos.items():
            for pos_tag in word_info.pos_tags:
                wordnet_pos = self._get_wordnet_pos(pos_tag)
                if wordnet_pos is not None:
                    lemma = self._lemmatizer.lemmatize(word, pos=wordnet_pos)
                    self.lemma_infos[lemma].word_forms[pos_tag] = word

    def _get_wordnet_pos(self, pos_tag):
        """
        Returns a wordnet pos type from the pos-tag passed in.
        We use the wordnet pos types when finding the lemma of a word.
        """
        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

