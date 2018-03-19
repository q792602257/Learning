#!/usr/bin/env python
# coding:utf8
import socket
import os
import sys
import json
reload(sys)
sys.setdefaultencoding("utf8")

class Client():
	prePath="/sdcard/eH"
	rprePath=False
	def Connect(self,addr="59.110.234.236",port=22):
		"""
		链接服务器
		"""
		self.con=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.con.connect((addr,port))
		print ("Conntected")
	def Send(self,data):
		"""
		发送数据
		"""
		if type(data)==int:
			ty="INT"
			data=str(data)
		elif type(data)==list or type(data)==tuple or type(data)==dict:
			ty="JSON"
			data=json.dumps(data)
		elif type(data)==str:
			if data=="False":
				ty="FALSE"
				data=""
			elif data=="True":
				ty="TRUE"
				data=""
			else:
				ty="STR"
		elif type(data)==float:
			ty="FLOAT"
			data=str(data)
		elif type(data)==file:
			ty="FILE\r\n%s"%(data.name)
			data=data.read()
		else:
			print ("DATA ERROR:\t%s"%data)
			return False
		print ("Send:\t%s\t%s"%(ty,data))
		self.con.send("jerryyan\r\n%s\r\n%s"%(ty,data))
		return self.Recive()
	def Recive(self):
		"""
		获取所有数据
		"""
		recv=""
		t=self.con.recv(1024)
		while t:
			recv+=t
			t=self.con.recv(1024)
		return self.handler(recv)
	def handler(self,recv):
		"""
		获取的数据处理
		"""
		recv=recv.split("\r\n",2)
		print ("Recv:\t%s\t%s"%(recv[1],len(recv[2])))
		if recv[0]=="jerryyan":
			if recv[1]=="JSON":
				data = self.jsonHandler(recv[2])
				return data
			elif recv[1]=="STR":
				return recv[2]
			elif recv[1]=="FALSE":
				return False
			elif recv[1]=="TRUE":
				return True
			elif recv[1]=="FILE":
				name=recv[2].split("\r\n",1)[0]
				data=recv[2].split("\r\n",1)[1]
				# self.fileHandler(name,data)
				return name,data
		else:
			print ("InVaild Recive data")
	def jsonHandler(self,jd):
		try:
			data=json.loads(jd)
			return data
		except Exception as e:
			return False
	def fileHandler(self,name,data):
		"""
		写文件
		"""
		path,Name=self.filenameHandler(name)
		path=os.path.join(self.prePath,path)
		if not os.path.isdir(path):
			os.makedirs(path)
		f=open(os.path.join(path,Name),"wb")
		f.write(data)
		f.close
	def filenameHandler(self,name):
		"""
		处理服务器的路径
		变成相对文件名
		"""
		pd,fn=os.path.split(name)
		dd,dr=os.path.split(pd)
		return dr,fn
	def queryAll(self,arg=0):
		"""
		查询未下载完成的所有id
		arg=1为已下载的所有id
		"""
		self.Connect()
		all=self.Send({"method":"getStat","arg":arg})
		return all
	def getInfo(self,id):
		"""
		获取id的详情信息
		"""
		self.Connect()
		if type(id)==str:
			return False
		info=self.Send({"method":"getInfo","id":id})
		return info
	def getFiles(self,id):
		"""
		获取对应id的图片文件路径
		"""
		self.Connect()
		if type(id)==str:
			return False
		info=self.Send({"method":"getFiles","id":id})
		return info
	def downImg(self,name):
		"""
		下载文件，相对路径或绝对路径
		"""
		self.Connect()
		data=self.Send({"method":"downImg","file":name})
		return data
	def finDown(self,id):
		"""
		标记已下载完成
		"""
		self.Connect()
		data=self.Send({"method":"finishDown","id":id})
		return data
c=Client()
all=c.queryAll()
for i in all:
	print (c.getInfo(i[0]))
	break
file= c.getFiles(i[0])
for j in file:
	fn,data=c.downImg(j)
	c.fileHandler(fn,data)
c.finDown(i[0])
