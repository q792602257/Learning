import socket
import json
from time import sleep
import threading

SERVER_PART=True
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
	retu=data_type+"\r\ns-p-l-i-t\r\n"+data+"\r\nE-N-D"
	retu=retu.encode()
	return retu

def recv(con,wait=False):
	data=b''
	while True:
		if wait:
			print("Here")
			while True:
				tmp = con.recv(1024)
				if tmp!=b'':
					wait=False
					data+=tmp
					break
				else:
					continue
		else:
			print("Here")
			tmp = con.recv(1024,)
			print(tmp)
			if tmp!=b'':
				data+=tmp
			else:
				break
	data_type,data=divide_data(data)
	if not data_type:
		print("Failed On Proceed Recived DATA")
	else:
		print("[Recv][%4s]%s"%(data_type,data))
	return data

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

def handle(data):
	print("[Hndl]%s"%data)

def server_ok_response(con):
	data = build_data("SERV","OK")
	print("[Send][SERV]OK")
	con.send(data)

def comminucation(con):
	if SERVER_PART:
		data=recv(con)
		server_ok_response(con)
	else:
		send(con,"OK")
		sleep(1)
		recv(con,True)
		server_ok_response(con)

if __name__=="__main__":
	if SERVER_PART:
		s=socket.socket()
		s.bind((ADDR,PORT))
		print("Listen to localhost:8888")
		while True:
			con,addr=s.accept()
			print("<---%15s:%-5d----"%(addr[0],addr[1]))
			threading.Thread(target=comminucation,args=(con,))
	else:
		con = socket.socket()
		con.connect((ADDR, PORT))
		print("----%15s:%-5d--->" % (ADDR, PORT))
		threading.Thread(target=comminucation,args=(con,))
