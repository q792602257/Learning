# coding:utf8
import requests
# from cookiejar import MozillaCookieJar
import datetime
import time
import os
import sys
import re
from flask import Flask
from flask import render_template as T
from flask import request as R
reload(sys)
sys.setdefaultencoding("utf8")

app=Flask(__name__)
@app.route("/")
def indexPage():
	return T("index.html")
@app.route("/vote",methods=["GET"])
def startVote():
	openid = R.args.get("openid","")
	icode = R.args.get("icode", "")
	if icode=="":
		return T("step1.html", openid=openid)
	text = vote(openid,icode)
	return buildPage(text)
@app.route("/step1",methods=["GET"])
def step1():
	url = R.args.get("url","")
	code= R.args.get("code", "")
	openid = R.args.get("openid", "")
	if openid=="":
		code = getCode(url)
		openid=getOpenID(code)
	downimg(openid)
	if not openid:
		print openid
		return T("error.html")
	return T("step1.html",openid=openid,code=code)
def getOpenID(code):
	h2 = {"Connection": "keep-alive",
            "Referer": "https://health.10086.cn/questionnaire/index.html?code=%s&state=1" % (code),
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"}
	ourl = "https://health.10086.cn/sfi/s/wechat/question/getManageById"
	odata = "id=&state=1&code=%s" % (code)
	try:
		op = requests.post(ourl, data=odata, headers=h2)
		od = op.json()
		openid = od['dataMap']["openid"]
	except:
		print('Cant Get OpenID!')
		print op.text
		return False
	if openid == "":
		print("The Code Has Been Used!")
		return False
	return openid
def downimg(openid):
	ts="%d"%(int(time.time()*1000))
	imgurl = "https://health.10086.cn/sfi/s/code/%s/getImageCode?openId=%s"%(ts,openid)
	print openid
	imgpage = requests.get(imgurl)
	imgcontent = imgpage.content
	with open("static/imgs/temp.jpg","wb") as f:
		f.write(imgcontent)
def vote(openid,icode):
	headers={"Accept":"application/json, text/javascript, */*; q=0.01",
			"Accept-Encoding":"gzip, deflate, br",
			"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
			"Connection":"keep-alive",
			"Referer":"https://health.10086.cn/questionnaire/all/record.html",
        	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
			"X-Requested-With":"XMLHttpRequest"
			}
	url="https://health.10086.cn/sfi/s/wechat/question/saveWechatQuestion"
	while not icode:
		downimg(openid)
		icode = raw_input("Please Input The Code:\t")
		if code == "r" or code == "":
			continue
		else:
			break
	data = {"imageCode":icode,
		"smsCode":"","data":'{"imageCode":"%s","smsCode":"","manageId":"2","manageName":"","typeId":"2","typeName":"","questionId":"6","questionName":"","hospitalId":2700,"latitude":"","longitude":"","openid":"%s","channelCode":"wechat_main","questionType":"","hospitalName":"","sex":"男","name":"","education":"本科或大专","pay":"城镇医疗保险（职工 / 居民）","medicalRecord":"","telephone":"","awardStatus":"","result1":3,"result2":"","result3":4,"result4":3,"result5":4,"result6":4,"result7":4,"result8":3,"result9":4,"result10":3,"result11":3,"result12":3,"result13":4,"result14":3,"result15":4,"result16":3,"result17":4,"result18":"10","result19":3,"result20":"","result21":1,"result26":"","result27":"","result28":"","result29":"","result30":"","result31":"","result32":"","result33":"","result34":"","result35":"","result36":"","result37":"","result38":"","result39":"","result40":"","result41":"","result42":"","result43":"","result44":"","result45":"","result46":"","result47":"","result48":"","result49":"","result50":"","age":"20 - 29岁"}' % (icode,openid)}
	try:
		page = requests.post(url,data=data,headers=headers)
		jdata = page.json()
	except:
		return page.text
	if jdata["resultCode"]==0:
		return jdata["resultMsg"]
	else:
		print(jdata["resultMsg"])
		return "ERROR OCCURED!!!"
def buildPage(text):
	template = """
<head>
	<title id="title">2017年全国万家医院满意度调查</title>
	<link rel="stylesheet" href="static/css/common.css">
	<link rel="stylesheet" href="static/css/c.css">
	<style>
		div {
            text-align: center;
			width:20rem;
        }
	</style>
</head>
<body>
	<div class="hjk-container" id="recordContainer">
	<div class="success-frame">
		<img src="static/imgs/icon_success.png" style="width: 28%;margin-top: 20%;margin-bottom: 8%;">
		<div style="color: #333;font-size: 0.9rem;margin-bottom: 0.7rem;">
			感谢您的参与！
		</div>
		<div style="color: #808080;font-size: 0.75rem;height:16%;padding: 0 13%;" id="pageSuccessTips">
			{{TEXT}}
		</div><div style="background: rgb(242, 243, 246) none repeat scroll 0% 0%; height: 16px; display: none;" id="zhuicha">

		</div>
		<img src="imgs/commity_down.png" style="width: 100%; display: none;" id="imgs2">
	</div>
	</div>
</body>""".replace("{{TEXT}}",text)
	return template
def getCode(url):
	url=url.strip('"').strip("'")
	if url.startswith("https://"):
		url = re.findall(r"\?code=(.{32})",url)[0]
	if len(url)==32:
		return url
	print ("Cant Get A Valid Code!!!")
	return ""
app.run("0.0.0.0",8901)
while False:
	url=raw_input("Input Wechat Url(q:Exit)\t")
	if url=="q":
		print ("You Want Exit,and Let it Go!")
		break
	code =getCode(url)
	phtml = vote(code)
	print (phtml)
	html = buildPage(phtml)
	with open("%s.html"%(code),"w") as f:
		f.write(html)
