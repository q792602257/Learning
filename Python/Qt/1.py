#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import os
from PyQt5 import QtWidgets
#reload(sys)
#sys.setdefaultencoding("utf8")
app=QtWidgets.QApplication(sys.argv)
label=QtWidgets.QLabel("<p style='color: red; margin-left: 20px'><b>hell world</b></p>")
label.show()
sys.exit(app.exec_())
