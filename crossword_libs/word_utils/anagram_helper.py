import itertools
from singleton_decorator import singleton
from collections import defaultdict
from .word_manager import WordManager
from .word_utils import WordUtils


@singleton
class AnagramHelper(object):
    """
    Finds anagrams for words.
    """
    
    def __init__(self):
        """
        Constructor.
        """
        # We create a mapping of anagram-key -> [words-which-are-anagrams-of-each-other]...
        self._character_prime_map = self._create_character_prime_map()
        self._anagram_lookup = self._create_anagram_lookup()

    def anagrams(self, word, word_lengths=None):
        """
        Returns anagrams of the word passed in.

        You can request that the result is split into words with lengths specified
        in the optional word_lengths parameter. For example:
          anagrams("astronomer", [4, 6]) -> ["moon", "starer"]
        """

        # If no word-length was specified, we specify that we want anagrams for the full
        # length of the word...
        if word_lengths is None:
            word_lengths = [len(word)]

        # We find the combinations of the ways the word can be split up
        # by the sizes requested...
        splits = WordUtils.letter_combinations(word, word_lengths)

        # We loop through the splits, finding ones where every word in the split 
        # is a valid anagram...
        for split in splits:
            # Each split is an array of the 'words' that make up the split.
            # We check whether all these words have anagrams...
            all_words_have_anagrams = True
            anagrams_for_words = []  # List of anagrams for each word in the split
            for word in split:
                anagram_key = self._get_anagram_key(word)
                anagrams_for_word = self._anagram_lookup.get(anagram_key, None)
                if anagrams_for_word is None:
                    # There are no anagrams for this word...
                    all_words_have_anagrams = False
                    break

                # There are anagrams for the word, so we record them...
                anagrams_for_words.append(anagrams_for_word)

            # If we found anagrams, we return them...
            if all_words_have_anagrams:
                # We first find all combinations (the cross-product) of the words we found...
                products = itertools.product(*anagrams_for_words)
                for product in products:
                    yield product

    def _create_character_prime_map(self):
        """
        Returns a dictionary of character -> prime-number for use with
        anagram key generation.
        """
        return dict( \
            a=2, e=3, i=5, o=7, u=11, \
            t=13, s=17, h=19, c=23, d=29, \
            k=31, l=37, m=41, n=43, j=47, \
            p=53, q=59, r=61, g=67, f=71, \
            b=73, v=79, w=83, x=89, y=97, z=101)

    def _get_anagram_key(self, word):
        """
        Returns an anagram key for the word specified.
        """
        key = 1
        for c in word:
            character_prime = self._character_prime_map[c]
            if character_prime is not None:
                key = key * character_prime
        return key

    def _create_anagram_lookup(self):
        """
        Creates a dictionary of anagram-key -> [words].

        The key is made by mapping each letter to a prime number and multiplying
        these values for each letter in a word. This means that the key for each 
        word is unique for the letters in the word - but not by their order. So
        anagrams share the same key.
        """
        anagram_lookup = defaultdict(list)

        # We map each word we have to its anagram key...
        for word in WordManager().get_words():
            # We find the anagram key for the word, and add it to the list of 
            # words for this key...
            anagram_key = self._get_anagram_key(word)
            anagram_lookup[anagram_key].append(word)

        return anagram_lookup

