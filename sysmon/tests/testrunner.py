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

"""Master YASMon tester.
"""

# system imports
import os
import sys

# unit tests
from unittest import *

class MyTestSuite(TestSuite):
    """Custom TestSuite implementation for YASMon.
    """
    def __init__(self,id,cases):
        TestSuite.__init__(self,cases)
        self._id=id

    def id(self):
        return self._id

class MyTestResult(TestResult):
    """Custom TestRsult implementation for YASMon, for use with MyTestRunner.
    """
    def __init__(self,callback):
        """Constructs a MyTestResult instance that will call the specified
        callback as progress is made.
        """
        TestResult.__init__(self)
        self.callback=callback

    def addError(self,test,err):
        self.callback.addError(test,err)

    def addFailure(self,test,err):
        self.callback.addFailure(test,err)

    def addSuccess(self,test):
        self.callback.addSuccess(test)

class MyTestRunner():
    """Custom TestRunner implemenation for YASMon.

    This implementation uses curses to a limited extent for the
    creation of progress bars and, where possible, colored output.
    """
    def __init__(self):
        """Constructs a TestRunner that employs a GUI.
        """
        pass
        
    def run(self,suite):
        """Runs the given suites.
        """
        usecurses=sys.stdin.isatty()
        maxscore=100
        print suite.id()
        result=MyTestResult(self)
        suite.run(result)

    def addError(self,test,err):
        print "error: ",err

    def addFailure(self,test,err):
        print "failure: ",err

    def addSuccess(self,test):
        print "success!"
