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

import callback

class System():
    """Represents an abstract system and implements some basic logic.

    """
    
    def __init__(self,name="no-name"):
        self.lock=Lock()
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
                self._netconns+
                [self._processlist])

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
        #don't do anything if we're weird
        if self.delay()==-1:
            return

        #acquire the lock
        self.system().acquire()
        #do the wuhk
        self.do_update()
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
        return self._system


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
        return "Unknown"

    def max_freq(self):
        """The maximum frequency of this processor, in MHz.
        """
        return 0

    def freq(self):
        """The current operating frequency of this processor, in MHz.
        """
        return 0

    def usage(self):
        """The current usage of this processor, as a fraction.
        """
        return 0

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
        return 0

    def free_memory(self):
        """Returns the amount of completely free memory, in bytes.

        Generally, it's better to use unused_memory, since
        free_memory doesn't count caching and other such "essentially
        free" types of memory.
        """
        return 0

    def active_memory(self):
        """Returns the number of bytes of active memory.
        """
        return 0

    def inactive_memory(self):
        """Returns the amount of inactive memory, in bytes.
        """
        return 0

    def unused_memory(self):
        """Returns the amount of unused memory, in bytes.
        """
        return self.total_memory()-self.active_memory()

    def total_swap(self):
        """Returns the total amount of swap, in bytes.
        """
        return 0

    def free_swap(self):
        """Returns the amount of free swap, in bytes.
        """
        return 0

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
    pass

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
