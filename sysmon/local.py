"""Provides an interface to the local machine.

"""

from system import *;

def get_local():
    """Returns an object representing the local system.
    """
    pass

class LocalSystem(System):
    """Represents a local system.

    """
    def __init__(self):
        System.__init__(self)

class LocalProcessor(Processor):
    """Represents a local processor
    """
    pass
