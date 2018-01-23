import socket
import json
from time import sleep

ADDR="127.0.0.1"
PORT=8888

def send(con,data):
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
	data=build_data(data_type,data)
	con.send(data)

def build_data(data_type,data):
	retu=data_type+"\r\ns-p-l-i-t\r\n"+data
	retu=retu.encode()
	return retu

def recv(con,wait=False):
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
			tmp = con.recv(1024)
			if tmp!=b'':
				data+=tmp
			else:
				break
	data_type,data=divide_data(data)
	if not data_type:
		print("Failed On Proceed Recived DATA")
	else:
		print("[Recv][%4s]%s"%(data_type,data))
		handle(data)

def divide_data(data):
	data=bytes.decode(data)
	data_array=data.split("\r\ns-p-l-i-t\r\n",1)
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

def handle(data):
	print("[Hndl]%s"%data)

while True:
	con=socket.socket()
	con.connect((ADDR,PORT))
	sleep(1)
	send(con,[123])
