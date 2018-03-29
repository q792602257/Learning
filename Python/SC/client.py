import socket
import json
from time import sleep
import threading

class MySC:

	def __init__(self,SERVER_PART = False,ADDR = "127.0.0.1",PORT = 8888):
		self.SERVER_PART=SERVER_PART
		self.ADDR=ADDR
		self.PORT=PORT
		if SERVER_PART:
			self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.s.bind((self.ADDR,self.PORT))
			self.s.listen()
			print("Listen to localhost:8888")
			while True:
				self.con,self.addr=self.s.accept()
				print("<---%15s:%-5d----"%(self.addr[0],self.addr[1]))
				threading.Thread(target=self.comminucation,args=(self.con,)).start()
		else:
			self.con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.con.connect((ADDR, PORT))
			print("----%15s:%-5d--->" % (ADDR, PORT))
			threading.Thread(target=self.comminucation,args=(self.con,)).start()

	def send(self,con,data):
		data_type=None
		if type(data)==str:
			data_type="str"
		elif type(data)==bool:
			data_type = "bool"
			if data:
				data="T"
			else:
				data="F"
		elif type(data) == dict or type(data) == list or type(data) == tuple:
			data_type = "json"
			data=json.dumps(data)
		print("[Send][%4s]%s"%(data_type,data))
		data=self.build_data(data_type,data)
		con.send(data)

	@staticmethod
	def build_data(data_type,data):
		retu=data_type+"\r\ns-p-l-i-t\r\n"+data+"\r\nE-N-D"
		retu=retu.encode()
		return retu

	def recv(self,con,wait=False):
		data=b''
		while True:
			if wait:
				while True:
					tmp = con.recv(1024)
					if tmp!=b'':
						wait=False
						data+=tmp
						break
					else:
						continue
			else:
				tmp = con.recv(1024,)
				if tmp!=b'':
					data+=tmp
				else:
					break
			break
		data_type,data=self.divide_data(data)
		if not data_type:
			print("Failed On Proceed Recived DATA")
		else:
			print("[Recv][%4s]%s"%(data_type,data))
		if data_type=="Clnt" and data=="OK":
			return "DISCONNECT"
		return data

	@staticmethod
	def divide_data(data):
		data=bytes.decode(data)
		data = data.split("\r\nE-N-D", 1)[0]
		data_array = data.split("\r\ns-p-l-i-t\r\n", 1)
		if len(data_array)!=2:
			print(data_array)
			return False,False
		else:
			if data_array[0]=='bool':
				if data_array[1]=="T":
					retu=True
				else:
					retu=False
			elif data_array[0]=='json':
				try:
					retu = json.loads(data_array[1])
				except:
					retu = None
			else:
				retu = data_array[1]
			return data_array[0],retu

	def handle(self,data):
		print("[Hndl]%s"%data)

	def server_ok_response(self,con):
		data = self.build_data("SERV","OK")
		print("[Send][SERV]OK")
		con.send(data)

	def client_ok_response(self,con):
		data = self.build_data("Clnt","OK")
		print("[Send][Clnt]OK")
		con.send(data)

	def comminucation(self,con):
		if self.SERVER_PART:
			while True:
				data=self.recv(con,True)
				# server_ok_response(con)
				if data=="DISCONNECT":
					print("Disconnect")
					break
				else:
					self.send(con,"123123")
					continue
		else:
			self.send(con,False)
			sleep(1)
			data=self.recv(con,True)
			self.send(con,True)
			data=self.recv(con,True)
			self.client_ok_response(con)

MySC()