#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import sys
import os
from urllib import quote
import re
from bs4 import BeautifulSoup as Soup
reload(sys)
sys.setdefaultencoding("utf8")

opener = requests.Session()
def getHTML(url,referer=""):
	global opener
	header = {"Connection": "keep-alive","Referer":referer}
	page = opener.get(url, headers=header)
	html = page.content
	return html
def weatherN(city,code):
	print city,code
	html = getHTML("http://www.weather.com.cn/weather1dn/%s.shtml"%code,"http://www.weather.com.cn/weather1dn/%s.shtml"%code)
	soup = Soup(html,"html.parser")
	script = soup.select("div.todayRight script")[0].get_text().strip()
	varList=re.findall("var (.+?) ?= ?(.+?);[v \r\n]",script)
	var={}
	for i in varList:
		var[i[0]]=json.loads(i[1])
	return var

def weather(city, code):
	print city,code
	a = weatherN(city, code)
	html = getHTML("http://d1.weather.com.cn/sk_2d/%s.html"%code,"http://m.weather.com.cn/mweather/%s.shtml"%code)
	html2 = getHTML("http://d1.weather.com.cn/weixinfc/%s.html"%code,"http://m.weather.com.cn/mweather/%s.shtml"%code)
	html3 = getHTML("http://d1.weather.com.cn/aqi_7d/XiangJiAqiFc5d/%s.html"%code,"http://m.weather.com.cn/mweather/%s.shtml"%code)
	jhtml=re.findall("{.+}",html)[0]
	jhtml2=re.findall("{.+}",html2)[0]
	jhtml3=re.findall("{.+}",html3)[0]
	jdata = json.loads(jhtml)
	jdata2 = json.loads(jhtml2)["f"]
	jdata3 = json.loads(jhtml3)["2001006"]
	weatherInfo={}
	weatherInfo["wet"]=jdata["SD"]
	weatherInfo["wind"]=jdata["WD"]+jdata["WS"]
	weatherInfo["aqi"]=jdata["aqi"]
	weatherInfo["isRain"]=jdata["rain24h"]
	weatherInfo["temp"]=jdata["temp"]
	weatherInfo["weather"]=jdata["weather"]
	weatherInfo["time"]=jdata["time"]
	weatherInfo["future"]=[]
	e=0
	for day in jdata2[1:3]:
		t={}
		t["天气1"]=day["fa"]
		t["天气2"]=day["fb"]
		t["温度1"]=day["fc"]
		t["温度2"]=day["fd"]
		t["风1"]=day["fe"]+day["fg"]
		t["风2"]=day["ff"]+day["fh"]
		t["日期"]=day["fi"]+day["fj"]
		t["日落"]=a["sunset"][e]
		t["日出"]=a["sunup"][e]		
		weatherInfo["三日天气"].append(t)
		e +=1
	weatherInfo["stime"]=a["uptime"]
	weatherInfo["detail"]=[]
	e=0
	for u in a["detail"]:
		for v in u:
			t={}
			t["weather"]=v["ja"]
			t["stime"]=v["jf"]
			t["temp"]=v["jb"]
			t["windd"]=v["jd"]
			t["wet"]=v["je"]
			t["isRain"]=v["jc"]
			weatherInfo["detail"].append(t)
		e+=1
		if e>=10:
			break
	return weatherInfo

def city2code(city):
	html = getHTML("http://toy1.weather.com.cn/search?cityname=%s" % (city))
	try:
		jhtml = re.findall("\((.*)\)", html)[0]
		jdata = json.loads(jhtml)[0]
		data = jdata["ref"].split("~")
		code = data[0]
		city = "%s-%s-%s" % (data[-1], data[4], data[2])
		return city, code
	except Exception as e:
		print "@c2c\t%s" % e
city, code = city2code("jiujiang")
print weather(city, code)
