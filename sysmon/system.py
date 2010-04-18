"""Provides an interface to an abstract system

"""

from threading import Timer

import callback

class System():
    """Represents an abstract system and implements some basic logic.

    """
    
    def __init__(self):
        self._processors=[]
        self._memory=Memory.null()
        self._drives=[]
        self._netconns=[] #network connections
        self._processlist=ProcessList.null()
        self._delay=5 #the update interval in seconds
        self._callback=callback.SysmonCallback()
        self._timers=[]

    def run(self):
        """Runs the system monitor.

        All parts are updated immediately, and then again at the
        interval specified in the parts' configuration.
        """
        print "hi"
        for part in self.parts():
            part.update()

    def stop(self):
        """Stops the system monitor.

        The monitor may safely be stopped and run and indefinite
        number of times.
        """
        for part in self.parts():
            part.timer.cancel()

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
        self.callback=callback

    def callback(self):
        """Returns the callback class being used
        """
        return self._callback

    def parts(self):
        """Returns a list of all parts of the system.
        """
        return (self._processors+
                [self._memory]+
                self._drives+
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
        """Returns a list of all drives in the system.
        """
        return self._drives

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
        if not self.delay():
            self.set_delay(self.system().delay())
        self.timer=Timer(self.delay(),self.update)
        self.timer.start()
        print " performing update - again in "+str(self.delay())
        self.do_update()

    def do_update(self):
        """Perform the actual update.

        Part implementations should override this method.
        """
        pass

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
    pass


class Memory(SystemPart):
    """Represents a memory (RAM) bank.
    """
    pass


class Drive(SystemPart):
    """Represents a drive.
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
