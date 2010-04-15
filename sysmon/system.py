"""Provides an interface to an abstract system

"""

class System():
    """Represents an abstract system.

    """
    
    def __init__(self):
        self.processors=[]
        self.memory=Memory.null()
        self.drives=[]

    def add_processor(self,processor):
        """Adds a processor to the system.
        """
        self.processors+=[processor]

    def processors(self):
        """Returns a list of processors in the system.
        """
        return self.processors

    def set_memory(self,memory):
        """Sets the system's memory bank.
        """
        self.memory=memory

    def memory(self):
        """Returns the system's memory bank
        """
        return self.memory

    def add_drive(self,drive):
        """adds a drive to the system
        """
        self.drives+=[drive]

    def drives(self):
        """Returns a list of all drives in the system.
        """
        return self.drives

    def set_processlist(self,processlist):
        """Sets the object representing the process list.
        """
        pass

    def processlist(self):
        """Returns the object representing the process list.
        """
        pass


class SystemPart():
    """Represents a part of a system
    """
    def null():
        """Returns a null part to be used when no real part is
        available.
        """
        return None


class Processor(SystemPart):
    """Represents a single abstract processor.
    """
    def null():
        return None


class Memory(SystemPart):
    """Represents a memory (RAM) bank.
    """
    def null():
        return None


class Drive(SystemPart):
    """Represents a drive.
    """
    def null():
        return None

class ProcessList(SystemPart):
    """Represents a list of processes.
    """
    def null():
        return None

class Process:
    pass
