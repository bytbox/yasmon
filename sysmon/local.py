"""Provides an interface to the local machine.

"""

import re;

from system import *;

def get_local():
    """Returns an object representing the local system.
    """
    system=LocalSystem()

    #create the processors
    cpuinfo=file("/proc/cpuinfo")
    for line in cpuinfo:
        match=re.match("^processor[^:]*:[ \t]*([0-9]+)",line)
        if match:
            system.add_processor(LocalProcessor(match.group(1),"cpu"+match.group(1)))
    cpuinfo.close()

    #create the memory bank
    system.set_memory(LocalMemory())

    #create the filesystems
    partitions=file("/proc/partitions")
    for line in partitions:
        match=re.match("^[ \t]+([0-9]+)[ \t]+([0-9]+)[ \t]+",line)
        if match:
            major=match.group(1)
            minor=match.group(2)
            system.add_filesystem(LocalFilesystem(major,minor))
    partitions.close()

    #create the process list
    system.set_processlist(LocalProcessList())
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
        self._name=name
        self._id=id

    def name(self):
        return self._name

    def do_update(self):
        with open("/proc/cpuinfo") as cpuinfo:
            for line in cpuinfo:
                pass
        self.callback().call("local.processor.updated",self.name())


class LocalMemory(Memory):
    """Represents a local memory (RAM) bank
    """
    def __init__(self,filename="/proc/meminfo"):
        """Creates a memory bank from the file.

        By default, the file /proc/meminfo is used.
        """
        Memory.__init__(self)
        self.filename=filename
        self._dict=dict()

    def do_update(self):
        with open(self.filename) as meminfo:
            for line in meminfo:
                match=re.search("([^:]+)[ \t]*:[ \t]*(.+)$",line)
                if match:
                    key=match.group(1)
                    val=match.group(2)
                    match=re.search("([0-9]+)[ \t]*kB",val)
                    if match:
                        val=int(match.group(1))*1024
                    match=re.search("([0-9]+)[ \t]*MB",str(val))
                    if match:
                        val=int(match.group(1))*1024*1024
                    self._dict[key]=val
        self.callback().call("local.memory.updated",None)

    def dict(self):
        return self._dict

    def total_memory(self):
        return self.dict()['MemTotal'];

    def free_memory(self):
        return self.dict()['MemFree'];

    def active_memory(self):
        return self.dict()['Active'];

    def inactive_memory(self):
        return self.dict()['Inactive'];

    def total_swap(self):
        return self.dict()['SwapTotal'];

    def free_swap(self):
        return self.dict()['SwapFree'];


class LocalFilesystem(Filesystem):
    """Represents a local filesystem.
    """
    def __init__(self,major,minor):
        """Creates the filesystem from the major and minor
        identifiers.
        """
        Filesystem.__init__(self)

    def do_update(self):
        self.callback().call("local.filesystem.updated",None)


class LocalProcessList(ProcessList):
    """Represents a local list of processes.

    Since this class always draws its information from the /proc
    directory, all created on the same system will be identical.
    """
    def __init__(self):
        ProcessList.__init__(self)

    def do_update(self):
        self.callback().call("local.processlist.updated",None)


class LocalProcess(Process):
    """Represents a single local process.
    """
    pass
