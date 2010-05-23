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

"""Collect data from remote systems.

"""

import re,socket,thread
from system import *

def get_remote(addr,port=61874):
    """Returns an object representing a remote system.
    """
    contact=RemoteContact(addr,port)
    system=RemoteSystem(contact)
    return system

class RemoteContact():
    """Communicates with a remote machine.

    Objects of this class may be used for communication with the
    remote machine. The necessary locking is handled automatically, so
    this class is thread-safe.
    """
    def __init__(self,addr,port):
        """Connects to the remote machine.
        """
        #connect
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr,port))
        self._socket=sock
        self._lock=thread.allocate_lock()
        self._addr=addr
        self._port=port

    def query(self,query):
        """Queries the remote machine.

        This method automatically handles the necessary locking to be
        thread-safe. Do NOT acquire this object's lock before calling
        this method - the method will block and never return.
        """
        with self.lock():
            #get the file
            f=self.socket().makefile()
            #send the query
            f.write("%s\n" % query)
            f.flush()
            info=""
            #read until final token
            for line in f:
                #get rid of excess newline
                line=re.sub("\n","",line)
                if line=='*DONE':
                    #it's over
                    break
                #append the line
                info+="%s\n" % line
            return info

    def socket(self):
        """Returns the backing socket.
        
        Because using this socket erases the thread safety, this
        method should never be used.
        """
        return self._socket

    def lock(self):
        """Returns the backing lock.
        """
        return self._lock

    def acquire(self):
        """Calls acquire on the backing lock.
        """
        self._lock.acquire()

    def release(self):
        """Releases the backing lock.
        """
        self._lock.release()
    
    def addr(self):
        """Returns the remote address in use.
        """
        return self._addr

    def port(self):
        """Returns the remote port in use.
        """
        return self._port


class RemoteSystem(System):
    """Represents a remote system.
    """
    def __init__(self,contact):
        """Creates an empty remote system.
        
        This constructor DOES initialize the remote system, using the
        RemoteContact passed to it (generally by get_remote).
        """
        #initialize stuff
        addr=contact.addr()
        System.__init__(self,addr)
        self._contact=contact
        #assume certain things - we have uptime, memory, etc...
        self.set_uptime(RemoteUptime(contact))
        self.set_memory(RemoteMemory(contact))
        self.set_processlist(RemoteProcessList(contact))
        #get information from the contact
        info=contact.query('overview')
        lines=re.split("\n",info)
        for line in lines:
            #processor?
            match=re.match("^processor ([a-z0-9]+)",line)
            if match:
                #create the processor and add it to the system
                print match.group(1)
            #filesystem?
            match=re.match("^filesystem ([a-z0-9]+)",line)
            if match:
                #create the filesystem and add it to the system
                print match.group(1)


    def contact(self):
        """Returns the backing RemoteContact object.
        """
        return self._contact


class RemoteUptime(Uptime):
    """Represents the uptime of a remote system.
    """
    def __init__(self,contact):
        """Creates a RemoteUptime instance based on the given
        RemoteContact.
        """
        Uptime.__init__(self)
        self._contact=contact
        self._uptime=0

    def uptime(self):
        return self._uptime

    def do_update(self):
        info=self._contact.query('uptime')
        self._uptime=int(info)
        self.callback().call("uptime.updated",self)
        
    def contact(self):
        """Returns the backing RemoteContact object.
        """
        return self._contact

class RemoteMemory(Memory):
    """Represents the physical memory (RAM) of a remote system.
    """
    def __init__(self,contact):
        """Creates a RemoteMemory instance based on the given
        RemoteContact.
        """
        Memory.__init__(self)

    def contact(self):
        """Returns the backing RemoteContact object.
        """
        return self._contact


class RemoteProcessList(ProcessList):
    """Represents the ProcessList of a remote system.
    """
    def __init__(self,contact):
        """Creates a RemoteProcessList instance based on the given
        RemoteContact.
        """
        ProcessList.__init__(self)

    def contact(self):
        """Returns the backing RemoteContact object.
        """
        return self._contact

