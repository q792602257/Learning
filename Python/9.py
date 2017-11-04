#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib2 , re , requests , os , urllib , glob , MySQLdb
import sys , json , http.cookiejar , time , threading
from bs4 import BeautifulSoup
import signal
reload(sys)
sys.setdefaultencoding('utf8')

def proxyGet(prox=None):
	print 'Getting Proxy'
	url="http://www.66ip.cn/nmtq.php?getnum=1&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"
	head = {
		'Cache-Control':'no-cache',
		'Connection':'keep-alive',
		'Referer':'http://www.66ip.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}
	page=requests.get(url,headers=head,timeout=15,proxies=prox)
	page.encoding="gbk"
	html=page.text
	m=re.findall(r"((\d{1,3}\.){3}\d{1,3}:\d{1,5})",html)
	try:
		print 'Proxy :\t%s'%m[0][0],
		ret={"http":"http://"+m[0][0],
			"https":"http://"+m[0][0]}
		return ret
	except Exception as e:
		print e
		return proxyGet(prox)

def getValidProxy(prox=None):
	proxy=proxyGet(prox)
	url="https://www.e-hentai.org"
	try:
		page=requests.get(url,proxies=proxy,timeout=10,verify=False)
		html=page.text
		if 'Cloudflare Ray ID' in html:
			print html
			raise NameError
		print 'OK'
		return proxy
	except Exception as e:
		print e
		print 'Failed'
		time.sleep(1)
		return getValidProxy(prox)

class code509(Exception):
	def __init__(self):
		self.value='code509 Bandwith Exceed'
	def __str__(self):
		exit()
		return repr(self.value)
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
class eHentai(MySQL):
	page=0
	url=''
	q=0
	proxy=None
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
		page= self.opener.post(url,data=data,headers=self.headers,proxies=self.proxy)
		if page.text.find("yxzyxz123456") >= 0:
			print "login Success"
			return True
		else:
			print "Login Failed"
			return False
	def getHtml(self,url):
		try:
			page=self.opener.get(url,headers=self.headers,proxies=self.proxy,timeout=20)
			page.encoding="utf-8"
			html = page.text
			if 'Cloudflare Ray ID' in html:
				print html
				raise NameError
			return html
		except Exception as e:
			print e
			self.proxy=getValidProxy()
			return self.getHtml(url)
	def quit(self,signal=None, frame=None):
		self.SQLUpdate("resume,url,q","1,%s,%s"%(self.url,self.q),self.id)
		sys.exit()
	def Downloader(self,url):
		if not os.path.exists(os.path.join("eH",self.id)):
			os.makedirs(os.path.join("eH",self.id))
		if not os.path.exists(os.path.join("eH",self.id,"%s.jpg"%self.q)):
			
			time.sleep(1)
			page = self.opener.get(url,headers=self.headers,timeout=15,proxies=self.proxy)
			if 'html' in page.headers["Content-Type"]:
				raise code509()
			data = page.content
			if len(data)==28658:
				raise code509()
			else:
				with open(os.path.join("eH",self.id,"%s.jpg"%self.q),"wb") as f:
					f.write(data)
					print "OK"
		else:
			print "Exist"
	def resume(self):
		res=self.SQLQuery("url,id,q,quote","where `resume`=1 order by id desc")
		for each in res:
			if each[2] and "http" in each[0]:
				print '---resume Download'
				self.q=each[2]
				self.id = str(each[1])
				self.url=each[0]
				if len(self.SQLQuery('id','where resume=0 and id={}'.format(self.id)))>0:
					print 'Exist'
					continue
				self.imgHandler(self.url)
			else:
				self.q=1
				self.id=str(each[1])
				self.url=self.imgHrefHandler(each[3])
				if self.url:
					self.imgHandler(self.url)
		print "---Complete"
	def imgHandler(self,url1):
		print "%9d"%(self.q),
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
				self.url=None
				self.q=0
				return True
		except code509:
			print 'Expected 509\nTry another Proxy'
			self.proxy=getValidProxy()
			#time.sleep(10000)
			print 'And Retry'
			self.imgHandler(self.url)
		except Exception as e:
			print "ERROR@imgH"
			print e
			# print soup.get_text()
			self.SQLUpdate("resume,url,q","1,'%s',%s"%(self.url,self.q),self.id)
			self.q=0
			self.url=None
			return False
	def listHandler(self,page=0):
		ret=[]
		self.page=page
		while True:
			print "Reading Page %d"%self.page
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
				print "Chang a Proxy"
				self.proxy=getValidProxy()
				print "And Retry"
			print "Finish Reading Threads"
			self.threadHandler(ret)
			print "Wait For 0 Minute"
			self.page+=1
			if self.page%3==2:
				self.resume()
				#self.page=0
			time.sleep(1)
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
			if not self.SQLQuery("id","where id=%s and `resume`=0"%thread['id']):
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
		print '-Starting Download'
		if len(soup.find_all(class_="gdtl")) != 0:
			url = soup.find_all(class_="gdtl")[0].select("a")[0]["href"]
			return url
		elif len(soup.find_all(class_="gdtm")) != 0:
			url = soup.find_all(class_="gdtm")[0].select("a")[0]["href"]
			return url
		else:
			self.SQLDel('id=%s'%self.id)
			print "Failed"
			return False
				
	def main(self):
		try:
			#self.proxy={'http':'http://45.62.238.199:48888',
				#'https':'http://45.62.238.199:48888'}
			self.proxy=getValidProxy()
			self.eLogin()
			self.resume()
			self.listHandler(100)
		except code509:
			print 'Excepted 509\nWait 3 Hour',
			time.sleep(9)
			print '\tAnd Retry'
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