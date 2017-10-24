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
from time import sleep

class ImagePrint():
	printerName="ImagePrinter"
	def __init__(self):
		try:
			key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Code Industry\\ImagePrinterPro\\')
			self.JobID,t=reg.QueryValueEx(key,'jobid')
			self.Pre,t=reg.QueryValueEx(key,"image_name")
			self.Path,t=reg.QueryValueEx(key,"path")
			print self.JobID,self.Pre,self.Path
			self.Busy=False
			self.waitNew=True
		except Exception as e:
			sys.exit()
	def getJobID(self):
		key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,'SOFTWARE\\Code Industry\\ImagePrinterPro\\')
		JobID,t=reg.QueryValueEx(key,'jobid')
		return JobID
	def waitNewJob(self):
		if not self.waitNew:
			return self.JobID
		while self.JobID==self.getJobID():
			sleep(1)
		self.waitNew=False
		return self.JobID	
	def getPriview(self,jobid=False):
		if jobid:
			newJobID=jobid
			JobID=jobid
		else:
			self.waitNewJob()
			JobID=self.JobID
		while (not os.path.isfile(os.path.join(self.Path,self.Pre+"_%s.png"%(JobID)))) and len(glob.glob(os.path.join(self.Path,self.Pre+"_%s_*.png"%(JobID))))==0:
			sleep(2)
		if os.path.isfile(os.path.join(self.Path,self.Pre+"_%s.png"%(JobID))):
			self.pages=1
			imgs= [os.path.join(self.Path,self.Pre+"_%s.png"%(JobID))]
		else:
			imgs = glob.glob(os.path.join(self.Path,self.Pre+"_%s_*.png"%(JobID)))
		self.page=len(imgs)
		return imgs
	def buildPriview(self,filename):
		while self.Busy:
			sleep(1)
		if os.path.isfile(filename):
			t = filetypeDetector(filename)
			cmd = printCommand(t).replace(r"%1",filename).replace(r"%2",self.printerName)
			print cmd
			self.Busy=True
			os.system(cmd)
			self.waitNew=True
			self.Busy=False
			imgs = self.getPriview()
			self.JobID=self.getJobID()
			return imgs
		return False
class FilePrint():
	printerName="Unkown"
	def printFile(self,filename):
		if os.path.isfile(filename):
			t = filetypeDetector(filename)
			cmd = printCommand(t).replace(r"%1",filename).replace(r"%2",self.printerName)
			os.popen(cmd)
def printCommand(t):
	if t=="Doc":
		return u'"C:\\Progra~1\\Micros~3\\Office14\\WINWORD.EXE" /j "%1" "%2"'
	elif t=="Xls":
		return u'"C:\\Progra~1\\Micros~3\\Office14\\EXCEL.EXE" /q "%1" /j "%2"'
	elif t=="Ppt":
		return u'"C:\\Progra~1\\Micros~3\\Office14\\POWERPNT.EXE" /pt "%2" "%1"'
	elif t=="Pdf":
		return u'C:\\Progra~1\\FoxitS~1\\FoxitR~1\\FOXITR~1.EXE /q /t "%1" "%2"'
	elif t=="Img":
		return u'%SystemRoot%\\System32\\rundll32.exe %SystemRoot%\\System32\\shimgvw.dll,ImageView_PrintTo /pt "%1" "%2"'
	return False
def filetypeDetector(filename):
	if ".doc" in filename:
		return "Doc"
	elif ".xls" in filename:
		return "Xls"
	elif ".ppt" in filename:
		return "Ppt"
	elif ".pdf" in filename:
		return "Pdf"
	elif ".jpg" in filename or ".png" in filename:
		return "Img"
	return False
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
# print ImagePrint().buildPriview('C:\Users\Windows\Documents\RFID.pdf')
print ImagePrint().getPriview("18")