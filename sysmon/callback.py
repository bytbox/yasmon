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

"""Provides a flexible and extensible callback class for the system
monitor.

"""

class SysmonCallback:
    """A flexible and extensible callback class for sysmon.

    Callback functions are registered with a unique identifying
    string, usually of the form part1.part2.specific. 

    Callback functions are called with a single argument, usually a
    dictionary. Callback functions are called in the order they were
    registered.
    """

    def __init__(self):
        """Creates an empty callback.
        """
        self.hooks=dict([])
    
    def hook(self,name,func):
        """Hooks the given function onto a string.

        Whenever the string is called, the given function will be
        called with a single argument (passed from the original
        caller).
        """
        if name in self.hooks:
            self.hooks[name].append(func)
        else:
            self.hooks[name]=[func]

    def call(self,name,part):
        """Calls all hooks matching the string with the given data
        (usually the caller).

        The hooks are called in the order they were created.
        """
        if name in self.hooks:
            for func in self.hooks[name]:
                func(part)
