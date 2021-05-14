# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 16:21:57 2018

@author: o.beckett
"""

import sys
import strings as s
import colours as c
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from termite_profile import Profile
 
class MyProfileTable(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.profile = data
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
 
    def setmydata(self):
        '''poulate the table with profile data'''
        for i, row in enumerate(self.profile.values):
            for j, val in enumerate(row):
                if val is None:
                    newitem=QTableWidgetItem("")
                else:
                    newitem = QTableWidgetItem('{0:.2f}'.format(val))
                newitem.setBackground(c.qbrush_from_perc(self.profile.get_value(i, j)))
                #print(newitem)
                self.setItem(i, j, newitem)
        self.setHorizontalHeaderLabels(s.TIMESOFDAY)
        self.setVerticalHeaderLabels(s.DAYSOFTHEWEEK)
        self.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        try:
            value = float(item.text())
        except:
            value = 0
        item.setBackground(c.qbrush_from_perc(value)) 
        
class MyProfileEditorView(QWidget):
    def __init__(self, my_profile):
        QWidget.__init__(self)
        self.setWindowTitle(my_profile.name)
        self.setStyleSheet("qtdarkstyle.ccs")
        
        self.layout = QVBoxLayout()
        self.my_label = QLabel(my_profile.name)
        self.table = MyProfileTable(my_profile, 7, 24)
        self.ok_button = QPushButton("Ok", self)
        
        self.ok_button.clicked.connect(self.ok_clicked)
        
        self.layout.addWidget(self.my_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.ok_button)
        
        self.setMinimumSize(1050, 270)
        
        self.setLayout(self.layout)
    
    def run(self):
        self.show()
        
    def ok_clicked(self):
        print("Hello World")
        self.destroy()
        

def main(args):
    my_profile = Profile()
    my_profile.name = "Always on"
    my_profile.set_increasing()
    my_profile.set_nine_to_five()
    my_profile.values[4,4]=0.5
    
    qt_app = QApplication(args)
    css = r"J:\J9999\O.Beckett\Tools\py\AIDA\qtdarkstyle.css"
    with open(css, "r") as fh:
        qt_app.setStyleSheet(fh.read())
   
    
    window = MyProfileEditorView(my_profile)
    window.run()
    
    sys.exit(qt_app.exec_())
 
if __name__=="__main__":
    main(sys.argv)