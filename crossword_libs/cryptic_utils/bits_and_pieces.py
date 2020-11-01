from singleton_decorator import singleton
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
        pass

    def _load_from_file(self):
        """
        Returns a map of phrase -> letters loaded from the bits_and_pieces.txt file.
        """

        # We load the file...
        filename = "bits_and_pieces.txt"
        path = Utils.path_relative_to_module(__file__, filename)
        