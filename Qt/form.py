# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json
class api():
    opener = requests.Session()
    # opener.cookies=MozillaCookieJar()
    times=0
    headers={"Connection": "Keep-Alive","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    oldret={"Error":"No Network"}
    def getHTML(self,url,method="GET",data=None):
        try:
            if method=="GET":
                page=self.opener.get(url,headers=self.headers)
                html=page.text
            elif method=="POST":
                page=self.opener.post(url,data=data,headers=self.headers)
                html=page.text
        except Exception as e:
            print (e)
            html="{'Error'='{e}'}"
        finally:
            return html
    def newWeatherCodeHandler(self,code):
        weathercode={0:u"晴",1:u"多云",2:u"阴",3:u"阵雨",4:u"雷阵雨",5:u"雷阵雨并伴有冰雹",6:u"雨夹雪",7:u"小雨",
        8:u"中雨",9:u"大雨",10:u"暴雨",11:u"大暴雨",12:u"特大暴雨",13:u"阵雪",14:u"小雪",15:u"中雪",16:u"大雪",
        17:u"暴雪",18:u"雾",19:u"冻雨",20:u"沙尘暴",21:u"小雨-中雨",22:u"中雨-大雨",23:u"大雨-暴雨",
        24:u"暴雨-大暴雨",25:u"大暴雨-特大暴雨",26:u"小雪-中雪",27:u"中雪-大雪",28:u"大雪-暴雪",29:u"浮沉",
        30:u"扬沙",31:u"强沙尘暴",32:u"飑",33:u"龙卷风",34:u"若高吹雪",35:u"轻雾",53:u"霾",99:u"未知"}
        return weathercode[int(code)]
    def windHandler(self,direction="",speed=""):
        if len(direction)!=0:
            direction = float(direction) 
            if direction>337.5 and direction<=360.0:
                d = u"北风"
            elif direction > 292.5:
                d = u"西北风"
            elif direction > 247.5:
                d = u"西风"
            elif direction > 202.5:
                d = u"西南风"
            elif direction > 157.5:
                d = u"南风"
            elif direction > 112.5:
                d = u"东南风"
            elif direction > 67.5:
                d = u"东风"
            elif direction > 22.5:
                d = u"东北风"
            elif direction<= 22.5 and direction>=0.0:
                d = u"北风"
            else:
                d = u""
        else:
            d=u""
        if len(speed)!=0:
            speed = float(speed)
            if speed <= 1.0 and speed >= 0.0:
                s=u"0级"
            elif speed <= 6.0:
                s=u"1级"
            elif speed <= 11.0:
                s=u"2级"
            elif speed <= 19.0:
                s=u"3级"
            elif speed <= 28.0:
                s=u"4级"
            elif speed <= 38.0:
                s=u"5级"
            elif speed <= 49.0:
                s=u"6级"
            elif speed <= 61.0:
                s=u"7级"
            elif speed <= 74.0:
                s=u"8级"
            elif speed <= 88.0:
                s=u"9级"
            elif speed <= 102.0:
                s=u"10级"
            elif speed >  102.0:
                s=u"飓风"
            else:
                s=""
        else:
            d=u""
        return "%s%s"%(d,s)
    def newWeatherHandler(self):
        code="101020300"
        url="https://weatherapi.market.xiaomi.com/wtr-v3/weather/all?latitude=31.383602&longitude=121.502899&isLocated=true&locationKey=weathercn:%s&days=15&appKey=weather20151024&sign=zUFJoAR2ZVrDy1vF3D07&romVersion=7.11.9&appVersion=102&alpha=false&isGlobal=false&device=ido&modDevice=ido_xhdpi&locale=zh_cn"%code
        if self.times>5 or self.times==0:
            html = self.getHTML(url)
            self.times=1
        else:
            self.times+=1
            return self.oldret
        try:
            jdata=json.loads(html)
            if 'Error' in jdata:
                return jdata
            ret={}
            ret["aqi"]=jdata["aqi"]["aqi"]
            ret["city"]="宝山"
            ret["tempRaw"]=int(jdata["current"]["temperature"]["value"])
            ret["temp"]="%2s[%.1f]℃"%(jdata["current"]["temperature"]["value"],float(jdata["current"]["feelsLike"]["value"]))
            ret["pressure"]="%shPa"%(jdata["current"]["pressure"]["value"])
            ret["weather"]=self.newWeatherCodeHandler(jdata["current"]["weather"])
            ret["time"]=jdata["current"]["pubTime"][11:16]
            ret["wet"]="%s"%jdata["current"]["humidity"]
            ret["wind"]=self.windHandler(jdata["current"]["wind"]["direction"]['value'],jdata["current"]["wind"]["speed"]['value'])
            ret["detail"]=[]
            ret["future"]=[]
            for i in range(0,35):
                t={}
                t["tempRaw"]=int(jdata["forecastHourly"]["temperature"]["value"][i])
                t["temp"]=u"%s℃"%(jdata["forecastHourly"]["temperature"]["value"][i])
                t["weather"]=self.newWeatherCodeHandler(jdata["forecastHourly"]["weather"]["value"][i])
                t["stime"]=jdata["forecastHourly"]["wind"]["value"][i]["datetime"][11:16]
                t["wind"]=self.windHandler("",jdata["forecastHourly"]["wind"]['value'][i]["speed"])
                t["windRaw"]=float(jdata["forecastHourly"]["wind"]['value'][i]["speed"])
                ret["detail"].append(t)
            tmp=[u"今天",u"明天",u"后天"]
            for j in range(0,3):
                t={}
                # forecastDaily
                t["date"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["from"][5:10]
                t["week"]=tmp[j]
                t1=jdata["forecastDaily"]["weather"]["value"][j]["from"]
                t2=jdata["forecastDaily"]["weather"]["value"][j]["to"]
                if t1==t2:
                    t["weather"]=self.newWeatherCodeHandler(t1)
                else:
                    t["weather"]=u"%s转%s"%(self.newWeatherCodeHandler(t1),self.newWeatherCodeHandler(t2))
                t["sunrise"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["from"][11:16]
                t["sunset"]=jdata["forecastDaily"]["sunRiseSet"]["value"][j]["to"][11:16]
                t["temp"]=u"%2s/%2s℃"%(jdata["forecastDaily"]["temperature"]["value"][j]["from"],jdata["forecastDaily"]["temperature"]["value"][j]["to"])
                t["wind"]=self.windHandler(jdata["forecastDaily"]["wind"]["direction"]['value'][j]["from"],jdata["forecastDaily"]["wind"]["speed"]['value'][j]["from"])
                ret["future"].append(t)
            self.oldret=ret
            return ret
        except Exception as e:
            if "html" in vars():
                print (html)
            print (e)
            if 'self.oldret' in vars():
                return self.oldret
            else:
                return {"Error":u"请连接网络"}
class Ui_Form(object):
    def __init__(self, *args, **kwargs):
        self.DPI=1
        self.width=176*self.DPI
        self.height=264*self.DPI
        self.W=QtWidgets.QDesktopWidget().screenGeometry().width()
        self.H=QtWidgets.QDesktopWidget().screenGeometry().height()
    def setupUi(self, Form):
        self.Form=Form
        Form.setObjectName("Form")
        Form.setGeometry(self.W-(self.width+32)*self.DPI,32*self.DPI,self.width*self.DPI, self.height*self.DPI)
        Form.setWindowOpacity(0.8)
        Form.setStyleSheet("""
        QMainWindow {
            background:gray;
        }
        QLabel {
            color:black;
            background:white;
        }
        QLabel[bw="true"] {
            color:white;
            background:black;
        }""")
        self.BigTime = QtWidgets.QLabel(Form)
        self.BigTime.setGeometry(QtCore.QRect(0, 0, int(self.width*self.DPI), int(36*self.DPI)))
        self.BigTime.setObjectName("BigTime")
        self.BigTime.setFont(QtGui.QFont("Inziu Iosevka SC",int(32*self.DPI),QtGui.QFont.Bold))
        self.SmallDate=QtWidgets.QLabel(Form)
        self.SmallDate.setProperty("bw",True)
        self.SmallDate.setGeometry(QtCore.QRect(self.width-int(96*self.DPI), self.BigTime.height(), int(96*self.DPI), int(20*self.DPI)))
        self.SmallDate.setFont(QtGui.QFont("Inziu Iosevka SC",int(12*self.DPI),QtGui.QFont.Bold))
        self.Temp = QtWidgets.QLabel(Form)
        self.Temp.setProperty("bw",True)
        self.Temp.setGeometry(QtCore.QRect(0, self.BigTime.height(), self.width-self.SmallDate.width()-1,int(20*self.DPI)))
        self.Temp.setFont(QtGui.QFont("Inziu Iosevka SC",int(12*self.DPI)))
        self.Temp.setText("00[00.0]℃")
        self.Weather = QtWidgets.QLabel(Form)
        self.Weather.setGeometry(QtCore.QRect(0, self.SmallDate.y()+self.SmallDate.height(), int(80*self.DPI),int(60*self.DPI)))
        self.Weather.setFont(QtGui.QFont("Inziu Iosevka SC",int(32*self.DPI)))
        self.Weather.setText(str(self.SmallDate.y()+self.SmallDate.height()))
        self.commandLinkButton = QtWidgets.QCommandLinkButton(Form)
        self.commandLinkButton.setGeometry(QtCore.QRect(600, 140, 172, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_weather)
        self.timer.start(300000)
        self.update_weather()

    def update_weather(self):
        a=api().newWeatherHandler()
        if "error" in a:
            self.Form.setFixedSize(self.width*self.DPI, 60*self.DPI)
            self.Temp.setText("<b>网络异常</b>")
        else:
            self.Temp.setText(a['temp'])
            self.Weather.setText("<b>"+a['weather']+"</b>")
            self.Form.setFixedSize(self.width*self.DPI, 120*self.DPI)            

    def update_time(self):
        now = datetime.datetime.now()
        self.BigTime.setText(now.strftime("%H:%M:%S"))
        self.SmallDate.setText(now.strftime("%y/%m/%d")+"<small> "+now.strftime("%a")+"</small>")

    def retranslateUi(self, Form):
        Form.setWindowTitle("Form")
        self.commandLinkButton.setText("Form, CommandLinkButton")
