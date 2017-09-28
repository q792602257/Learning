#!/usr/bin/python
# -*- coding:utf8 -*-
import urllib2 , re , requests , os , urllib , glob , MySQLdb
import sys , json , http.cookiejar , time , threading
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

opener = requests.Session()
opener.cookies = http.cookiejar.MozillaCookieJar()
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
		'Accept-Encoding':'gzip, deflate',
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Referer": "https://e-hentai.org/",
		"Connection": "keep-alive",}

def SQLCon():
	conn= MySQLdb.connect(
		host='localhost',
		port = 3306,
		user='root',
		passwd='cc1123yhq',
		db ='eh',
		charset="utf8",
		)
	return conn
def SQLAdd(col,val):
	conn = SQLCon()
	sql = conn.cursor()
	sql.execute('INSERT INTO `eh` (%s) VALUES (%s)'%(col,val.encode("utf-8")))
	print "MySQL Add OK"
	sql.close()
	conn.commit()
	conn.close()
	return True
def SQLQuery(col,where):
	conn = SQLCon()
	sql = conn.cursor()
	a = sql.execute('select %s from `eh` %s'%(col,where))
	data=sql.fetchall()
	sql.close()
	conn.commit()
	conn.close()
	return data
def SQLUpdate(col,val,id):
	conn = SQLCon()
	sql = conn.cursor()
	sql.execute('UPDATE `eh` (%s) VALUES (%s) where id="%s"',(%col,val.encode("utf-8"),id))
	print "MySQL Add OK"
	sql.close()
	conn.commit()
	conn.close()
	return True
def eLogin():
	global opener
	global headers
	url = "https://forums.e-hentai.org/index.php?act=Login&CODE=01"
	data= {"CookieDate":1,"UserName":"yxzyxz123456","PassWord":"yxzyxz123456"}
	page = opener.post(url,data=data,headers=headers)
	if page.text.find("yxzyxz123456") >= 0:
		print "login Success"
		return True
	else:
		print "Login Failed"
		return False
def getHtml(url,method="GET",data=None):
		global opener
		global headers
		if method == "GET":
			time.sleep(5)
			page = opener.get(url,headers=headers)
			html = page.text
		elif method == "POST":
			time.sleep(1)
			page = opener.post(url,headers=headers,data=data)
			html = page.text
		return html

def Downloader(url,name,d="./"):
	global opener
	global headers
	if not os.path.exists(os.path.join("eH",d)):
		os.makedirs(os.path.join("eH",d))
	if not os.path.exists(os.path.join("eH",d,name)):
		page = opener.get(url,headers=headers,timeout=15)
		a = page.content
		f = open(os.path.join("eH",d,name),"wb")
		f.write(a)
		f.close
def continued():
	global q
	global aid
	res=SQLQuery("url,id,q")
	for each in res:
		print 'continue Download'
		aid = each[1]
		q=int(each[2])
		url=each[0]
		imgHandler(url)
		break

def imgHandler(url1):
	global q
	global aid
	q += 1
	print "\t%s"%q
	html = getHtml(url1)
	soup = BeautifulSoup(html,"html.parser")
	try:
		url2 = soup.select("div#i3 > a")[0]["href"]
		if url1 != url2:
			Downloader(soup.select("div#i3 > a > img")[0]["src"],"%s.jpg"%q,aid,)
			imgHandler(url2)
		else:
			return True
	except Exception as e:
		print e
		return False

def eHentai(pages=1):
	global atype
	global atitle
	global aid
	global q
	try:
		for i in range(pages):
			html = getHtml("https://e-hentai.org/?page=%s"%i)
			asoup = BeautifulSoup(html,"html.parser")
			#print asoup.select("div.ido > div > table.ptt")
			for i in asoup.select("div.ido > div > table.itg")[0].find_all(class_=re.compile("gtr.")):
				q = 0
				atype = i.select("td.itdc > a > img")[0]["alt"]
				atime = i.select("td.itd")[0].get_text()
				atitle= i.select("td.itd > div > div.it5 > a")[0].get_text()
				aurl  = i.select("td.itd > div > div.it5 > a")[0]["href"]
				print atype
				print atitle
				aid = aurl.split("/")[-3]
				if SQLQuery(aid):
					html = getHtml(aurl)
					bsoup = BeautifulSoup(html,"html.parser")
					if len(bsoup.find_all(class_="gdtl")) != 0:
						burl = bsoup.find_all(class_="gdtl")[0].select("a")[0]["href"]
					elif len(bsoup.find_all(class_="gdtm")) != 0:
						burl = bsoup.find_all(class_="gdtm")[0].select("a")[0]["href"]
					else:
						print bsoup.get_text()
						continue
					if not imgHandler(burl):
						return False
				else:
					print "Exist:\t%s"%aid
	except Exception as e:
		print e
		return False
def main():
	eLogin()
	continued()
	try:
		while True:
			if not eHentai(5):
				main()
			print 'Wait Half Hour to Privent 509'
			time.sleep(1800)
	except Exception as e:
		print e
		print "\nWait 2 Minute..."
		time.sleep(120)
		print "And Retry"
		main()
main()
