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

"""Provides a framework for a graphical user interface to YASMon,
using Qt4.

"""

#GUI Code for YASMon client (uses QT4)
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sysmon

def about_yasmon(parent):
    """Displays an "About YASMon" dialog box.
    """
    QMessageBox.about(parent, "About YASMon",
                      "<b>YASMon v"+sysmon.version())


class ScaleView(QWidget):
    """A widget to view information on a scale, with details
    below.
    
    """
    def __init__(self,name,min=0,max=100,unit='%',default=0):
        QWidget.__init__(self)
        self.name=name
        self.min=min
        self.max=max
        self._value=default
        self.unit=unit
        self.setToolTip("%d/%d %s" % (int(self.value()),int(max),unit))
        
    def value(self):
        """Returns the current value.
        """
        return self._value

    def set_max(self,maxval):
        self.max=maxval
    def set_min(self,minval):
        self.min=minval

    def set_value(self,value):
        """Sets the value to be displayed.
        
        This method sets the value stored in the object and
        updates the onscreen representation.
        """
        self._value=value
        self.setToolTip("%d/%d %s" % (int(self.value()),int(self.max),self.unit))
        self.update()
        
    def paintEvent(self,event):
        #settings
        painter=QPainter(self)
        painter.setPen(QPen())
        painter.setBrush(QBrush())
        painter.setRenderHint(QPainter.Antialiasing)

        painter.drawRect(QRect(10,0,50,64))
        height=(float(self.value())-self.min)*64.0/self.max
        painter.fillRect(QRect(10,64,50,-height),QColor.fromRgb(height*4,0,0))
        painter.drawText(QRect(0,0,70,100),
                         Qt.AlignHCenter | Qt.AlignBottom,
                         self.name+"\n"+str(float(int((self.value()-self.min)*1000.0/self.max))/10)+'%')


    def sizeHint(self):
        return QSize(70,100)
    def minimumSize(self):
        return self.sizeHint()


class CPUView(ScaleView):
    """A widget to view cpu usage information et al. for a single
    CPU.
    
    This consists of a simple graphic, with a single vertical
    "progress bar" (labelled as appropriate) and two numbers
    below: the exact percentage usage and the current temperature,
    if available.
    
    Although this view is meant for a single CPU, it may actually
    represent multiple CPUs, depending on the implementation of
    the backend object.
    """
    def __init__(self,processor):
        ScaleView.__init__(self,processor.name())
        self.processor=processor
        #add me to the hook
        

class ProcessorView(QWidget):
    """A widget to view processor information for multiple
    processors.
    
    This will normally be significantly wider than it is tall, as
    it consists simply of a horizontal row of CPUViews.
    """
    def __init__(self,processorlist):
        QWidget.__init__(self)
        layout=QHBoxLayout()
        layout.setMargin(0)
        self.setLayout(layout)
        #for each cpu...
        for processor in processorlist:
            layout.addWidget(CPUView(processor))
            
class MemoryView(ScaleView):
    """A widget to display the current memory usage in a memory
    bank (RAM).
    
    """
    def __init__(self,memory):
        ScaleView.__init__(self,"ram",0,1,'MB')
        self.memory=memory
        memory.system().callback().hook('memory.updated',self.catch_update)

    def catch_update(self,data):
        self.set_max(self.memory.total_memory()/1000000)
        self.set_value(self.memory.active_memory()/1000000)


class SystemView(QGroupBox):
    """Displays current information for the most general (and
    critical) parts of a single system.
    
    This generally means the processors, memory, and hard disk
    usage.
    """
    def __init__(self,system):
        QFrame.__init__(self,system.name())
        layout=QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(ProcessorView(system.processors()))
        layout.addWidget(MemoryView(system.memory()))
        
class HistoryView(QFrame):
    """Displays most of OverviewView's content, as a history.
    
    This view consists of a set of a few graphs, each containing in
    somewhat condensed for the history of some measure of
    performance. In general, single pixel is used for every related
    update fired.
    """
    def __init__(self):
        QFrame.__init__(self)
        
class MainView(QWidget):
    def __init__(self,systems):
        QWidget.__init__(self)
        layout=QVBoxLayout()
        self.setLayout(layout)
        for system in systems:
            print system
            layout.addWidget(SystemView(systems[system]))
        layout.addWidget(QLabel("Tabs for HistoryView here! (TODO)"))
        
