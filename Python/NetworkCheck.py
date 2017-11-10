import requests
import subprocess
import sys
import os
import re
import socket
from time import sleep

def reconnect():
	try:
		url = "http://192.168.1.1/device-map/wan_action.asp"
		data = "wan_action=Connect&modem_prio=1"
		header = {"Authorization":"Basic YWRtaW46YWRtaW4="}
		page=requests.post(url,data=data,headers=header)
		print ("Reconnect Wan")
		return True
	except Exception as e:
		print ("Error",e)
		return False
def wanstat():
	try:
		url = "http://192.168.1.1/status_wanlink.asp"
		header = {"Authorization": "Basic YWRtaW46YWRtaW4="}
		page=requests.get(url,headers=header)
		html=page.text
		stat = html.split("\n")[0]
		a=re.findall(r"return (\d);",stat)
		return a[0]
	except Exception as e:
		print ("Error",e)
		return False
def ping(ip,port,timeout=2):  
	try:  
		cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
		address=(str(ip),int(port))  
		status = cs.connect_ex((address))  
		cs.settimeout(timeout)
		if status != 0:
			return False
		else:
			return True	
	except Exception as e:
		print ("error:%s" %e)
		return False
laststate=0
while True:
	s = wanstat()
	sleep(5)
	if s == "0":
		laststate = 0
		if not ping("baidu.com",80,5):
			reconnect()
		sleep(5)
	elif s == "1":
		print ("Unplugged Cable")
		laststate = 1
		sleep(120)
	elif s == "7":
		print ("Disconnected")
		laststate = 7
		sleep(5)
		reconnect()
	else:
		print ("Unkown status:",s)



