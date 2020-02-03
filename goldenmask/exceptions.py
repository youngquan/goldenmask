"""
goldenmask.exceptions
~~~~~~~~~~~~~~~~~~~~~
This module contains the set of Goldenmask's exceptions.
"""


class UnsupportedLayerException(Exception):
    """This layer is not supported now!"""


class NoPythonFiles(Exception):
    """There is no python files to build"""
