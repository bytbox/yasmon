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

"""Improved versions of Qt4 widgets for use in YASMon.

All classes in this module use the prefix 'QM' for 'QtMod'.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class QMKeyValueTable(QTableWidget):
    """Displays a basic, two-column, immutable table.
    """
    row_height=20
    def __init__(self):
        """There are no configuration options.
        """
        QTableWidget.__init__(self,0,2)
        self.content = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    def addRow(self,key,value):
        """Add a row with the specified key and value.

        A tuple with the QMTableItems containing the key and the value is
        returned.
        """
        # add the stuff to our content database
        items = (QTableWidgetItem(key),
                 QTableWidgetItem(value))
        self.content += [items]
        rc=self.rowCount()
        # add this row to the gui
        self.insertRow(rc)
        self.setItem(rc,0,items[0])
        self.setItem(rc,1,items[1])
        self.setRowHeight(rc,self.row_height)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        # set the minimum size
        self.setMinimumHeight(self.sizeHint().height())
        self.setMinimumWidth(self.columnWidth(0)+
                             6+self.columnWidth(1))
        # return the tuple of QTableWidgetItems
        return items

    def sizeHint(self):
        return QSize(-1,
                     (self.row_height)*(len(self.content))+4)
