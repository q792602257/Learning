#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os , urllib , glob
import sys , json , http.cookiejar
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

opener = requests.Session()
opener.cookies = http.cookiejar.MozillaCookieJar()
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0','Connection': 'keep-alive',}

def getHTML(url):
	global opener
	global headers
	page = opener.get(url,headers=headers,timeout=10)
	html = page.text
	return html.encode(page.encoding)

def findDlink(url):
	html = getHTML(url)
	soup = BeautifulSoup(html,"html.parser")
	return "http://f.wanfangdata.com.cn/%s"%soup.select('p > a')[0]['href']

def Downloader(url,name):
	global opener
	global headers
	page = opener.get(url,headers=headers,timeout=10)
	content = page.content
	f=open("pdf1/%s.pdf"%name,"wb")
	print "%s.pdf Downloaded"%name
	f.write(content)
	f.close

def wanfang(url):
	html = getHTML(url)
	soup=BeautifulSoup(html,"html.parser")
	for i in soup.select('.qkcontent_ul > li'):
		url = i.select('a.qucontent_pdfimg')[0]['href']
		name = i.select('a.qkcontent_name')[0].get_text()
		Downloader(findDlink(url),name)

def cqvip(url):
	print getHTML("http://www.cqvip.com/ajax/html.aspx?action=upld&lf=1")
	html = getHTML(url)
	soup=BeautifulSoup(html,"html.parser")
	for i in soup.select('ul > li > em > a'):
		durl = "http://www.cqvip.com/main/confirm.aspx?id=%s"%i['href'].split("/")[-1].split('.')[0]
		name = i.get_text()
		soup = BeautifulSoup(getHTML(durl),'html.parser')
		Downloader(soup.select('ul.getfile > li > a')[0]['href'],name)

for j in range(1,7):
	for i in range(1,7):
		print "\t201%s -- %s"%(j,i)
		cqvip("http://www.cqvip.com/QK/96654X/201%s0%s"%(j,i))
		wanfang("http://c.wanfangdata.com.cn/periodical/lskjyjj/201%s-%s.aspx"%(j,i))
