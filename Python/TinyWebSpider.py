#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import re , requests , urllib , http.cookiejar
import os , sys , json , threading , webbrowser
import md5 , base64 , random , binascii , hashlib , time
import Tkinter , tkMessageBox , tkFileDialog
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
# reload(sys)
# sys.setdefaultencoding('utf8')

class GUIDemo():

	modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
			'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
			'104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
			'575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
			'3ece0462db0a22b8e7')
	nonce = '0CoJUm6Qyw8W8jud'
	pubKey = '010001'
	iss = 1
	header1 = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'music.163.com',
		'Referer': 'http://music.163.com/search/',
		'User-Agent':
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
	}

	opener = requests.Session()
	opener.cookies = http.cookiejar.LWPCookieJar()
	tMax = 5
	threads = []
	stop=False
	tCount = 0

	def __init__(self):
		self.TkInit()

	#主窗口#
	def TkInit(self):
		self.root = Tkinter.Tk()
		self.root.title("Tiny WebSpider by JerryYan")
		self.root.geometry("768x480")
		self.TkMWindow()
		self.function = [
		{
			"name":"音乐搜索",
			"func":self.Music_search,
			"stop":True,
			"args":"sthE",
			"Entry":"normal",
			"command":self.cT5,
			"dClick":self.Music_Download,
			"which":"2\t0",
			"RMenu":self.RMenu6,
		},
		{
			"name":"盘搜音乐",
			"func":self.PanSouM,
			"stop":False,
			"args":"sthE\t10",
			"Entry":"normal",
			"command":self.cT6,
			"dClick":self.browserOpen,
			"which":1,
			"RMenu":self.RMenu1,
		},
		{
			"name":"blank",
		},
		{
			"name":"热映电影",
			"func":self.HotMovies,
			"stop":True,
			"args":(4,),
			"Entry":"readonly",
			"command":self.cT0,
			"dClick":self.eSet,
			"which":0,
			"RMenu":self.RMenu0,
		},
		{
			"name":"百度云盘",
			"func":self.sousuo,
			"stop":False,
			"args":"sthE",
			"Entry":"normal",
			"command":self.cT1,
			"dClick":self.browserOpen,
			"which":1,
			"RMenu":self.RMenu2,
		},
		{
			"name":"blank",
		},
		{
			"name":"迅雷链接",
			"func":self.sousuoD,
			"stop":False,
			"args":"sthE",
			"Entry":"normal",
			"command":self.cT3,
			"dClick":self.browserOpen,
			"which":1,
			"RMenu":self.RMenu4,
		},

		]
		self.TkMBar()
		self.cT0()
		self.root.mainloop()

	def TkMWindow(self):
		self.label = Tkinter.Label(self.root,text="Jerry",font=("黑体", 16, "normal"),width=8)
		self.scrollY=Tkinter.Scrollbar(self.root)
		self.mainList = Tkinter.Listbox(self.root,font=("宋体", 14, "normal"),selectmode= "browse",yscrollcommand=self.scrollY.set,width=56)
		self.sth = Tkinter.StringVar()
		self.blank=Tkinter.Label(self.root,height=1)
		self.sthE = Tkinter.Entry(self.root,textvariable=self.sth,font=("宋体", 14, "normal"),width=56)
		self.button = Tkinter.Button(self.root,text="搜索",font=("黑体", 16, "normal"),command=self.ButtonClick)
		self.bLabel = Tkinter.Label(self.root,font=("黑体", 12, "normal"),width=80,justify="left",anchor="w")

		self.label.bind("<Button-1>", self.cT)
		self.label.bind("<Button-3>", self.changeMode)
		self.sthE.bind("<Button-3>", self.copyMenu)
		self.mainList.bind('<Double-Button-1>', self.dClick)
		self.mainList.bind("<Button-3>", self.lRkMenu)
		self.scrollY.config(command=self.mainList.yview)

		self.mainList.grid(row="2",column="0",ipadx=80,padx="0",ipady="60p",columnspan="3")
		self.label.grid(row="0",column="0",sticky="w")
		self.blank.grid(row="1",column="0")
		self.sthE.grid(row="0",column="1",sticky="nesw")
		self.button.grid(row="0",padx="0p",column="2",columnspan="2")
		self.scrollY.grid(row="2",column="3",ipady="120p",sticky="w")
		self.bLabel.grid(row="3",column="0",columnspan="3",sticky="w")

	def TkMBar(self):
		menubar = Tkinter.Menu(self.root,bg="white",font=("黑体", 16, "normal"))
		self.root.config(menu = menubar)
		self.cMode = Tkinter.Menu(self.root, tearoff=0)
		for i in self.function:
			if i["name"]=="blank":
				self.cMode.add_separator()
			else:
				self.cMode.add_command(label=i["name"], command=i["command"])
		#add_cascade
		self.others = Tkinter.Menu(self.root, tearoff=0)
		self.others.add_command(label="关于",command=self.about)
		self.others.add_command(label="反馈",command=self.suggWindow)
		menubar.add_cascade(label="切换", menu=self.cMode)
		menubar.add_cascade(label="其他", menu=self.others)
		menubar.add_command(label="退出", command=self.root.quit)

	def help(self):
		pass

	def about(self):
		tkMessageBox.showinfo(self.root,
	"""作者：\tJerryYan/开心鄢\n邮箱：\t792602257@qq.com\n版本：\tv0.0.3 Beta @17/8/16\n测试版本，请勿用作违法用途""")

	def suggWindow(self):
		self.sugg = Tkinter.Tk()
		self.sugg.title("反馈")
		self.sugg.geometry("400x200")
		self.sla = Tkinter.Label(self.sugg,text="Jerry",font=("黑体", 16, "normal"),width=28,justify="left",anchor="w")
		self.sla.bind("<Button-1>", self.suggCh)
		self.sla.grid(row="0",column="0",sticky="w")
		self.submit = Tkinter.Button(self.sugg,text="提交",font=("黑体", 16, "normal"),command=self.support,width=4)
		self.submit.grid(row="0",column="1",sticky="e")
		self.suggtext = Tkinter.Text(self.sugg,font=("宋体", 14, "normal"),width=32,height=7)
		self.suggtext.grid(row="1",column="0",columnspan="2",sticky="news")
		self.suggCh()
		self.sugg.mainloop()

	def suggCh(self,*args):
		self.iss += 1
		if self.iss == 2:
			self.sla["text"]="那必须得有意见了"
		else:
			self.iss = 1
			self.sla["text"]="那肯定是支持啦:D"


	#菜单项#
	def lRkMenu(self,event):
		self.mainList.select_clear(0,'end')
		self.mRs = self.mainList.nearest(event.y)
		self.mainList.select_set(self.mainList.nearest(event.y),)
		self.menuR = Tkinter.Menu(self.root, tearoff=0)
		self.function[self.Mode]["RMenu"]()
		self.menuR.add_separator()
		self.menuR.add_command(label="关于", command=self.about)
		self.menuR.post(event.x_root, event.y_root)

	def copyMenu(self,event):
		self.menucp = Tkinter.Menu(self.root, tearoff=0)
		self.menucp.add_command(label="复制", command=self.eCopy)
		self.menucp.add_command(label="粘贴", command=self.ePaste)
		self.menucp.add_separator()
		self.menucp.add_command(label="清空", command=self.eClear)
		self.menucp.post(event.x_root, event.y_root)

	def changeMode(self,event):
		self.cMode.post(event.x_root, event.y_root)

	#多进程#
	def tRun(self):
		for t in self.threads:
			self.tCount+=1
			t.setDaemon(True)
			t.start()
			self.threads.remove(t)

	def tStart(self):
		self.button["command"]=self.tStop
		self.button["text"]="停止"
		self.stop=False
		self.tRun()

	def tStop(self,mode=0):
		if mode == 0:
			self.tCount=1
		self.tCount-=1
		if self.tCount <= 0:
			self.button["command"]=self.ButtonClick
			self.button["text"]="搜索"
			self.stop=True

	#功能#
	def buildArgs(self,action,key):
		args=()
		if action == 1:
			if type(self.function[self.Mode][key])==tuple:
				return self.function[self.Mode][key]
			elif type(self.function[self.Mode][key])==int:
				return (self.function[self.Mode][key],)
			else:
				for i in self.function[self.Mode][key].split("\t"):
					args = args + (i.replace("sthE",self.sthE.get()),)
		elif action == 2:
			if type(self.function[self.Mode][key])==tuple:
				return self.function[self.Mode][key]
			elif type(self.function[self.Mode][key])==int:
				return (self.mainList.get(self.mainList.curselection()).split("\t")[self.function[self.Mode][key]],)
			else:
				for i in self.function[self.Mode][key].split("\t"):
					args = args + (self.mainList.get(self.mainList.curselection()).split("\t")[int(i)],)
		return args

	def ButtonClick(self):
		self.listClear()
		args=self.buildArgs(1,"args")
		#if len(self.sthE.get()) > 0:
		if self.Mode in range(len(self.function)):
			if self.function[self.Mode]["name"]!="blank":
				t = threading.Thread(target=self.function[self.Mode]["func"],args=args)
				self.threads.append(t)
				self.tStart()
				if self.function[self.Mode]["stop"]:
					self.tStop()

	def dClick(self,*args):
		args = self.buildArgs(2,"which")
		if self.function[self.Mode]["dClick"]:
			t = threading.Thread(target=self.function[self.Mode]["dClick"],args=args)
			self.threads.append(t)
			self.tStart()

	def listClear(self):
		self.mainList.delete(0,"end")

	def listAdd(self,thing):
		self.mainList.insert('end',thing)

	def browserOpen(self,url):
		try:
			webbrowser.open(url,new=1)
		except Exception as e:
			print (e)

	#右键菜单#
	def RMenu0(self):
		self.menuR.add_command(label="复制整条数据", command=self.lCopyAll)
		self.menuR.add_command(label="复制标题", command=self.lCopy0)

	def RMenu1(self):
		self.RMenu0()
		self.menuR.add_separator()
		self.menuR.add_command(label="打开该链接", command=self.dClick)
		self.menuR.add_command(label="复制百度云链接", command=self.lCopy1)

	def RMenu2(self):
		self.RMenu1()
		self.menuR.add_command(label="复制提取码/原网页链接", command=self.lCopy2)
		self.menuR.add_command(label="复制原网页链接", command=self.lCopy3)

	def RMenu4(self):
		self.RMenu0()
		self.menuR.add_separator()
		self.menuR.add_command(label="打开该链接", command=self.dClick)
		self.menuR.add_command(label="复制链接", command=self.lCopy1)

	def RMenu6(self):
		self.menuR.add_command(label="复制整条数据", command=self.lCopyAll)
		self.menuR.add_command(label="复制歌手名", command=self.MCopy0)
		self.menuR.add_command(label="复制歌曲名", command=self.MCopy1)
		self.menuR.add_command(label="复制专辑名", command=self.lCopy1)
		self.menuR.add_separator()
		self.menuR.add_command(label="下载该歌曲", command=self.dClick)

	#功能切换#
	def cT(self,*args):
		self.tStop()
		self.listClear()
		self.bLabel["text"]="Waiting......"
		self.Mode += 1
		if self.Mode in range(len(self.function)):
			if self.function[self.Mode]["name"]!="blank":
				self.label["text"]=self.function[self.Mode]["name"]
				self.sthE["state"]=self.function[self.Mode]["Entry"]
			else:
				self.cT()
		else:
			self.Mode = 0
			self.label["text"]=self.function[self.Mode]["name"]
			self.sthE["state"]=self.function[self.Mode]["Entry"]
		#print tkFileDialog.askdirectory()

	def cT0(self,*args):
		self.Mode=-1
		self.cT()

	def cT1(self,*args):
		self.Mode=0
		self.cT()

	def cT3(self,*args):
		self.Mode=2
		self.cT()

	def cT5(self,*args):
		self.Mode=4
		self.cT()

	def cT6(self,*args):
		self.Mode=5
		self.cT()

	def cT7(self,*args):
		self.Mode=6
		self.cT()

	#复制清空粘贴等#
	def lCopyAll(self):
		self.root.clipboard_append(self.mainList.get(self.mRs))

	def lCopy0(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[0])

	def MCopy0(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[0].split(" - ")[0])

	def MCopy1(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[0].split(" - ")[1])

	def lCopy1(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[1])

	def lCopy2(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[2])

	def lCopy3(self):
		self.root.clipboard_append(self.mainList.get(self.mRs).split("\t")[3])

	def eCopy(self):
		self.root.clipboard_append(self.sthE.get())

	def ePaste(self):
		try:
			self.sth.set(self.root.clipboard_get())
		except Exception as e:
			#pass
			print (e)

	def eClear(self):
		self.sth.set("")

	def eSet(self,sth):
		try:
			self.sth.set(sth)
			self.cT1()
		except Exception as e:
			#pass
			print (e)

	#主体功能#
	def PanSouM(self,name,pages=10):
		self.PanSou("%s mp3"%(name),pages)

	def Music_Download(self,id,name):
		url = self.songs_detail_new_api([int(id)])[0]['url']
		self.downloader(url,"%s.mp3"%name)

	def downloader(self,url,name,path="./"):
		try:
			self.bLabel["text"]="正在下载：%s"%name
			temp = requests.get(url,timeout=10)
			f = open(os.path.join(path,name),"wb")
			f.write(temp.content)
			f.close
			self.bLabel["text"]="下载完成：%s"%name
		except Exception as e:
			print ("!!!>%s@downloader"%e)

	def getHTML(self,url,method="GET",data=None,headers=None):
		self.bLabel["text"]="正在解析：\t%s"%(url)
		headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'} if headers is None else headers
		try:
			if method == "GET":
				page = self.opener.get(url,headers=headers,timeout=10)
				html = page.text
			elif method == "POST":
				page = self.opener.post(url,data=data,headers=headers,timeout=10)
				html = page.text
			self.bLabel["text"]="解析完成"
			return html.encode(page.encoding)
		except Exception as e:
			#print u'\t 失败,先休息一会在来吧'
			#print url
			#print e
			self.bLabel["text"]="ERROR"
			return "<ERROR>"

	def getJsonData(self,html="\{\}"):
		try:
			return json.loads(re.findall(re.compile(r"\{.*\}"),html)[0])
		except Exception as e:
			return {}

	def isLinkOK(self,url):
		html = self.getHTML(url)
		soup = BeautifulSoup(html,"html.parser")
		if soup.title.get_text().find("不存在") >= 0 or soup.title.get_text().find("jpg") >= 0 or soup.title.get_text().find("png") >= 0 or soup.title.get_text().find("gif") >= 0 or soup.title.get_text().find("apk") >= 0:
			return "",0
		elif soup.title.get_text().find("提取密码") >=0:
			return "输入提取码",9
		else:
			return soup.title.get_text().split("_免费高速下载")[0],1

	def findDownLink(self,url):
		if not self.stop:
			html = self.getHTML(url)
			try:
				a = re.findall(re.compile("(ed2k://|thunder://|magnet:\?xt=urn:btih:|ftp://)([^<>]+?)[\#\? '\"]"),html)
				if len(a)>0:
					for l in a:
						self.listAdd(l[0]+l[1])
			except Exception as e:
				print ("!!!>\t %s @fDL"%(e))
				#pass
				#print html
				#sys.exit()

	def findPanLink(self,url):
		if not self.stop:
			html = self.getHTML(url)
			try:
				soup = BeautifulSoup(html,"html.parser")
				a = re.findall(re.compile("https{0,1}://pan\.baidu\.com/s[\w&;\=/\?]+"),html)
				for l in a:
					title,lOK = self.isLinkOK(l)
					if lOK == 1:
						code = ""
						self.listAdd("%s\t%s\t%s\t%s"%(title,l,code,url))
					elif lOK == 9:
						b = re.findall(re.compile(r"%s.+?码[:：][ ]{0,2}(\w{4})"%(l)),html)
						if len(b) > 0:
							code = b[0]
						else:
							code = url
						self.listAdd("%s\t%s\t%s\t%s"%(title,l,code,url))
			except Exception as e:
				#pass
				print ("!!!>\t %s @fPL"%(e))
				print ("!>\t%s"%(url))
				#print html

	def sousuoP(self,sth,page=50):
		if len(sth.strip("")) > 0:
			for p in range(page):
				if self.stop:
					break
				url = "http://www.baidu.com/s?wd=%s&pn=%s" %(sth+" 百度云",p*10)
				html = self.getHTML(url)
				soup = BeautifulSoup(html,"html.parser")
				for i in soup.find_all("h3"):
					if not self.stop:
						try:
							self.findPanLink(i.find("a")["href"])
						except Exception as e:
							#pass
							print ("!!!>\t %s @ssP"%(e))
							#print i
							#print i.find("a")["href"]
			self.tStop(1)

	def sousuoD(self,sth,page=50):
		if len(sth.strip("")) > 0:
			for p in range(page):
				if self.stop:
					break
				url = "http://www.baidu.com/s?wd=%s&pn=%s" %(sth+" 下载",p*10)
				html = self.getHTML(url)
				soup = BeautifulSoup(html,"html.parser")
				for i in soup.find_all("h3"):
					if not self.stop:
						self.findDownLink(i.find("a")["href"])
			self.tStop(1)

	def HotMovies(self,pages=5):
		pages = int(pages)
		for p in range(pages):
			html = self.getHTML("https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28286&from_mid=1&format=json&ie=utf-8&oe=utf-8&query=电影&sort_key=17&sort_type=1&pn=%s&rn=8"%(p*8))
			jdata = self.getJsonData(html)
			for i in jdata["data"][0]["result"]:
				self.listAdd("%s\t%s"%(i["name"],i["additional"]))
		self.tStop(1)

	def PanSou(self,sth,pages=10):
		if len(sth.strip("")) > 0:
			try:
				pages=int(pages)
			except:
				exit()
			for p in range(pages):
				if self.stop:
					break
				html = self.getHTML("http://106.15.195.249:8011/search_new?q=%s&p=%s"%(sth,p+1))
				jdata = self.getJsonData(html)
				for i in jdata["list"]["data"]:
					if not self.stop:
						title,lOK = self.isLinkOK(i["link"])
						if lOK == 1 :
							self.listAdd("%s\t%s\t\t"%(i["title"],i["link"]))
			self.tStop(1)

	def DouBanRank(self,sth):
		html = self.getHTML("https://movie.douban.com/j/subject_suggest?q=%s"%(sth))
		jdata = json.loads(html)
		html1 = self.getHTML("https://movie.douban.com/subject/%s"%jdata[0]["id"])
		soup = BeautifulSoup(html1,"html.parser")
		self.listAdd(u"%s(%s)\t此片评分为：%s(%s)" %(jdata[0]["title"],jdata[0]["year"],soup.select(".rating_num")[0].get_text(),soup.select(".rating_sum > a > span ")[0].get_text()))

	def sousuo(self,sth):
		if len(sth.strip("")) > 0:
			t = threading.Thread(target=self.sousuoP,args=(sth,))
			self.threads.append(t)
			t = threading.Thread(target=self.PanSou,args=(sth,))
			self.threads.append(t)
			self.tStart()

	def support(self,*args):
		text = self.suggtext.get(1.0,"end").replace("\n","<br/>")
		#html = self.getHTML("https://jerry.jerryyan.top/api/tiny.php",method="POST",data={"support":self.iss,"text":text,})
		#print html
		tkMessageBox.showinfo(self.sugg,"反馈提交成功")
		self.sugg.quit()

	#网易云功能#
	def Music_search(self, name, stype=1, offset=0, total='true', limit=60):
		if len(name.strip("")) > 0:
			action = 'http://music.163.com/api/search/get'
			data = {
				's': name,'type': stype,'offset': offset,'total': total,'limit': limit
			}
			jData = self.getJsonData(self.getHTML(action, method = 'POST', data = data , headers = self.header1))
			if jData['code'] == 200 and jData['result']['songCount'] > 0:
				for i in jData['result']['songs']:
					self.listAdd('%s - %s\t%s\t%s'%(i['artists'][0]['name'],i['name'], i['album']['name'], i['id']))
			else:
				self.listAdd("无结果")
			self.tStop(1)

	def song_detail(self, music_id):
		action = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'.format(
			music_id, music_id)  # NOQA
		try:
			data = self.getHTML(action,headers=self.header1)
			return data['songs']
		except requests.exceptions.RequestException:
			return []

	def songs_detail(self, ids, offset=0):
		tmpids = ids[offset:]
		tmpids = tmpids[0:100]
		tmpids = list(map(str, tmpids))
		action = 'http://music.163.com/api/song/detail?ids=[{}]'.format(','.join(tmpids))
		try:
			data = self.getHTML(action,headers=self.header1)
			# the order of data['songs'] is no longer the same as tmpids,# so just make the order back
			data['songs'].sort(key=lambda song: tmpids.index(str(song['id'])))

			return data['songs']
		except requests.exceptions.RequestException:
			return []

	def songs_detail_new_api(self, music_ids, bit_rate=320000):
		action = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='  # NOQA
		csrf = ''
		action += csrf
		data = {'ids': music_ids, 'br': bit_rate, 'csrf_token': csrf}
		self.bLabel["text"]="已添加下载任务"
		result = self.getJsonData(self.getHTML(action,method="POST",data=self.encrypted_request(data),headers=self.header1, )) 
		return result['data']

	def dig_info(self, data, dig_type):
		temp = []
		if dig_type == 'songs' or dig_type == 'fmsongs':
			for i in range(0, len(data)):
				url, quality = self.geturl_new_api(data[i])
				if data[i]['album'] is not None:
					album_name = data[i]['album']['name']
					album_id = data[i]['album']['id']
				else:
					album_name = '未知专辑'
					album_id = ''

				song_info = {
					'song_id': data[i]['id'],'artist': [],'song_name': data[i]['name'],'album_name': album_name,'album_id': album_id,'mp3_url': url,'quality': quality,'playTime': play_time
				}
				if 'artist' in data[i]:
					song_info['artist'] = data[i]['artist']
				elif 'artists' in data[i]:
					for j in range(0, len(data[i]['artists'])):
						song_info['artist'].append(data[i]['artists'][j]['name'])
					song_info['artist'] = ', '.join(song_info['artist'])
				else:
					song_info['artist'] = '未知艺术家'
				temp.append(song_info)
		elif dig_type == 'artists':
			artists = []
			for i in range(0, len(data)):
				artists_info = {
					'artist_id': data[i]['id'],'artists_name': data[i]['name'],'alias': ''.join(data[i]['alias'])
				}
				artists.append(artists_info)

			return artists

		elif dig_type == 'albums':
			for i in range(0, len(data)):
				albums_info = {
					'album_id': data[i]['id'],'albums_name': data[i]['name'],'artists_name': data[i]['artist']['name']
				}
				temp.append(albums_info)

		elif dig_type == 'top_playlists':
			for i in range(0, len(data)):
				playlists_info = {
					'playlist_id': data[i]['id'],'playlists_name': data[i]['name'],'creator_name': data[i]['creator']['nickname']
				}
				temp.append(playlists_info)

		elif dig_type == 'channels':
			url, quality = self.geturl_new_api(data)
			channel_info = {
				'song_id': data['id'],'song_name': data['name'],'artist': data['artists'][0]['name'],'album_name': '主播电台','mp3_url': url,'quality': quality
			}
			temp = channel_info

		elif dig_type == 'playlist_classes':
			soup = BeautifulSoup(data, 'lxml')
			dls = soup.select('dl.f-cb')
			for dl in dls:
				title = dl.dt.text
				sub = [item.text for item in dl.select('a')]
				temp.append(title)
				self.playlist_class_dict[title] = sub

		elif dig_type == 'playlist_class_detail':
			temp = self.playlist_class_dict[data]


		elif dig_type == 'user_songs':
			for i in range(0, len(data)):
				url, quality = self.geturl_new_api(data[i])
				song_info = {
					'song_id': data[i]['id'],'artist': [],'song_name': data[i]['name'],'mp3_url': url,'quality': quality,}
				temp.append(song_info)
 

		return temp

	def encrypted_id(self,id):
		magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
		song_id = bytearray(id, 'u8')
		magic_len = len(magic)
		for i, sid in enumerate(song_id):
			song_id[i] = sid ^ magic[i % magic_len]
		m = hashlib.md5(song_id)
		result = m.digest()
		result = base64.b64encode(result)
		result = result.replace(b'/', b'_')
		result = result.replace(b'+', b'-')
		return result.decode('utf-8')

	def encrypted_request(self,text):
		text = json.dumps(text)
		secKey = self.createSecretKey(16)
		encText = self.aesEncrypt(self.aesEncrypt(text, self.nonce), secKey)
		encSecKey = self.rsaEncrypt(secKey, self.pubKey, self.modulus)
		data = {'params': encText, 'encSecKey': encSecKey}
		return data

	def aesEncrypt(self,text, secKey):
		pad = 16 - len(text) % 16
		text = text + chr(pad) * pad
		encryptor = AES.new(secKey, 2, '0102030405060708')
		ciphertext = encryptor.encrypt(text)
		ciphertext = base64.b64encode(ciphertext).decode('utf-8')
		return ciphertext

	def rsaEncrypt(self,text, pubKey, modulus):
		text = text[::-1]
		rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16)) % int(modulus, 16)
		return format(rs, 'x').zfill(256)

	def createSecretKey(self,size):
		return binascii.hexlify(os.urandom(size))[:16]

	def geturl_new_api(self,song_id):
		for i in song:
			print("%s\t%s"%(i,song[i]))
		br_to_quality = {128000: 'MD 128k', 320000: 'HD 320k'}
		alter = self.songs_detail_new_api(song_id)[0]
		url = alter['url']
		quality = br_to_quality.get(alter['br'], '')
		return url, quality

GUIDemo()
#GUIDemo().suggWindow()


