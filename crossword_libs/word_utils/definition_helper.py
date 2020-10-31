from nltk.corpus import wordnet
from .word_utils import WordUtils


class DefinitionHelper(object):
    """
    Finds words which match a crossword definition. For example:
      "rodents" -> "rats", "mice"
    """

    @staticmethod
    def words_for_definition(definition):
        """
        Finds a collection of words from a hint. For example:
          "rodents" -> "rats", "mice" etc
        """
        synsets = set()

        # We look up synsets for the word. These are words / concepts with the same meaning...
        for synset in wordnet.synsets(definition):
            # For each synset, we look up similar words...
            synsets = synsets.union(DefinitionHelper._find_similar_synsets(synset, 3))

        # We find hyponyms for each synset we've found...
        hyponyms = set()
        for synset in synsets:
            hyponyms = hyponyms.union(DefinitionHelper._get_hyponyms_from_synset(synset))
        synsets = synsets.union(hyponyms)

        # We find all the words from the synsets we've found...
        words = set()
        for synset in synsets:
            words_in_synset = DefinitionHelper._words_from_synset(synset)
            for word_in_synset in words_in_synset:

                # We clean the word, for example, to remove underscores...
                clean_word = WordUtils.clean_word(word_in_synset)

                # We return the word (if we have not already returned it previously)...
                if clean_word in words: continue
                words.add(clean_word)
                yield clean_word

    @staticmethod
    def _find_similar_synsets(synset, similar_to_recursion_level=0):
        """
        Returns a collection of synsets including the original synset provided as
        well as other synsets which are similar to it. The similarity can be done
        recursively on these synsets to the recursion level specified.
        """

        # We add the synset provided to the results...
        results = set()
        results.add(synset)

        if similar_to_recursion_level == 0:
            return results

        # We want to find similar synsets...
        for similar_to in synset.similar_tos():
            results = results.union(DefinitionHelper._find_similar_synsets(similar_to, similar_to_recursion_level-1))

        return results

    @staticmethod
    def _words_from_synset(synset):
        """
        Returns the list of words (lemma-names) from the synset passed in.
        """
        words = set()

        # We add the words from the synset...
        for lemma_name in synset.lemma_names():
            words.add(lemma_name)

        return words

    @staticmethod
    def _get_hyponyms_from_synset(synset):
        """
        Returns the collection of all hyponyms for the synset passed in.
        A hyponym is a specific example of the synset, eg "oak" is a hyponym of "tree".
        """
        hyponyms = set()

        # We add all hyponyms (recursively) to the collection of results...
        for hyponym in synset.hyponyms():
            hyponyms.add(hyponym)
            hyponyms = hyponyms.union(DefinitionHelper._get_hyponyms_from_synset(hyponym))

        return hyponyms

