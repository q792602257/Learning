#!/usr/bi/pythonenv python
# coding:utf8
import socket
import os
import sys
import json
import MySQLdb
import glob
reload(sys)
sys.setdefaultencoding("utf8")

class MySQL():
	def SQLCon(self):
		self.conn= MySQLdb.connect(
			host='59.110.234.236',
			port = 3306,
			user='root',
			passwd='cc1123yhq',
			db ='Images',
			charset="utf8",
			)
		self.sql=self.conn.cursor()
	def SQLDel(self,where):
		self.SQLCon()
		self.sql.execute('DELETE FROM `eh` where %s'%where)
		self.sql.close()
		self.conn.commit()
		print "MySQL Del OK"
		self.conn.close()
	def SQLAdd(self,col,val):
		self.SQLCon()
		self.sql.execute('INSERT INTO `eh` (%s) VALUES (%s)'%(col,val))
		print "MySQL Add OK"
		self.sql.close()
		self.conn.commit()
		self.conn.close()
		return True
	def SQLQuery(self,col,where):
		self.SQLCon()
		a = self.sql.execute('select %s from `eh` %s'%(col,where))
		data=self.sql.fetchall()
		self.sql.close()
		self.conn.commit()
		self.conn.close()
		return data
	def SQLUpdate(self,col,val,id):
		self.SQLCon()
		sql=""
		j=0
		for i in col.split(","):
			sql="%s `%s`=%s,"%(sql,col.split(",")[j],val.split(",")[j])
			j+=1
		sql=sql.strip(",")	
		self.sql.execute('UPDATE `eh` SET %s where id=%s'%(sql,id))
		print "MySQL Upd OK"
		self.sql.close()
		self.conn.commit()
		self.conn.close()
		return True

class Server():
	prePath=r"eH/"
	def Listen(self,addr="0.0.0.0",port=22):
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
		recv=recv.split("\r\n",2)
		print "RECV:\t%s"%recv[2]
		if recv[0]=="jerryyan":
			if recv[1]=="JSON":
				self.jsonHandler(recv[2])
				return True
			elif recv[1]=="STR":
				pass
			elif recv[1]=="FALSE":
				pass
			elif recv[1]=="TRUE":
				pass
			elif recv[1]=="FILE":
				name=recv[2].split("\r\n",1)[0]
				data=recv[2].split("\r\n",1)[1]				
		self.Send("Please Use Software to Access This API")
	def jsonHandler(self,jd):
		try:
			data=json.loads(jd)
			if data["method"]=="downImg":
				self.imgDown(data["file"])
			elif data["method"]=="getStat":
				self.getStat(data["arg"])
			elif data["method"]=="getprePath":
				self.Send(self.prePath)
			elif data["method"]=="getInfo":
				self.getInfo(data["id"])
			elif data["method"]=="getFiles":
				self.getFiles(data["id"])
			elif data["method"]=="finishDown":
				self.finDown(data["id"])
		except Exception as e:
			print e
			self.Send("False")
			return False
	def finDown(self,id):
		MySQL().SQLUpdate("d","1",id)
		self.Send("True")
	def getFiles(self,id):
		files=glob.glob(os.path.join(self.prePath,str(id),"*.jpg"))
		self.Send(files)
	def getInfo(self,id):
		data=MySQL().SQLQuery("id,catagory,title","where id=%d"%id)
		self.Send(data)
	def imgDown(self,file):
		if os.path.isfile(file):
			f=open(file,"rb")
			self.Send(f)
		else:
			self.Send("False")
	def getStat(self,arg=0):
		if arg==1:
			data = MySQL().SQLQuery("id","where d=1")
		elif arg==0:
			data = MySQL().SQLQuery("id","where d=0")
		else:
			self.Send("False")
			return False
		self.Send(data)
	def Send(self,data):
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
			print "DATA ERROR:\t%s"%data
			return False
		print "TYPE:\t%s"%(ty)
		try:
			self.con.sendall("%s\r\n%s\r\n"%("jerryyan",ty))
			self.con.sendall(data)
		except Exception as e:
			print e
		finally:
			self.con.close()
	def Exit(self,*args):
		self.s.close()
		sys.exit()
s=Server()
s.Listen()