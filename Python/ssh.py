#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pexpect,re,sys
reload(sys)
sys.setdefaultencoding("utf8")

class ssh():
	MultiMode=False
	countServer=0
	sshList=[]
	headers=[]
	def ServerAdd(self,ipOrDict,port="22",passwd="root"):
		if type(ipOrDict)==list:
			self.MultiMode=True
			return self.MultiServerHandle(ipOrDict)
		elif type(ipOrDict)==str:
			self.MultiMode=False
			self.headers.append("%s:%s"%(ipOrDict,port))
			if self.sshlogin(ipOrDict,port,passwd):
				self.sshList.append(self.ssh)
				return 0
			else:
				return False
	def MultiServerHandle(self,sdict):
		ret=[]
		for i in sdict:
			self.headers.append("%s:%s"%(i["ip"],i["port"]))
			if self.sshlogin(i["ip"],i["port"],i["passwd"]):
				self.sshList.append(self.ssh)
				ret.append(self.countServer)
			else:
				self.sshList.append(False)
				ret.append("%s:%s"%(i["ip"],i["port"]))
			self.countServer+=1
		return ret
	def sshlogin(self,ip,port,passwd):
		header="%s:%s"%(ip,port)
		self.ssh = pexpect.spawn('ssh root@%s -p %s'%(ip,port))
		print "%s\tConnecting"%(header)
		try:
			i = self.ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=8)
			if i==1:
				self.ssh.sendline("yes\n")
				self.ssh.expect("password:")
			self.ssh.sendline(passwd)
			if self.ssh.expect(['#'], timeout=5)==0:
				print "%s\tLogin Success"%(header)
				return True
			else:
				print "%s\tLogin Fail"%(header)
		except pexpect.exceptions.EOF:
			print "%s\tERROR@Login:\tDisconnected"%(header)
			return False
		except pexpect.exceptions.TIMEOUT:
			print "%s\tERROR@Login:\tTimeout"%(header)
			return False
	def execcmd(self,command,No=0):
		if not self.MultiMode:
			No=0
		else:
			if self.sshList[No]:
				self.commands=[]
				header=self.headers[No]
				if type(command)==list:
					for cmd in command:
						self.commands.append(cmd)
						print "%s\tExec: \t%s"%(header,cmd),
						self.sshList[No].sendline(cmd)
						print "\tExec OK"
				elif type(command)==str:
					self.commands.append(command)
					print "%s\tExec: \t%s"%(header,command),
					self.sshList[No].sendline(command)
					print "\tExec OK"
	def Exit(self,No):
		if self.sshList[No]:
			self.sshList[No].sendline("exit")
			return self.Result(No)
	def Result(self,No):
		res=[]
		command=self.commands
		r=self.sshList[No].read()
		self.sshList[No]=False
		if type(command)==list:
			for cmd in command:
				tres={}
				tres["command"]=cmd
				tres["result"]=re.findall(re.compile(" %s\r\n(.+?)\x1b"%cmd,re.S),r)[0].strip("\r\n")
				res.append(tres)
		elif type(command)==str:
				tres={}
				tres["command"]=cmd
				tres["result"]=re.findall(re.compile(" %s\r\n(.+?)\x1b"%cmd,re.S),r)[0].strip("\r\n")
				res.append(tres)
		return res
def Monitor():
	s=ssh()
	command=["uname -r","cat /etc/issue","uptime","free -m","ls|grep grep|grep -v grep"]
	serverList=[
	{"ip":"www.jerryyan.top","port":2257,"passwd":"Bd960912"},
	{"ip":"www.himei.top","port":1123,"passwd":"CC1123yhq"},
	]
	for i in s.ServerAdd(serverList):
		if type(i)==int:
			s.execcmd(command,i)
			print s.Exit(i)
		else:
			print "%s\tThe Server Has Failed."%i
Monitor()
