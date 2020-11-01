import logging
from singleton_decorator import singleton
from collections import defaultdict
from ..word_utils import WordUtils
from ..utils import Utils


@singleton
class BitsAndPieces(object):
    """
    Manages a collection of 'bits and pieces' - ie, substitutions of
    words or phrases for collections of letters. For example:
      lincoln -> abe
      actor   -> ham
    """

    def __init__(self):
        """
        Constructor.
        """
        # A map of phrase -> [abbreviations]...
        self.abbreviations = self._load_from_file()

    def bits_and_pieces_from_clue(self, clue, require_whole_word_if_length_less_than=4):
        """
        Returns a list of bits and pieces for the clue provided. Each item in 
        the list is tuple of (phrase, [abbreviations]). For example:
          ("sailor", ["tar", "jack"])
        """
        results = []

        # We make sure the clue has punctuation removed (and is lower case)...
        clue = WordUtils.remove_punctuation(clue)
        words_in_clue = clue.split()

        # We check each phrase we manage to see if it is in the clue...
        for (phrase, abbreviations) in self.abbreviations.items():

            # We check differently depending on the length of the phrase.
            if len(phrase) < require_whole_word_if_length_less_than:
                # The phrase is short, so we check if it exists as a whole word in the clue...
                if phrase in words_in_clue:
                    results.append((phrase, abbreviations))
            else:
                # The phrase is long, so we check if it is anywhere in the clue...
                if phrase in clue:
                    results.append((phrase, abbreviations))

        return results

    def _load_from_file(self):
        """
        Returns a map of phrase -> letters loaded from the bits_and_pieces.txt file.
        """
        results = defaultdict(list)

        # We load the file...
        filename = "bits_and_pieces.txt"
        path = Utils.path_relative_to_module(__file__, filename)
        logging.info("Loading bits-and-pieces from " + path)
        with open(path, "r") as file:
            lines = file.readlines()

        # Each line looks like:
        #   he: His Excellency
        #
        # We want to provide the mapping the other way around, ie from the word or phrase
        # which we might find in a clue to the letters. Note that the same word can map
        # to multiple letters, for example:
        #   sailor -> ab
        #   sailor -> tar
        # So words map to a list of abbreviations.
        for line in lines:
            tokens = line.split(":")
            if len(tokens) != 2: continue
            abbreviation = tokens[0].strip().lower()
            phrase = tokens[1].strip().lower()
            results[phrase].append(abbreviation)

        return results
