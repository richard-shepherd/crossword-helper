import sys
import os
import logging


class Utils(object):
    """
    Utility functions.
    """

    @staticmethod
    def log_to_stdout(level=logging.INFO):
        """
        Sets up logging to stdout at the (optional) level specified.
        """
        root = logging.getLogger()
        root.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)

    @staticmethod
    def path_relative_to_module(module_file_path, filename):
        """
        Returns a path for filename in the same folder as the module_file_path.
        When calling this, you will usually pass __file__ as the module_file_path parameter.
        """
        return os.path.join(os.path.dirname(module_file_path), filename)