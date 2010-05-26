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

"""Provides an interface to an abstract system

"""

from threading import Lock,Timer
import re
import callback
from error import *

class System():
    """Represents an abstract system and implements some basic logic.

    """
    
    def __init__(self,name="no-name"):
        self.lock=Lock()
        self._uptime=Uptime.null()
        self._processors=[]
        self._memory=Memory.null()
        self._filesystems=[] #filesystems (to measure space usage)
        self._drives=[] #drives (to measure i/o usage)
        self._netconns=[] #network connections
        self._processlist=ProcessList.null()
        self._delay=5 #the update interval in seconds
        self._callback=callback.SysmonCallback()
        self._timers=[]
        self._name=name

    def name(self):
        """Returns the identifying name of the system.
        """
        return self._name

    def run(self):
        """Runs the system monitor.

        All parts are updated immediately, and then again at the
        interval specified in the parts' configuration.
        """
        for part in self.parts():
            part.update()

    def stop(self):
        """Stops the system monitor.

        The monitor may safely be stopped and run and indefinite
        number of times.
        """
        for part in self.parts():
            part.timer.cancel()

    def acquire(self):
        """Acquire the lock object hidden in this system,
        """
        self.lock.acquire()

    def release(self):
        """Release the lock object hidden in this system.
        """
        self.lock.release()

    def update(self):
        """Performs an update of the system.

        These updates are done periodically (depending on the delay
        setting), so there is ordinarily no reason to call it from
        outside of the system.

        Implementation note: this method updates the entire
        system. Since each part may have its own delay interval, the
        parts are responsible for calling their own update methods
        independently of the system. In other words, this method is
        ordinarily never called.
        """
        for part in self.parts():
            part.update()

    def set_delay(self,interval):
        """Sets the update interval after which information is
        refreshed, in seconds. This may be a fraction.
        """
        self._delay=interval

    def delay(self):
        """Returns the update interval after which information is
        refreshed in seconds.
        """
        return self._delay

    def set_callback(self,callback):
        """Sets the callback class to be used
        
        Generally, this function is not needed, as a callback class is
        usually created that can be used without setting a new one. 
        """
        self._callback=callback

    def callback(self):
        """Returns the callback class being used
        """
        return self._callback

    def parts(self):
        """Returns a list of all parts of the system.
        """
        return (self._processors+
                [self._memory]+
                self._filesystems+
                self._drives+
                [self._uptime]+
                self._netconns+
                [self._processlist])

    def set_uptime(self,uptime):
        """Sets the system's uptime object.
        """
        uptime.set_system(self)
        self._uptime=uptime

    def uptime(self):
        """Returns the system's uptime object.
        """
        return self._uptime

    def add_processor(self,processor):
        """Adds a processor to the system.
        """
        processor.set_system(self)
        self._processors+=[processor]

    def processors(self):
        """Returns a list of processors in the system.
        """
        return self._processors

    def processor(self,name):
        """Returns the processor with the specified name, or None if
        there is none.
        """
        for p in self.processors():
            if p.name()==name:
                return p
        return None

    def set_memory(self,memory):
        """Sets the system's memory bank.
        """
        memory.set_system(self)
        self._memory=memory

    def memory(self):
        """Returns the system's memory bank.
        """
        return self._memory

    def add_drive(self,drive):
        """adds a drive to the system
        """
        drive.set_system(self)
        self._drives+=[drive]

    def drives(self):
        """Returns a list of all physical drives in the system.
        """
        return self._drives

    def add_filesystem(self,filesystem):
        """adds a filesystem to the system
        """
        filesystem.set_system(self)
        self._filesystems+=[filesystem]

    def filesystems(self):
        """Returns a list of all filesystems in the system.
        """
        return self._filesystems

    def add_networkconnection(self,nc):
        """Adds a network connection to the system.
        """
        nc.set_system(self)
        self._netconns+=[nc]

    def networkconnections(self):
        """Returns a list of all network connections in the system
        """
        return self._netconns

    def set_processlist(self,processlist):
        """Sets the object representing the process list.
        """
        processlist.set_system(self)
        self._processlist=processlist

    def processlist(self):
        """Returns the object representing the process list.
        """
        return self._processlist


