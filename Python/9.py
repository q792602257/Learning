#!
# -*- coding=utf-8 -*-
import socket , sys , os

#-*- coding: utf-8 -*-
from socket import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

HOST=''
PORT=8080
BUFSIZ=1024
ADDR=(HOST, PORT)
sock=socket(AF_INET, SOCK_STREAM)

sock.bind(ADDR)

sock.listen(5)
while True:
    print('waiting for connection')
    tcpClientSock, addr=sock.accept()
    print('connect from ', addr)
    while True:
        try:
            data=tcpClientSock.recv(BUFSIZ)
        except:
            print(e)
            tcpClientSock.close()
            break
        if not data:
            break
        s='Hi,you send me\t\t %s' %(data)
        tcpClientSock.send(s)
        print(data)
tcpClientSock.close()
sock.close()
