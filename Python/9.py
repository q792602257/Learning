#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib2 , re , requests , os , urllib , glob , MySQLdb
import sys , json , http.cookiejar , time , threading
from bs4 import BeautifulSoup
import signal
reload(sys)
sys.setdefaultencoding('utf8')

class MySQL():
	def SQLCon(self):
		self.conn= MySQLdb.connect(
			host='localhost',
			port = 3306,
			user='root',
			passwd='cc1123yhq',
			db ='Images',
			charset="utf8",
			)
		self.sql=self.conn.cursor()
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
		self.sql.execute('UPDATE `eh` SET %s where `id`=%s'%(sql,id))
		print "MySQL Upd OK"
		self.sql.close()
		self.conn.commit()
		self.conn.close()
		return True
class eHentai(MySQL):
	page=0
	opener = requests.Session()
	opener.cookies = http.cookiejar.MozillaCookieJar()
	headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
			'Accept-Encoding':'gzip, deflate',
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
			"Referer": "https://e-hentai.org/",
			"Connection": "keep-alive"}
	def eLogin(self):
		# print "Start Login"
		url = "https://forums.e-hentai.org/index.php?act=Login&CODE=01"
		data= {"CookieDate":1,"UserName":"yxzyxz123456","PassWord":"yxzyxz123456"}
		page= self.opener.post(url,data=data,headers=self.headers)
		if page.text.find("yxzyxz123456") >= 0:
			print "login Success"
			return True
		else:
			print "Login Failed"
			return False
	def getHtml(self,url,data=None):
		time.sleep(5)
		page = self.opener.get(url,headers=self.headers)
		page.encoding="utf-8"
		html = page.text
		return html
	def quit(self,signal=None, frame=None):
		self.SQLUpdate("resume,url,q","1,%s,%s"%(self.url,self.q),self.id)
		sys.exit()
	def Downloader(self,url):
		if not os.path.exists(os.path.join("eH",self.id)):
			os.makedirs(os.path.join("eH",self.id))
		if not os.path.exists(os.path.join("eH",self.id,"%s.jpg"%self.q)):
			if os.path.getsize(os.path.join("eH",self.id,"%s.jpg"%self.q))=28658:
				page = self.opener.get(url,headers=self.headers,timeout=15)
				data = page.content
				with open(os.path.join("eH",self.id,"%s.jpg"%self.q),"wb") as f:
					f.write(data)
					print "OK"
			else:
				print "Exist"
		else:
			print "Exist"
	def resume(self):
		res=self.SQLQuery("url,id,q,quote","where `resume`=1")
		for each in res:
			print '----resume Download'
			self.id = str(each[1])
			if each[2]:
				self.q=int(each[2])
				self.url=each[0]
				self.imgHandler(self.url)
			else:
				self.q=1
				self.url=self.imgHrefHandler(each[3])
				if self.url:
					self.imgHandler(self.url)
				else:
					print "----Next Time"
			print "----Complete"
	def imgHandler(self,url1):
		print "%9d"%(self.q) ,
		html = self.getHtml(url1)
		soup = BeautifulSoup(html,"html.parser")
		try:
			url2 = soup.select("div#i3 > a")[0]["href"]
			if url1 != url2:
				imgu=soup.select("div#i3 > a > img")[0]["src"]
				print "Downloading...\t",
				self.Downloader(imgu)
				self.q += 1
				self.url = url2
				self.imgHandler(url2)
			else:
				print "Finish"
				self.SQLUpdate("resume,url,q","0,'',0",self.id)
				return True
		except Exception as e:
			print "ERROR"
			# print soup.get_text()
			self.SQLUpdate("resume,url,q","1,'%s',%s"%(self.url,self.q),self.id)
			print e
			return False
	def listHandler(self):
		ret=[]
		while True:
			print "Reading Page %s"%self.page
			html = self.getHtml("https://e-hentai.org/?page=%s"%self.page)
			asoup = BeautifulSoup(html,"html.parser")
			try:
				threads=asoup.select("div.ido > div > table.itg")[0].find_all(class_=re.compile("gtr."))
				for thread in threads:
					t={}
					t["cata"] = thread.select("td.itdc > a > img")[0]["alt"]
					t["title"]= thread.select("td.itd > div > div.it5 > a")[0].get_text()
					t["url"]  = thread.select("td.itd > div > div.it5 > a")[0]["href"]
					t["id"]=t["url"].split("/")[-3]
					ret.append(t)
			except IndexError:
				print html
				print "Wait 10 Min",
				sleep(600)
				print "And Retry"
			print "Finish Reading Threads"
			self.threadHandler(ret)
			print "Wait For 3 Minute\t",
			if self.page>20:
				self.page=0
			self.page+=1
			time.sleep(180)
			print "And Continue"
	def threadHandler(self,ret):
		for thread in ret:
			self.q=1
			self.id=thread["id"]
			self.title=MySQLdb.escape_string(thread["title"])
			self.cata=thread["cata"]
			print "page:%s\t%s\t%s"%(self.page,self.id,self.cata)
			print self.title
			if not self.SQLQuery("id","where `id`=%s"%thread['id']):
				self.SQLAdd("id,title,catagory,quote","%s,'%s','%s','%s'"%(self.id,self.title,self.cata,MySQLdb.escape_string(thread['url'])))
			if not self.SQLQuery("id","where `id`=%s and `resume`=0"%thread['id']):
				url = self.imgHrefHandler(thread['url'])
				if url:
					self.imgHandler(url)					
				else:
					continue
			else:
				print "Exist:\t%s\n%s"%(thread["id"],thread["title"])
				continue
	def imgHrefHandler(self,url):
		html = self.getHtml(url)
		soup = BeautifulSoup(html,"html.parser")
		if len(soup.find_all(class_="gdtl")) != 0:
			url = soup.find_all(class_="gdtl")[0].select("a")[0]["href"]
			return url
		elif len(soup.find_all(class_="gdtm")) != 0:
			url = soup.find_all(class_="gdtm")[0].select("a")[0]["href"]
			return url
		else:
			print soup.get_text()
			print "Failed"
			return False
				
	def main(self):
		self.eLogin()
		try:
			self.resume()
			self.listHandler()
		except Exception as e:
			print e
			print "\nWait 2 Minute..."
			time.sleep(120)
			print "And Retry"
			self.main()
e=eHentai()
signal.signal(signal.SIGTERM, e.quit)
signal.signal(signal.SIGINT, e.quit)
e.main()
