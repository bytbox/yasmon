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
from PyQt4 import QtSvg

import re,sys,sysmon,traceback

def about_yasmon(parent):
    """Displays an "About YASMon" dialog box.
    """
    dialog=AboutYasmon(parent)
    dialog.exec_()

def yasmon_icon():
    """Returns a scalable version of YASMon's icon.
    """
    return QIcon("/usr/share/icons/hicolor/scalable/apps/yasmon.svg")

def yasmon_image():
    """Returns an QSvgWidget with YASMon's logo
    """
    i=QtSvg.QSvgWidget("/usr/share/icons/hicolor/scalable/apps/yasmon.svg")
    i.setMaximumSize(i.sizeHint())
    i.setMinimumSize(i.sizeHint())
    return i

def qt_icon():
    """Returns a scalable version of QT's logo.
    """
    return QIcon()

class AboutYasmon(QDialog):
    """YASMon's about dialog box.
    """
    def __init__(self,parent):
        super(AboutYasmon, self).__init__(parent)
        self.setWindowTitle("About YASMon")
        overlayout=QVBoxLayout()
        layout=QHBoxLayout()
        layout.addWidget(yasmon_image())
        sublayout=QVBoxLayout()
        sublayout.addWidget(QLabel("<html><b>"+
                                   "Yet Another System Monitor</b></html>"))
        sublayout.addWidget(QLabel("<html><p>Version %s</p>" % sysmon.version()
                                   +"<p>&copy; 2010 Scott Lawrence "
                                   +"&lt;<a href='mailto:bytbox@gmail.com'>"
                                   +"bytbox@gmail.com</a>&gt;</p>"
                                   +"<p>Licensed under the GNU GPL version 3 "
                                   +"or, at your <br />choice, any later "
                                   +"version.</p></html>"))
        layout.addLayout(sublayout)
        overlayout.addLayout(layout)
        bb=QDialogButtonBox(QDialogButtonBox.Ok,Qt.Horizontal,self)
        bb.setCenterButtons(True)
        bb.accepted.connect(self.accept)
        overlayout.addWidget(bb)
        self.setLayout(overlayout)


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
        self.setMaximumSize(QSize(70,100))
        self.setMinimumSize(QSize(70,100))
        
    def value(self):
        """Returns the current value.
        """
        return self._value

    def set_max(self,maxval):
        """Sets the maximum value.
        """
        self.max=maxval
    def set_min(self,minval):
        """Sets the minimum value.
        """
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

        #draw the scale
        painter.drawRect(QRect(7,0,56,64))
        height=(float(self.value())-self.min)*64.0/self.max
        painter.fillRect(QRect(7,64,56,-height),QColor.fromRgb(height*3.9,0,0))
        #draw the text
        painter.drawText(QRect(0,0,70,100),
                         Qt.AlignHCenter | Qt.AlignBottom,
                         self.name+"\n"+str(float(int((self.value()-self.min)*1000.0/self.max))/10)+'%')


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
        ScaleView.__init__(self,processor.name(),0,1,"MHz used")
        self.processor=processor
        #add me to the hook
        processor.system().callback().hook("processor.%s.updated" % processor.name()
                                           ,self.catch_update)

    def catch_update(self,processor):
        self.set_max(self.processor.max_freq())
        self.set_value(self.processor.usage())
        

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
        self.set_max(self.memory.total_memory()/1000000.)
        self.set_value(self.memory.active_memory()/1000000.)

class UptimeView(QLabel):
    """A widget to display the current system uptime.
    """
    def __init__(self,uptime):
        QLabel.__init__(self)
        self.uptime=uptime
        self.setAlignment(Qt.AlignCenter)
        uptime.system().callback().hook('uptime.updated',self.catch_update)
        
    def catch_update(self,data):
        uptime=int(self.uptime.uptime())
        days=uptime/(60*60*24.)
        hours=int(uptime/(60*60.))%24
        mins=(int(uptime/60.)%60)
        secs=uptime%60
        self.setText("Up %d days, %02d:%02d:%02d" % (days,hours,mins,secs)) 

    def sizeHint(self):
        return QSize(120,20)

class SystemView(QGroupBox):
    """Displays current information for the most general (and
    critical) parts of a single system.
    
    This generally means the processors, memory, and hard disk
    usage.
    """
    def __init__(self,system):
        QFrame.__init__(self,system.name())
        overlayout=QVBoxLayout()
        layout=QHBoxLayout()
        self.setLayout(overlayout)
        overlayout.addWidget(UptimeView(system.uptime()))
        overlayout.addSpacing(10)
        overlayout.addLayout(layout)
        layout.addWidget(ProcessorView(system.processors()))
        layout.addSpacing(16)
        layout.addWidget(MemoryView(system.memory()))
        
class HistoryView(QFrame):
    """Displays most of OverviewView's content, as a history.
    
    This view consists of a set of a few graphs, each containing in
    somewhat condensed for the history of some measure of
    performance. In general, single pixel is used for every related
    update fired.
    """
    def __init__(self,system):
        QFrame.__init__(self)

class TopView(QFrame):
    """Displays a top-like view of a system.
    """
    def __init__(self,system):
        QFrame.__init__(self)

class MetaView(QTableWidget):
    """Displays interesting/semi-important static meta-information
    about the system.
    """
    def __init__(self,system):
        QTableWidget.__init__(self,0,2)
        self.setColumnWidth(1,600)
        self.meta=system.meta()
        #enable satus bar stuff
        self.setMouseTracking(True)
        for key in self.meta:
            desc=self.meta[key][0]
            value=self.meta[key][1]
            rc=self.rowCount()
            self.insertRow(rc)
            self.setRowHeight(rc,20)
            #key field
            ki=QTableWidgetItem(key)
            #show description stuff
            ki.setToolTip(desc)
            ki.setStatusTip(desc)
            ki.setWhatsThis(desc)
            #flags
            ki.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            
            #value field
            vi=QTableWidgetItem(value)
            #flags
            vi.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            #expand on the value
            vi.setToolTip(value)
            vi.setStatusTip(value)
            vi.setWhatsThis(desc)
            self.setItem(rc,0,ki)
            self.setItem(rc,1,vi)
    def sizeHint(self):
        return QSize(650,100)
        

class DetailedSystemView(QFrame):
    """Displays a detailed system view, consisting of a MetaView,
    a HistoryView, and a TopView.
    """
    def __init__(self,system):
        QFrame.__init__(self)
        layout=QVBoxLayout()
        sublayout=QHBoxLayout()
        layout.addWidget(MetaView(system))
        layout.addLayout(sublayout)
        self.setLayout(layout)
        
class MainView(QWidget):
    """The main view - contains everything else.

    This is what the simplest graphical applications will want to use,
    as it contains all of YASMon's functionality.
    """
    def __init__(self,systems):
        QWidget.__init__(self)
        layout=QVBoxLayout()
        sublayout=QHBoxLayout()
        self.setLayout(layout)
        tabWidget=QTabWidget()
        tabWidget.setTabPosition(QTabWidget.South)
        for system in systems:
            tabid=tabWidget.addTab(DetailedSystemView(systems[system]),QString(system))
            tabWidget.setTabToolTip(tabid,QString("View information for %s" % system))
            sublayout.addWidget(SystemView(systems[system]))
        sublayout.addStretch()
        layout.addLayout(sublayout)
        layout.addWidget(tabWidget)
        
