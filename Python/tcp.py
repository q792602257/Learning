#!/usr/bin/env python
# -*- coding:utf8 -*-
import socket
import pexpect
import sys
import json
import re
reload(sys)
sys.setdefaultencoding("utf8")

class S():

	def listen(self,addr="0.0.0.0",port=8888):
		self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((addr,port))
		self.s.listen(5)
		print "Listen:\t%s:%s"%(addr,port)
		while True:
			try:
				self.con,addr=self.s.accept()
			except KeyboardInterrupt:
				print "Exiting..."
				self.Exit()
				sys.exit()
			print "From:\t%s:%s"%(addr[0],addr[1])
			recv=self.con.recv(65536)
			self.handle(recv)
	def handle(self,recv):
		if "jerryadmin" == recv[:10] and (["{","}"] == [recv[10], recv[-2]] or ["[","]"] == [recv[10], recv[-2]]):
			a=json.loads(recv[10:-1])
			if a["method"]=="shell":
				if a["shell"]:
					self.Send(self.execcmd(a["shell"]))
					self.con.close()
			elif a["method"]=="isNginx":
				self.Send(self.isNginx())
				self.con.close()
			elif a["method"]=="isMysql":
				self.Send(self.isMysql())
				self.con.close()
			elif a["method"]=="dfStat":
				self.Send(self.dfStat())
				self.con.close()
			elif a["method"]=="upTime":
				self.Send(self.upTime())
				self.con.close()
			elif a["method"]=="memStat":
				self.Send(self.memStat())
				self.con.close()
			elif a["method"]=="openPort":
				self.Send(self.openPort())
				self.con.close()
		else:
			print recv
			self.Send("Please Use The Software To Access This.")
			self.con.close()
	def execcmd(self,cmd):
		self.execresult=[]
		if type(cmd)==list:
			for i in cmd:
				print "Exec:\t%s"%i
				self.execresult.append(self.shell(i))
		elif type(cmd)==str:
			print "Exec:\t%s"%cmd
			self.execresult.append(self.shell(cmd))
		return self.execresult
	def openPort(self):
		Exec=["netstat -ntpl","netstat -nupl"]
		a=self.execcmd(Exec)
		data=[]
		for j in a:
			j=j.strip("\r\n").split("\r\n")
			j.pop(0)
			j.pop(0)
			for i in j:
				t={}
				p=re.split(" +",i.strip())
				t["prot"]=p[0]
				t["port"]=p[3].split(":")[-1]
				t["PID"]=p[-1].split("/",1)[0]
				t["prog"]=p[-1].split("/",1)[1]
				data.append(t)
		return data
	def memStat(self):
		Exec=["bash -c 'free -m|grep Mem'"]
		data = re.split(" +",self.execcmd(Exec)[0].strip("\r\n"))
		return data
	def isNginx(self):
		Exec=["bash -c 'ps -d|grep nginx|grep -v grep'","whereis nginx"]
		data = self.execcmd(Exec)
		if len(data[0].strip("\r\n").strip())!=0:
			return 1
		elif len(data[1].strip("\r\n").split(":")[1])==0:
			return 0
		else:
			return 9
	def isMysql(self):
		Exec=["bash -c 'ps -d|grep mysql|grep -v grep'","whereis mysql"]
		data = self.execcmd(Exec)
		if len(data[0].strip("\r\n").strip())!=0:
			return 1
		elif len(data[1].strip("\r\n").split(":")[1])==0:
			return 0
		else:
			return 9
	def dfStat(self):
		Exec=["bash -c 'df -h|grep /$'"]
		data = re.split(" +",self.execcmd(Exec)[0].strip("\r\n"))
		if data[-1]=="/":
			return data
	def upTime(self):
		Exec=["uptime"]
		a=self.execcmd(Exec)
		data = re.findall(r" (.+?) up *(.+?), *(\d+?) users?, *load average: (.+?), (.+?), (.+)",a[0].strip("\r\n"))[0]
		return data
	def shell(self,command):
		p=pexpect.spawn(command,timeout=5)
		try:
			result=p.read()
			return result
		except pexpect.exceptions.TIMEOUT:
			return "TimeOut"
	def Send(self,data):
		print data
		if type(data)==str or type(data)==int:
			self.con.send("jerryadmin%s2"%data)
		elif type(data)==dict or type(data)==list or type(data)==tuple:
			self.con.send("jerryadmin%s2"%json.dumps(data))
	def Exit(self):
		self.s.close()

class C():

	def connect(self,addr="jerryyan.top",port=8888):
		self.con=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.connect((addr,port))
		print "Conntected"
	def Send(self,data):
		if type(data)==str:
			self.con.send("jerryadmin%s2"%data)
		elif type(data)==dict:
			self.con.send("jerryadmin%s2"%json.dumps(data))
		recv=self.con.recv(65536)
		return self.handle(recv)
	def handle(self,recv):
		if "jerryadmin" == recv[:10] and (["{","}"] == [recv[10], recv[-2]] or ["[","]"] == [recv[10], recv[-2]]):
			a=json.loads(recv[10:-1])
			return a
		else:
			print recv
			print "Invalid Return."
			return False
		self.con.close()

def c():
	while True:
		c=C()
		c.connect(addr="127.0.0.1")
		print c.Send({"method":"openPort"})
		break
def s():
	s=S()
	s.listen()
s()

