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

"""YASMon error handling.
"""

class Error(Exception):
    """Base class for YASMon errors.
    """
    def __init__(self,msg="Unknown"):
        Exception.__init__(self)
        self.msg=msg
    def __str__(self):
        return self.msg

class UserError(Error):
    """Error indicating that the user did something wrong.
    """
    def __init__(self,msg="Unknown"):
        Error.__init__(self,msg)

class CLArgumentError(UserError):
    """The command-line arguments were bad.
    """
    def __init__(self,msg="Unknown"):
        UserError.__init__(self,msg)

class InsaneError(Error):
    """Something about the environment is insane - this may make data
    collection impossible.
    """
    def __init__(self,msg="Insane environment"):
        Error.__init__(self,msg)

class RemoteError(Error):
    """An error occurred when talking to a remote machine.
    """
    def __init__(self,remote,msg="Unknown"):
        Error.__init__(self,"%s (remote = %s)" % (msg,remote))

