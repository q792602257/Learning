# -*- coding:utf8 -*-
import socket
import requests
import sys
import threading
from http.cookiejar import MozillaCookieJar
reload(sys)
sys.setdefaultencoding("utf8")

opener=requests.Session()
opener.cookies=MozillaCookieJar()

def getHTML(url,method="GET",headers=None,data=None):
	if method=="GET":
		page=opener.get(url,headers=headers)
	elif method=="POST":
		page=opener.post(url,headers=headers,data=data)
	else:
		return None
	rcode=page.status_code
	rheader=page.headers
	rcontent=page.content
	return rcode,headerHandle(rheader),rcontent

def urlHandle(url):
	if url.startswith("http"):
		return url
	elif url.startswith("/"):
		return "https://tieba.baidu.com%s"%url

def headerHandle(rh):
	try:
		rh.pop("Content-Encoding")
		if rh["Transfer-Encoding"]:
			rh["Transfer-Encoding"]='identity'
	except KeyError:
		pass
	rheader=""
	for key in rh:
		rheader +="%s: %s\r\n"%(key,rh[key])
	return rheader

def dataHandle(recv):
	a=recv.pop(0).split()
	method= a[0]
	url=urlHandle(a[1])
	header={}
	while len(recv)>0:
		j=recv.pop(0)
		if len(j)!=0:
			j=j.split(": ",1)
			header[j[0]]=j[1]
		else:
			break
	data="\r\n".join(recv)
	rsc,rh,rc=getHTML(url,method,header,data)
	print rsc
	print rh
	return "%s %s OK\r\n%s\r\n%s"%(a[2],rsc,rh,rc)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1",880))
s.listen(5)
while True:
	conn,addr=s.accept()
	recv=conn.recv(131072).replace("http://127.0.0.1:880","https://passport.baidu.com")
	print recv
	if len(recv)!=0:
		ret=dataHandle(recv.split("\r\n"))
		conn.send(ret)
	conn.close()
