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

import thread
import socket
from system import *

def get_remote(addr):
    """Returns an object representing a remote system.
    """
    contact=RemoteContact(addr)
    system=RemoteSystem(contact)
    return system

class RemoteContact():
    """Communicates with a remote machine.

    Objects of this class may be used for communication with the
    remote machine. The necessary locking is handled automatically, so
    this class is thread-safe.
    """
    def __init__(self,addr,port=61874):
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

        This method automatically the necessary locking to be
        thread-safe. Do NOT acquire this object's lock before calling
        this method - the method will block and never return.
        """
        with self.lock():
            #get the file
            f=self.socket().makefile()
            #send the query
            f.write("%s\n" % query)
            #read until final token
            for line in f:
                if line=='*DONE':
                    break
                print line
            print "DONE"

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
        
        This constructor does not initialize the remote system - that
        is done with the get_remote method.
        """
        addr=contact.addr()
        System.__init__(self,addr)
        self._contact=contact

    def contact(self):
        """Returns the backing RemoteContact object.
        """
        return self._contact

