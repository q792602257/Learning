# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def __init__(self, *args, **kwargs):
        self.DPI=1.5
        self.width=176*self.DPI
        self.height=264*self.DPI
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setGeometry(1000,32,self.width*self.DPI, self.height*self.DPI)
        Form.setWindowOpacity(0.8)
        Form.setStyleSheet("""
        QMainWindow {
            background:gray;
        }
        QLabel {
            color:black;
            background:white;
        }
        QLabel[bw="true"] {
            color:white;
            background:black;
        }""")
        self.BigTime = QtWidgets.QLabel(Form)
        self.BigTime.setGeometry(QtCore.QRect(0, 0, int(self.width*self.DPI), int(36*self.DPI)))
        self.BigTime.setObjectName("BigTime")
        self.BigTime.setFont(QtGui.QFont("Inziu Iosevka SC",int(32*self.DPI),QtGui.QFont.Bold))
        self.SmallDate=QtWidgets.QLabel(Form)
        self.SmallDate.setProperty("bw",True)
        self.SmallDate.setGeometry(QtCore.QRect(self.width-int(96*self.DPI), self.BigTime.height(), int(96*self.DPI), int(20*self.DPI)))
        self.SmallDate.setFont(QtGui.QFont("Inziu Iosevka SC",int(12*self.DPI),QtGui.QFont.Bold))
        self.update_time()
        self.Temp = QtWidgets.QLabel(Form)
        self.Temp.setProperty("bw",True)
        self.Temp.setGeometry(QtCore.QRect(0, self.BigTime.height(), self.width-self.SmallDate.width()-1,int(20*self.DPI)))
        self.Temp.setFont(QtGui.QFont("Inziu Iosevka SC",int(12*self.DPI)))
        self.Temp.setText("00[00.0]℃")
        self.Weather = QtWidgets.QLabel(Form)
        self.Weather.setGeometry(QtCore.QRect(0, self.SmallDate.y()+self.SmallDate.height(), int(80*self.DPI),int(60*self.DPI)))
        self.Weather.setFont(QtGui.QFont("Inziu Iosevka SC",int(40*self.DPI)))
        self.Weather.setText(str(self.SmallDate.y()+self.SmallDate.height()))
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton.setGeometry(QtCore.QRect(600, 140, 172, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        now = datetime.datetime.now()
        self.BigTime.setText(now.strftime("%H:%M:%S"))
        self.SmallDate.setText(now.strftime("%y/%m/%d")+"<small> "+now.strftime("%a")+"</small>")

    def retranslateUi(self, Form):
        Form.setWindowTitle("Form")
        self.commandLinkButton.setText("Form, CommandLinkButton")
