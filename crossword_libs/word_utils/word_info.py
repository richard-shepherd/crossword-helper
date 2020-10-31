class WordInfo(object):
    """
    Information associated with a word.
    """

    def __init__(self):
        """
        Constructor.
        """

        # The collection of part-of-speech tags for the word...
        self.pos_tags = set()
        