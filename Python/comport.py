#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import serial
import array
import binascii
import socket

class cardReader():
	verified=False
	selectCard=False
	autoFound=True
	beep=True
	error=False
	t=False
	def connect(self,port="com3",bitrate=9600,timeout=5):
		print "[INFO][CONN] %s"%(port),
		try:
			self.t=serial.Serial(port,9600,timeout=15)
			print "OK"
			return True
		except serial.serialutil.SerialException as e:
			print "Fail"
			self.error=True
			print e
			return False
	def turnBeep(self,to=False):
		print "[INFO][Beep] Turn",
		if to:
			print "ON"
			self.send("0104")
		else:
			print "OFF"
			self.send("0105")
		self.beep=to
		print "[INFO][Beep] OK"
	def turnAFount(self,to=False):
		print "[INFO][aFdC] Turn",
		if self.autoFound:
			print "ON"
			self.send("0103")
		else:
			print "OFF"
			self.send("0101")
		self.autoFound=to
		print "[INFO][aFdC] OK"
	def datasHandler(self,data):
		data=int2hex(len(data.decode("hex"))+1,4)+data
		cs=checksum(data)
		data+=cs
		data=("55550000%s"%data)
		print "[COMp][SEND] %s"%data
		return data.decode("hex")
	def datarHandler(self,info):
		info = info.encode("hex")
		print info
		if info[:8]=="55550000":
			length=int(info[8:12],16)
			if len(info[12:].decode("hex"))==length:
				if length==2:
					if info[12:14]=="00":
						return True
					elif info[12:14]=="01":
						return False
					else:
						print "[ERRO][RcvH] Status Code: %s"%info[12:14]
						return False
				else:
					return info[12:-2]
			else:
				print "[ERRO][RcvH] Length Not Match\n%s"%info
		else:
			print info
			return False
	def send(self,data="0104"):
		data=data.replace(" ","")
		if len(data)==0:
			return False
		if not self.error:
			if not self.t:
				self.connect()
				if not self.t:
					sys.exit()
			self.t.flushOutput()
			print "[INFO][SEND] %s"%data
			data=self.datasHandler(data)
			self.t.write(data)
			return self.read()
		else:
			print "[ERRO][SEND] Detected ERROR"
			return False
	def read(self):
		print "[COMp][RECV]",
		n=0
		while n==0:
			n = self.t.inWaiting()
			info=self.t.read(n)
		return self.datarHandler(info)
	def verifyToken(self,token,where,ttype="A")
		token=token.replace(" ","")
		print "[INFO][VFTK] @%s/%s %s"%(where,ttype,token)
		if not self.selectCard:
			self.selectCard=self.complexSelectCard()
		where = int2hex(where)
		if self.verified != where:
			if ttype=="A":
				tData="60"
			elif ttype=="B":
				tData="61"
			if self.selectCard:
				info = self.send("030100%s00%s%s"%(where,tData,token))
				if info:
					print "[INFO][VFTK] @%s/%s %s OK"%(where,ttype,token)
					self.verified=where
					return True
				else:
					return False
			else:
				print "[INFO][VFTK] Find NO Card"
	def complexSelectCard(self):
		print "[INFO][cSLC] Start"
		self.turnBeep()
		self.turnAFount()
		info = self.send("0204")
		print "[INFO][cSLC]",
		if info:
			print "ID: %s"%info
			self.selectCard=info
			return info
		else:
			print "Fail"
			return False
	def getCardInfo(self):
		info = self.send("0102")
		if info:
			cT=info[:2]
			cardID=info[2:]
			if cT=="04":
				return "%s\tS50"%(cardID)
			elif cT=="02":
				return "%s\tS70"%(cardID)
		else:
			return "Unknown"
	def readData(self,where,part=0):
		if self.verified == where:
			info = self.send("")
			if info :
				pass
		return False
	def writeData(self,where,part,data):
		if len(data.decode("hex"))==16:
			if self.verified == where:
				self.send("")
				pass
				return True
		return False
	def cashRead(self,where):
		pass
	def cashAdd(self,where,amount):
		pass

def int2hex(h,length=0):
	if type(h)==int:
		s=hex(h)[2:]
	else:
		s=hex(int(h,16))[2:]
	if len(s) % 2:
		s="0"+s
	while len(s)<length:
		s="00"+s
	return s	
def checksum(data):
	n=0
	s=int(data[n:n+2],16)
	n+=2
	while n+2<=len(data):
		d1=int(data[n:n+2],16)
		s^=d1
		n+=2
	return int2hex(s)

a=cardReader()
a.complexSelectCard()
a.verifyToken("FFFFFFFFFFFF",14,"A")
a.turnAFount()
a.turnBeep()

# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
