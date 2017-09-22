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
	weatherInfo["湿度"]=jdata["SD"]
	weatherInfo["风向"]=jdata["WD"]
	weatherInfo["风力"]=jdata["WS"]
	weatherInfo["空气质量"]=jdata["aqi"]
	weatherInfo["下雨概率"]=jdata["rain24h"]
	weatherInfo["当前温度"]=jdata["temp"]
	weatherInfo["当前天气"]=jdata["weather"]
	weatherInfo["更新时间"]=jdata["time"]
	weatherInfo["三日天气"]=[]
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
	weatherInfo["预报更新时间"]=a["uptime"]
	weatherInfo["小时预报"]=[]
	e=0
	for u in a["hour3data"]:
		for v in u:
			t={}
			t["天气"]=v["ja"]
			t["时间"]=v["jf"]
			t["温度"]=v["jb"]
			t["风向"]=v["jd"]
			t["湿度"]=v["je"]
			t["下雨"]=v["jc"]
			weatherInfo["小时预报"].append(t)
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
