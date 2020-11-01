from .bits_and_pieces import BitsAndPieces


class Clue(object):
    """
    Parses cryptic clues and provides information on how to solve them.
    """

    def __init__(self, clue):
        """
        Constructor.
        """
        # The original text of the clue...
        self.clue = clue

    @staticmethod
    def parse(clue):
        """
        Parses the clue and returns a Clue object.
        """
        # We show bits-and-pieces for the clue...
        bits_and_pieces = BitsAndPieces().bits_and_pieces_from_clue(clue)
        for (phrase, abbreviations) in bits_and_pieces:
            phrase = phrase.upper()
            abbreviations = [x.upper() for x in abbreviations]
            print("{0} -> {1}".format(phrase, abbreviations))