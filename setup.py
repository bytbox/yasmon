#!/usr/bin/python

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

from distutils.core import setup

import sysmon

#generate icon installation list (hicolor)
iconlist=[]
for x in [16,22,24,32,36,48,64,72,96,128,192,256]:
    dest="/usr/share/icons/hicolor/%dx%d/apps" % (x,x)
    src="gr/%dx%d/yasmon.png" % (x,x)
    iconlist=iconlist+[(dest,[src])]

setup(name='YASMon',
      version=sysmon.version(),
      description='yet another system monitor',
      author='Scott Lawrence',
      author_email='bytbox@gmail.com',
      maintainer='Scott Lawrence',
      maintainer_email='bytbox@gmail.com',
      url='http://github.com/bytbox/yasmon',
      requires=['PyQt4'],
      packages=['sysmon'],
      scripts=['yasmon','yasmond'],
      data_files=[('/usr/share/man/man1',['yasmon.1','yasmond.1']),
                  ('/usr/share/applications',['yasmon.desktop']),
                  ('/usr/share/icons/hicolor/scalable/apps',['gr/yasmon.svg']),
                  ('/usr/share/app-install/icons',['gr/yasmon.png']),
                  ('/usr/share/pixmaps',['gr/yasmon.png']),
                  ('/usr/share/icons/hicolor/scalable/apps',
                   ['gr/yasmon.svg'])]+iconlist)
