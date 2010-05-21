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

"""Provides an interface to the null machine.

"""

from system import *;

def get_null():
    """Returns an object representing the null system.
    """
    system=NullSystem()

class NullSystem(System):
    """Represents a null system.

    """
    def __init__(self):
        System.__init__(self)


class NullProcessor(Processor):
    """Represents a null processor
    """
    pass


class NullMemory(Memory):
    """Represents a null memory (RAM) bank
    """
    pass


class NullFilesystem(Filesystem):
    """Represents a null filesystem
    """
    pass


class NullDrive(Drive):
    """Represents a null drive
    """
    pass


class NullProcessList(ProcessList):
    """Represents a null list of processes
    """
    pass


class NullProcess(Process):
    """Represents a single null process
    """
    pass
