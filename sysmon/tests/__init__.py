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

"""Test suites for YASMon
"""

#unit tests
from unittest import *

#available unit tests
import localtest,remotetest,daemontest,testrunner


def run_tests():
    """Simple interface to run all tests.
    """
    #run the tests!
    runner=TextTestRunner(verbosity=2)
    #for each suite
    suites=[localtest.suite(),remotetest.suite(),daemontest.suite()]
    for suite in suites:
        runner.run(suite)
