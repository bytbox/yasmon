"""Provides an interface to the null machine.

"""

from system import *;

def get_null():
    """Returns an object representing the null system.
    """
    system=NullSystem()

class NullSystem(System):
    """Represents a null system.

    """
    def __init__(self):
        System.__init__(self)


class NullProcessor(Processor):
    """Represents a null processor
    """
    pass


class NullMemory(Memory):
    """Represents a null memory (RAM) bank
    """
    pass


class NullDrive(Drive):
    """Represents a null drive
    """
    pass


class NullProcessList(ProcessList):
    """Represents a null list of processes
    """
    pass


class NullProcess(Process):
    """Represents a single null process
    """
    pass