class SystemPart():
    """Represents a part of a system.
    """
    def __init__(self):
        self._delay=None
        self._system=None
        self.timer=None
        self._history=SystemPartHistory(self)

    @staticmethod
    def values():
        """An abstract method returning a list of functions referring
        to data contained in an object of this class.

        This method must be implemented by every subclass that.
        """
        raise UnimplementedError("SystemParts must implement values()")
    
    @staticmethod
    def null():
        """Returns a null part to be used when no real part is
        available.
        """
        return SystemPart()

    def update(self):
        """Performs an update of the part's information.

        This method is called periodically (depending on the delay
        setting), so there is ordinarily no reason to call it from
        outside of the system.
        """
        #make sure we have a valid delay
        if not self.delay():
            self.set_delay(self.system().delay())
            

        #acquire the lock
        self.system().acquire()
        #do the wuhk
        self.do_update()

        #don't set the timer if we're weird
        if not self.delay()==-1:
            #reset the timer
            self.timer=Timer(self.delay(),self.update)
            self.timer.daemon=True
            self.timer.start()
        #release the lock
        self.system().release()

    def callback(self):
        return self.system().callback()

    def do_update(self):
        """Perform the actual update.

        Part implementations should override this method.
        """
        self.system().callback().call("misc.updated",self)

    def set_delay(self,delay):
        """Sets the delay between updates.
        """
        self._delay=delay

    def delay(self):
        """Returns the current delay between updates.
        """
        return self._delay

    def set_system(self,system):
        """Sets the system that this part is in.

        A part may only be in one system at once - if a part is in two
        systems at once IRL, it may be best to have a representation
        of it in each system, or to make it its own system.
        """
        self._system=system

    def system(self):
        """Returns the system with which this object is associated.
        """
        return self._system

    def history(self):
        """Returns the history storing information about this part.
        """
        return self._history


class SystemPartHistory():
    """Stores the history of a system part.

    This class should not be extended. If you want to extend it, you
    are almost certainly doing something very wrong.
    """
    def __init__(self,part):
        """Creates a blank history for the given part.
        """
        self._part=part
        self.part_values=part.values()
 
    def update(self):
        """Update the part's history.

        This method needs to be called once for each update -
        SystemPartHistory will not keep track of a delay. In normal
        usage, the SystemPart will take care of this.
        """
        self.part().system().callback().call("misc.hist.updated")

    def part(self):
        """Returns the SystemPart for which this object stores
        history.  
        """
        return self._part


class Uptime(SystemPart):
    """Represents the uptime of a system.
    """
    def uptime(self):
        """Returns the uptime in seconds.
        """
        return 0

class Processor(SystemPart):
    """Represents a single abstract processor.
    """
    def name(self):
        """An appropriate name for the processor, like cpu4.
        """
        return "cpu"

    def modelname(self):
        """The modelname of this processor.
        """
        return self.dict()['model name']

    def max_freq(self):
        """The maximum frequency of this processor, in MHz.
        """
        mf=self.freq() #if nothing else is found
        #check the model name
        mn=self.modelname()
        match=re.search('([0-9.]+)GHz',mn)
        if match:
            mf=float(match.group(1))*1000
        return float(mf)

    def freq(self):
        """The current operating frequency of this processor, in MHz.
        """
        return self.dict()['cpu MHz']

    def usage(self):
        """The current usage of this processor, as a fraction.
        """
        return float(self.dict()['usage'])

    def dict(self):
        """Returns a dictionary with a massive amount of
        meta-information, by string. 

        Most implementations will take this directly out of
        /proc/cpuinfo. It is generally bad form to use this directly
        in an application.
        """
        return dict()


class Memory(SystemPart):
    """Represents a memory (RAM) bank.
    """
    def total_memory(self):
        """Returns the total amount of memory, in bytes.
        """
        return self.dict()['MemTotal']

    def free_memory(self):
        """Returns the amount of completely free memory, in bytes.

        Generally, it's better to use unused_memory, since
        free_memory doesn't count caching and other such "essentially
        free" types of memory.
        """
        return self.dict()['MemFree']

    def active_memory(self):
        """Returns the number of bytes of active memory.
        """
        return self.dict()['Active']

    def inactive_memory(self):
        """Returns the amount of inactive memory, in bytes.
        """
        return self.dict()['Inactive']

    def unused_memory(self):
        """Returns the amount of unused memory, in bytes.
        """
        return self.total_memory()-self.active_memory()

    def total_swap(self):
        """Returns the total amount of swap, in bytes.
        """
        return self.dict()['SwapTotal']

    def free_swap(self):
        """Returns the amount of free swap, in bytes.
        """
        return self.dict()['SwapFree']

    def dict(self):
        """Returns a dictionary with a massive amount of
        meta-information, by string. 

        Most implementations will take this directly out of
        /proc/meminfo. It is generally bad form to use this in an
        application.
        """
        return dict()


class Filesystem(SystemPart):
    """Represents a filesystem.
    """
    def size(self):
        """Returns the size, in bytes, of the filesystem.
        """
        return 0
    
    def used(self):
        """Returns the amount of used space, in bytes, of the
        filesystem.
        """
        return 0

    def available(self):
        """Returns the available space, in bytes, of the filesystem.
        """
        return self.size()-self.used()

    def device(self):
        """Returns the device name (the relative path from /dev).
        """
        pass
    
    def mount_point(self):
        """Returns the mount point of the drive, or None if not
        mounted.
        """
        pass

    def mounted(self):
        """Returns True if the drive is mounted, or False otherwise.
        """
        return self.mount_point()==None
    

class Drive(SystemPart):
    """Represents a physical drive.
    """
    pass

class ProcessList(SystemPart):
    """Represents a list of processes.
    """
    pass


class NetworkConnection(SystemPart):
    """Represents a single network connection
    """
    pass


class Process:
    """Represents a single process
    """
    pass


class Server:
    """Represents running server software (sshd, httpd, etc...)
    """
    pass
