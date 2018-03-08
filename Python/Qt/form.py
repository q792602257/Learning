# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(176*2, 264*2)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(8, 0, 176*2, 56*2))
        self.label.setObjectName("label")
        self.label.setBackgroundRole(QtGui.QPalette.ColorRole(0))
        self.label.setFont(QtGui.QFont("pixelmix",72))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(600, 20, 181, 91))
        self.pushButton.setObjectName("pushButton")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton.setGeometry(QtCore.QRect(600, 140, 172, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(290, 30, 37, 18))
        self.toolButton.setObjectName("toolButton")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        now = datetime.datetime.now()
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Form")
        self.pushButton.setText("0")
        self.commandLinkButton.setText("Form, CommandLinkButton")
        self.toolButton.setText(_translate("Form", "..."))
        self.label.setText(now.strftime("%H:%M"))

