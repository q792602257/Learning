# coding:utf8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
import sqlite3 as sq
import _winreg as reg
import glob
import json

class ImagePrint():
	path=False
	JobID=False
	def __init__(self):
		try:
			key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Code Industry\\ImagePrinterPro\\')
			self.JobID,t=reg.QueryValueEx(key,'jobid')
			self.Pre,t=reg.QueryValueEx(key,"image_name")
			self.Path,t=reg.QueryValueEx(key,"path")
			print self.JobID,self.Pre,self.Path
		except Exception as e:
			sys.exit()
	def getJobID(self):
		try:
			key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Code Industry\\ImagePrinterPro\\')
			self.JobID,t=reg.QueryValueEx(key,'jobid')
		except Exception as e:
			sys.exit()
		return self.JobID
	def getPriview(self,filename):
		pass
class FilePrint():
	printerName="Unkown"
	def printFile(self,filename):
		pass
# "C:\PROGRAM FILES\FOXIT SOFTWARE\FOXIT READER\FOXITREADER.EXE" /q /t C:\Users\yan1h\Documents\1.pdf "Send To OneNote 2016"
# "C:\Program Files\Microsoft Office\Root\Office16\EXCEL.EXE" /q C:\Users\yan1h\Documents\1.xlsx /j "Send To OneNote 2016"
# "C:\Program Files\Microsoft Office\Root\Office16\WINWORD.EXE" /j "%1" "%2"
# %SystemRoot%\system32\NOTEPAD.EXE /pt %1
# "%SystemRoot%\System32\rundll32.exe" "%SystemRoot%\System32\shimgvw.dll",ImageView_PrintTo /pt C:\Users\yan1h\Documents\Learning\wallpaper\19484.jpg "Send To OneNote 2016"
	
class Socket():
	addr='0.0.0.0'
	port=9999
	s=False
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	def listen(self):
		self.s.bind((self.addr,self.port))
		self.s.listen(5)
		while True:
			try:
				self.con,addr=self.s.accept()
			except Exception as e:
				sys.exit()
			print addr
			recv = self.con.recv(65536)
			self.handler(recv)
	def handler(self,recv):
		if "jerryadmin" == recv[:10] and (["{","}"] == [recv[10], recv[-2]] or ["[","]"] == [recv[10], recv[-2]]):
			a=json.loads(recv[10:-1])
		else:
			print recv
			self.Send("Please Use The Software To Access This.")
			self.con.close()
	def Send(self,data):
		pass
print ImagePrint().getJobID()