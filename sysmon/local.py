"""Provides an interface to the local machine.

"""

from system import *;

def get_local():
    """Returns an object representing the local system.
    """
    system=LocalSystem()

class LocalSystem(System):
    """Represents a local system.

    """
    def __init__(self):
        System.__init__(self)


class LocalProcessor(Processor):
    """Represents a local processor
    """
    pass


class LocalMemory(Memory):
    """Represents a local memory (RAM) bank
    """
    pass


class LocalDrive(Drive):
    """Represents a local drive
    """
    pass


class LocalProcessList(ProcessList):
    """Represents a local list of processes
    """
    pass


class LocalProcess(Process):
    """Represents a single local process
    """
    pass
