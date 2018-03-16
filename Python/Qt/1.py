#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from form import Ui_Form
from time import sleep
#reload(sys)
#sys.setdefaultencoding("utf8")
class mywindow(QtWidgets.QWidget,Ui_Form):    
    def __init__(self):    
        self.times=0
        super(mywindow,self).__init__()    
        self.setupUi(self)
        self.commandLinkButton.clicked.connect(self.hello)

    #定义槽函数
    def hello(self):
        self.times+=1
        print("Ok")
        sleep(1)
        self.label.setText(str(self.times))

app = QtWidgets.QApplication(sys.argv)
window = mywindow()
window.setFixedSize(window.width, window.height)
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
window.show()
sys.exit(app.exec_())