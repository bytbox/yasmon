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

"""Provides a framework for a graphical user interface to YASMon.

"""

#GUI Code for YASMon client (uses QT4)
from PyQt4.QtCore import *
from PyQt4.QtGui import *

local=None

def set_local_system(lsys):
    global local
    local=lsys

class ScaleView(QWidget):
    """A widget to view information on a scale, with details
    below.
    
    """
    def __init__(self,name,min=0,max=100,suffix="%",default=0):
        QWidget.__init__(self)
        self.name=name
        self.min=min
        self.max=max
        self._value=default
        self.suffix=suffix
        
    def value(self):
        """Returns the current value.
        """
        return self._value

    def set_value(self,value):
        """Sets the value to be displayed.
        
        This method sets the value stored in the object and
        updates the onscreen representation.
        """
        self._value=value
        self.update()
        
    def paintEvent(self,event):
        #settings
        painter=QPainter(self)
        painter.setPen(QPen())
        painter.setBrush(QBrush())
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.drawText(QRect(0,0,70,80),
                         Qt.AlignHCenter | Qt.AlignBottom,
                         self.name+"\n"+str(self.value())+
                         self.suffix)

    def sizeHint(self):
        return QSize(70,100)


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
    def __init__(self):
        QWidget.__init__(self)
        layout=QHBoxLayout()
        self.setLayout(layout)
        #for each cpu...
        for processor in local.processors():
            layout.addWidget(CPUView(local.processor(processor.name())))
            
class MemoryView(ScaleView):
    """A widget to display the current memory usage in a memory
    bank (RAM).
    
    """
    def __init__(self,memory):
        ScaleView.__init__(self,"ram")
        self.memory=memory

class LocalMemoryView(MemoryView):
    """A widget to display the current memory usage in the local
    RAM.
    
    """
    
    def __init__(self):
        MemoryView.__init__(self,local.memory())
        local.callback().hook('local.memory.updated',self.catch_update)
        
    def catch_update(self,data):
        self.set_value(int(float(self.memory.active_memory())*1000.0
                           /float(self.memory.total_memory()))/10.0)
        print self.value()
        
class RemoteMemoryView(MemoryView):
    """A widget to display the current memory usage in remote RAM.
    """
    pass

class OverviewView(QFrame):
    """Displays current information for the most general (and
    critical) parts of the system
    
    This generally means the processors, memory, and hard disk
    usage.
    """
    def __init__(self):
        QFrame.__init__(self)
        self.setLineWidth(2);
        self.setFrameStyle(self.StyledPanel | QFrame.Raised)
        layout=QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(ProcessorView())
        layout.addWidget(LocalMemoryView())
        
class HistoryView(QFrame):
    """Displays most of OverviewView's content, as a history.
    
    This view consists of a set of a few graphs, each containing
    in somewhat condensed for the history of some measure of
    performance. A single pixel is used for every related update
    fired.
    """
    def __init__(self):
        QFrame.__init__(self)
        
class MainView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout=QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(OverviewView())
        layout.addWidget(QLabel("ho"))
        
