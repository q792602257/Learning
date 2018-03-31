import socket
import json
from time import sleep
import threading

class MySC:

	def __init__(self,SERVER_PART = True,ADDR = "127.0.0.1",PORT = 8888):
		self.SERVER_PART=SERVER_PART
		self.ADDR=ADDR
		self.PORT=PORT
		if SERVER_PART:
			self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.s.bind((self.ADDR,self.PORT))
			self.s.listen()
			print("Listen to localhost:8888")
			while True:
				self.con,addr=self.s.accept()
				print("<---%15s:%-5d----"%(addr[0],addr[1]))
				threading.Thread(target=self.comminucation,args=(self.con,addr)).start()
		else:
			self.con = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.con.connect((ADDR, PORT))
			print("----%15s:%-5d--->" % (self.ADDR, self.PORT))
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
		elif type(data) == bytes:
			data_type = "Raw"
		print("[Send][%4s]%d Byte"%(data_type,len(data)))
		data=self.build_data(data_type,data)
		con.send(data)

	@staticmethod
	def build_data(data_type,data):
		if data_type=="Raw" and type(data)==bytes:
			retu = b"Raw\r\ns-p-l-i-t\r\n"+data+b"\r\nE-N-D"
		else:
			retu=data_type+"\r\ns-p-l-i-t\r\n"+data+"\r\nE-N-D"
			retu=retu.encode()
		return retu

	def recv(self,con):
		data=b''
		while True:
			try:
				tmp = con.recv(1024)
			except ConnectionResetError:
				return "D-I-S-C-O-O-N-E-C-T"
			data+=tmp
			if tmp.endswith(b"\r\nE-N-D"):
				break
			else:
				print("[Recving]%12d Byte"%len(data),'\b'*32+'\r')
				continue
		data_type,data=self.divide_data(data)
		if not data_type:
			print("Failed On Proceed Recived DATA")
		else:
			print("[Recv][%4s]%d Byte"%(data_type,len(data)))
		if (data_type=="Clnt" or data_type=="SERV") and data==b"OK":
			return "D-I-S-C-O-O-N-E-C-T"
		return data

	@staticmethod
	def divide_data(data):
		# data=bytes.decode(data)
		data = data.split(b"\r\nE-N-D", 1)[0]
		data_array = data.split(b"\r\ns-p-l-i-t\r\n", 1)
		try:
			data_type=bytes.decode(data_array[0])
		except:
			return False,False			
		if len(data_array)!=2:
			print(data_array)
			return False,False
		else:
			if data_array[0]==b'bool':
				data_type=bytes.decode(data_array[0])
				if data_array[1]==b"T":
					retu=True
				else:
					retu=False
			elif data_array[0]==b'json':
				data_type=bytes.decode(data_array[0])
				try:
					retu = json.loads(bytes.decode(data_array[1]))
				except:
					retu = None
			else:
				retu = data_array[1]
			return data_type,retu

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

	def comminucation(self,con,addr=[]):
		if self.SERVER_PART:
			while True:
				print("<---%15s:%-5d----"%(addr[0],addr[1]))				
				data=self.recv(con)
				# server_ok_response(con)
				if data=="D-I-S-C-O-O-N-E-C-T":
					print("Disconnect")
					break
				else:
					self.send(con,"1")
					continue
		else:
			while True:
				sleep(1)
				print("----%15s:%-5d--->" % (self.ADDR, self.PORT))	
				with open("cnn.h5","rb") as f:
					self.send(con,b"".join(f.readlines()))
				data=self.recv(con)
				if data=="D-I-S-C-O-O-N-E-C-T":
					print("Disconnect")
					break
				else:
					break
			self.client_ok_response(con)

MySC()