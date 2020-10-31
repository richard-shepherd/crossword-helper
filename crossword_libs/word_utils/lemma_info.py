from collections import defaultdict


class LemmaInfo(object):
    """
    Holds info related to a lemma - ie, to the root form of a word.

    In particular we hold a map of pos-tags to the word form for them.
    For example, the LemmaInfo for "good" will include:
      JJR -> "better"
      JJT -> "best"
    """
    
    def __init__(self):
        """
        Constructor.
        """
        # Collection of word forms keyed by pos-tag, eg RBT -> "best"...
        self.word_forms = dict()
