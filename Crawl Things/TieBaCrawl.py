# -  *  - coding:utf8 -  *  - 
import requests
import re
import json, threading
import os
import sys
from urllib import quote, unquote
from bs4 import BeautifulSoup as Soup
from http.cookiejar import MozillaCookieJar
import time
reload(sys)
sys.setdefaultencoding('utf-8')

opener = requests.Session()
opener.cookies = MozillaCookieJar()
threadList = []
lock = threading.Lock()
tielist = []

def getHTML(url):
		global opener
		headers =  {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0', "Connection":"Keep-Alive", }
		try:
			page = opener.get(url, headers = headers, timeout = 10)
			html = page.text
			return html.encode("utf8")
		except Exception as e:
			#print u'\t 失败,先休息一会在来吧'
			#print url
			print e

def tRun():
	global threadList
	for i in threadList:
		threadList.pop().start()

def tAdd(Func, Args):
	global threadList
	t = threading.Thread(target = Func, args = Args)
	threadList.append(t)
	tRun()

def hrefHandle(href):
	if href.startswith("http"):
		return href
	else:
		return "https://tieba.baidu.com%s"%href

def tiebaListHandle(thtml):
	a = re.findall('"frs-list/pagelet/thread_list", ({.+})\).then', thtml)[0]
	b = json.loads(a)["content"]
	return b

def tieHandle(html):
	soup = Soup(html, "html.parser")
	ret = []
	for j in soup.select("div.j_threadlist_li_right"):
		t =  {}
		t["title"] = j.select("a.j_th_tit")[0].get_text()
		t["link"] = hrefHandle(j.select("a.j_th_tit")[0]["href"])
		t["sendUser"] = j.select("a.j_user_card")[0].get_text()
		t["sendTime"] = j.select("span.is_show_create_time")[0].get_text().strip()
		t["sendUserUrl"] = hrefHandle(j.select("a.j_user_card")[0]["href"])
		try:
			t["lreplyUser"] = j.select("a.j_user_card")[1].get_text()
			t["lreplyTime"] = j.select("span.threadlist_reply_date")[0].get_text().strip()
			t["lreplyUserHref"] = hrefHandle(j.select("a.j_user_card")[1]["href"])
		except IndexError:
			pass
		ret.append(t)
	return ret

def tieba(ba = "铁扇公主", timestamp = time.time(), page = 1, interval = 5):
	global tielist
	global lock
	for i in range(page):
		thtml = tiebaListHandle(getHTML("https://tieba.baidu.com/f?kw=%s&ie=utf-8&pn=%s&pagelets=frs-list/pagelet/thread&kpagelets_stamp=%.f"%(ba,i*50,float(timestamp*1000))).replace("\\\\",'\\').replace("\\(","("))
		tlist = tieHandle(thtml)
		lock.acquire()
		tielist.extend(tlist)
		lock.release()

def getTieInfo(link = None):
	if link:
		while True:
			soup = Soup(getHTML(link), "html.parser")
			for i in soup.select("div.l_post"):
				if len(i.select("div.d_badge_lv")) != 0:
					print i.select("a.p_author_name")[0].get_text().strip()
					print i.select("div.d_badge_lv")[0].get_text()
					print i.select("div.d_post_content")[0].get_text()
			b = soup.select(".pb_list_pager")[0].find("a", text = "下一页")
			if b:
				link = hrefHandle(b["href"])
				print link
			else:
				print "end"
				break
	else:
		for i in tielist:
			link = i["link"]
			print i["title"]
			while True:
				soup = Soup(getHTML(link), "html.parser")
				for i in soup.select("div.l_post"):
					if len(i.select("div.d_badge_lv")) != 0:
						print i.select("span.tail-info")[-2].get_text()
						print i.select("span.tail-info")[-1].get_text()
						print i.select("a.p_author_name")[0].get_text().strip()
						print i.select("div.d_badge_lv")[0].get_text()
						print i.select("div.d_post_content")[0].get_text()
						print
				b = soup.select(".pb_list_pager")[0].find("a", text = "下一页")
				if b:
					link = hrefHandle(b["href"])
					print link
				else:
					print "end"
					break
			
def emgjhk():
	getHTML("http://shop.emgjhk.com")
getHTML("https://tieba.baidu.com")
tieba(page = 1)
getTieInfo()
