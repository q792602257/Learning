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
	def verifyToken(self,token,where,ttype="A"):
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
	def complexReadData(self,where,part,ttype='A',token='FFFFFFFFFFFF'):
		print "[INFO][cRdC] Start"
		where=int2hex(where)
		part=int2hex(part)
		token=token.replace(" ","")
		if not self.selectCard:
			self.complexSelectCard()
		if len(token)!=12:
			print "[ERRO][cRdC] Token isnt Vaild : %s"%token			
			return False
		if ttype=='A':
			tD='60'
		elif ttype=='B':
			tD='61'
		else:
			return False
		info = self.send("03070000%s%s%s%s"%(where,part,tD,token))
		print "[INFO][cRdC] @%s+%s : %s"%(where,part,info)
		return info
	def complexWriteData(self,data,where,part,ttype='A',token='FFFFFFFFFFFF'):
		print "[INFO][cWrC] Start"
		data=data.replace(" ","")
		if len(data)!=32:
			print "[ERRO][cWrC] Data isnt Vaild : %s"%data
			return False
		where=int2hex(where)
		part=int2hex(part)
		token=token.replace(" ","")
		if not self.selectCard:
			self.complexSelectCard()
		if len(token)!=12:
			print "[ERRO][cWrC] Token isnt Vaild : %s"%token
			return False
		if ttype=='A':
			tD='60'
		elif ttype=='B':
			tD='61'
		info = self.send("03070100%s%s%s%s%s"%(where,part,tD,token,data))
		print "[INFO][cWrC] @%s+%s :"%(where,part),
		if info:
			print "Success"
		else:
			print "Fail"
		return info
	def cashRead(self,where,part,ttype='A',token='FFFFFFFFFFFF'):
		where=int2hex(where)
		part=int2hex(part)
		if self.verified!=where:
			self.verifyToken(token,where,ttype)
		info = self.send("030500%s%s"%(where,part))
		return info
	def cashAdd(self,amount,where,part,ttype='A',token='FFFFFFFFFFFF'):
		where=int2hex(where)
		part=int2hex(part)
		if self.verified!=where:
			self.verifyToken(token,where,ttype)
		info = self.send("03060100%s%s%s"%(where,part,amount))
		return info
	def cashDel(self,amount,where,part,ttype='A',token='FFFFFFFFFFFF'):
		where=int2hex(where)
		part=int2hex(part)
		if self.verified!=where:
			self.verifyToken(token,where,ttype)
		info = self.send("03060200%s%s%s"%(where,part,amount))
		return info
	def cashInit(self,default,where,part,ttype='A',token='FFFFFFFFFFFF'):
		where=int2hex(where)
		part=int2hex(part)
		if self.verified!=where:
			self.verifyToken(token,where,ttype)
		info=self.send("030400%s%s%s"%(where,part,default))
		return info

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
def big2small(data,force=False):
	if type(data)==int:
		data=int2hex(data,8)
	elif type(data)==str and (not force):
		return data
	elif type(data)==str and (force):
		data=int2hex(data,8)
	if len(data)%2 or len(data)>8:
		print "[ERRO][BtoS] InVaild Data : %s"%data
		return False
	ret=''
	for j in range(4):
		ret=data[j*2:j*2+2]+ret
	return ret
a=cardReader()
a.complexSelectCard()
a.complexReadData(11, 1, 'B', '59687E737241')

a.turnAFount(True)
a.turnBeep(True)
# print big2small(4350)
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
