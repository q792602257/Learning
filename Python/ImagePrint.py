# coding:utf8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
import json

class ImagePrint():
	path=False
	JobID=False
	def getJobID(self):
		try:
			f=open(os.path.join(self.path,'JobID'),'r+')
			self.JobID=f.readline()
			f.close()
		except Exception as e:
			sys.exit()
		return self.JobID
	def genJobID(self):
		pass
	def printFile(self,filename):
		pass
	
class Socket(ImagePrint):
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