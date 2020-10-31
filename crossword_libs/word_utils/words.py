import re
from .anagram_helper import AnagramHelper
from .definition_helper import DefinitionHelper
from .word_manager import WordManager


class Words(object):
    """
    Provides a fluent interface for looking up words given certain constraints.

    Examples:
    - Words().match("...)
    """
    
    def __init__(self):
        """
        Constructor.
        """
        
        # We default the collection of words we hold to the collection of all
        # words known by the WordManager.
        # Note: This object must be iterable.
        self.words = WordManager().get_words()

    def __iter__(self):
        """
        Allows the words held by these objects to be iterated.
        """
        return self.words

    def print(self):
        """
        Prints the collection of words we hold.
        """
        for word in self.words:
            print(word)

    def match(self, pattern):
        """
        Finds words which match the regex pattern supplied.
        """
        result = Words()
        result.words = self._internal_match(pattern)
        return result

    def anagrams(self, word, word_lengths=None):
        """
        Returns anagrams of the word passed in.

        You can request that the result is split into words with lengths specified
        in the optional word_lengths parameter. For example:
          anagrams("astronomer", [4, 6]) -> ["moon", "starer"]
        """
        result = Words()

        # We find anagrams...
        anagrams = AnagramHelper().anagrams(word, word_lengths)

        # The anagrams are returned as a collection of tuples. We convert these
        # to an iterable of single strings...
        result.words = ("".join(anagram) for anagram in anagrams)

        return result

    def definition(self, definition):
        """
        Returns words associated with the definition supplied.
        """
        result = Words()
        result.words = DefinitionHelper.words_for_definition(definition)
        return result

    def length(self, length):
        """
        Returns words filtered to the length specified.
        """
        result = Words()
        result.words = (word for word in self.words if len(word) == length)
        return result

    def _internal_match(self, pattern):
        compiled_re = re.compile(pattern)
        for word in self.words:
            if compiled_re.fullmatch(word) is not None:
                yield word


