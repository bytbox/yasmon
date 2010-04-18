"""Provides an interface to the local machine.

"""

from system import *;

def get_local():
    """Returns an object representing the local system.
    """
    system=LocalSystem()

    #create the processors
    cpuinfo=file("/proc/cpuinfo")
    for line in cpuinfo:
        pass 
    cpuinfo.close()

    #create the memory bank
    system.set_memory(LocalMemory())

    #create the drives
    partitions=file("/proc/partitions")
    for line in partitions:
        pass
    partitions.close()

    #create the process list
    system.set_processlist(ProcessList())
    return system

class LocalSystem(System):
    """Represents a local system.

    """
    def __init__(self):
        """Creates an empty local system.

        This constructor does not initialize the local system - that
        is done with the get_local() method.
        """
        System.__init__(self)


class LocalProcessor(Processor):
    """Represents a local processor
    """
    def __init__(self,id,name):
        """Creates a local processor.

        Ordinarily, the name will be the same as cpu<id>.
        """
        Processor.__init__(self)


class LocalMemory(Memory):
    """Represents a local memory (RAM) bank
    """
    def __init__(self,filename="/proc/meminfo"):
        """Creates a memory bank from the file.

        By default, the file /proc/meminfo is used.
        """
        self.filename=filename


class LocalDrive(Drive):
    """Represents a local drive
    """
    pass


class LocalProcessList(ProcessList):
    """Represents a local list of processes

    Since this class always draws its information from the /proc
    directory, all created on the same system will be identical.
    """
    pass


class LocalProcess(Process):
    """Represents a single local process
    """
    pass
