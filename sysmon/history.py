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

"""Provides utilities for storing and analyzing histories of parts.
"""

import cPickle

import sysmon

class PartHistory():
    """Stores the history of a single part.

    Because different parts of the history might be needed at different times,
    PartHistory serializes the entire part.
    """
    def __init__(self,part):
        """Creates a self-managing PartHistory for the given part.

        The PartHistory will need no maintenance - at any point in the
        future, it may be queried for the most up-to-date history data.
        """
        # remember the part
        self.part=part
        # add the hook
        part.system().callback().hook(part.update_hook(),
                                      self.catch_update)
        # initialize history with current values
        self.hist=[self.part.data_copy()]

    def catch_update(self,data):
        """Updates the history.

        This method is called after the attached part updates (by the hook
        system), and should not be called in any other way, as this would
        confuse and possibly corrupt the history record.
        """
        # append the current data to the history
        self.hist += [self.part.data_copy()]
