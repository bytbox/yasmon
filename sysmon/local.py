#########################################################################
# YASMon - Yet Another System Monitor                                   #
# Copyright (C) 2010  Scott Lawrence                                    #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

"""Provides an interface to the local machine.

"""

import re;

from system import *;

def get_local():
    """Returns an object representing the local system.
    """
    system=LocalSystem("localhost")
    uptime=LocalUptime()

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
        match=re.match("^[ \t]+([0-9]+)[ \t]+([0-9]+)[ \t]+([0-9]+)[ \t]+([a-z0-9]+)",line)
        if match:
            major=match.group(1)
            minor=match.group(2)
            blocks=match.group(3)
            name=match.group(4)
            system.add_filesystem(LocalFilesystem(name))
    partitions.close()

    #create the process list
    system.set_processlist(LocalProcessList())
    system.set_uptime(uptime)

    #create meta data
    system.create_meta()
    return system

def read_file(filename):
    content=""
    with open(filename) as file:
        for line in file:
            content="%s%s" % (content,line)
    return content

class LocalSystem(System):
    """Represents a local system.

    """
    def __init__(self,name="localhost"):
        """Creates an empty local system.

        This constructor does not initialize the local system - that
        is done with the get_local() method.
        """
        System.__init__(self,name)

    def create_meta(self):
        """Creates the meta information.

        Ordinarily, this method is called only once, since the
        meta-information should never change (except perhaps on
        reboot).
        """
        #clear the dictionary
        self._meta={}
        meta=self._meta
        meta['name']=('System name',self.name())
        meta['cmdline']=('Command line with which kernel was booted',
                         read_file("/proc/cmdline"))
        meta['version']=('The version of the kernel being run',
                         read_file("/proc/version"))
        meta['issue']=('The issue (or distribution) being run',
                       re.sub("\\\\[nl]",'',read_file("/etc/issue")))


class LocalUptime(Uptime):
    """Represents the local uptime.
    """
    def __init__(self):
        Uptime.__init__(self)
        self._uptime=0

    def uptime(self):
        return self._uptime

    def do_update(self):
        with open("/proc/uptime") as uptime:
            for line in uptime:
                self._uptime=float(re.split(" ",line)[0])                
        self.callback().call("uptime.updated",self)

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
        self._dict=dict()

        #history-keeping for calculation (math: a crude hack that works)
        self._totalusage=0
        self._totalidle=0

    def name(self):
        return self._name

    def dict(self):
        return self._dict

    def do_update(self):
        ignoring=True
        #learn about our cpus
        with open("/proc/cpuinfo") as cpuinfo:
            for line in cpuinfo:
                match=re.match("processor[ \t]*:[ \t]*([0-9]+)",line)
                if match:
                    #should we ignore stuff, or pay attention?
                    if match.group(1)==str(self._id):
                        ignoring=False
                    else:
                        ignoring=True
                if not ignoring:
                    match=re.search("([^:\t]+)[ \t]*:[ \t]*(.+)$",line)
                    if match:
                        key=match.group(1)
                        val=match.group(2)
                        self._dict[key]=val

        #now look up our cpu's statistics
        with open("/proc/stat") as stat:
            for line in stat:
                match=re.match("%s[ \\t]+([0-9]+)[ \\t]+([0-9]+)[ \\t]+([0-9]+)[ \\t]+([0-9]+)[ \\t]+"
                         % self._name,line)
                if match:
                    usage=int(match.group(1))+int(match.group(2))+int(match.group(3))
                    idle=int(match.group(4))
                    #update our current statistics
                    newusage=usage-self._totalusage
                    newidle=idle-self._totalidle
                    if (newusage+newidle)>0:
                        pu=newusage/float(newusage+newidle)
                    else:
                        pu=0
                    #will this cause a problem with variable frequency cpus?
                    self.dict()['usage']=pu*self.max_freq()
                    self._totalusage=usage
                    self._totalidle=idle
        self.callback().call("processor.%s.updated" % self.name(),self)


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
        self.callback().call("memory.updated",self)

    def dict(self):
        return self._dict


class LocalFilesystem(Filesystem):
    """Represents a local filesystem.
    """
    def __init__(self,device):
        """Creates the filesystem from the device name.
        """
        Filesystem.__init__(self)

    def do_update(self):
        self.callback().call("filesystem.updated",self)


class LocalDrive(Drive):
    """Represents a local drive.
    """
    def __init__(self,major,minor):
        """Creates the drive from the major and minor
        identifiers.
        """
        Drive.__init__(self)

    def do_update(self):
        self.callback().call("drive.updated",self)


class LocalProcessList(ProcessList):
    """Represents a local list of processes.

    Since this class always draws its information from the /proc
    directory, all instances created on the same system will be
    identical.
    """
    def __init__(self):
        ProcessList.__init__(self)

    def do_update(self):
        self.callback().call("processlist.updated",self)


class LocalProcess(Process):
    """Represents a single local process.
    """
    pass
