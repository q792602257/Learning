#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os , urllib , glob
import sys , json , http.cookiejar
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

def getReferer(url):  
    reference = "http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id="  
    reg = r'.+/(\d+)_p0'  
    return reference + re.findall(reg,url)[0] + "&page=0"  
def pLogin():
    login_url="https://www.pixiv.net/login.php"#登录页面api
    ldata={'pixiv_id' : 'jerryyan0912',#帐号
        'pass' : 'YAN1HAO',#密码
        'mode' : 'login',
        'skip' : 1}
    login_data=urllib.urlencode(ldata)#处理一下post DATA
    login_header={'Accept-Language':'zh-CN,zh;q=0.8',
                'Referer':'https://www.pixiv.net/login.php?return_to=0',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'  }
    request = urllib2.Request(url=login_url,headers=login_header,data=login_data)
    print(u'正在尝试登录'),
    cookie = http.cookiejar.MozillaCookieJar()#存储cookie的容器
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)#网页请求处理器，包含cookie
    response = opener.open(request)#登录
    print(u'\t 登录部分处理完毕')  
    return opener , cookie
    #上方无法处理登录出错的情况
def getHtml(url1,cookie,referer):#处理普通的网页，主要是p站要查referer，要不然403
    header={'Accept-Language':'zh-CN,zh;q=0.8',
                'Referer':referer,
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'  }
    request = urllib2.Request(url=url1,headers=header)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    try:
        response = opener.open(request)
    except Exception as e: #出错了？死给你看
        print url1
        print cookie
        print header
        print e
        sys.exit()
    return response.read()
opener , cookie = pLogin()#包含cookie的网页请求处理器
sousuo="東方project"
for i in range(1):
    html = getHtml("https://www.pixiv.net/search.php?word="+sousuo+"&s_mode=s_tag_full&order=date_d&p="+str(i),cookie,"https://www.pixiv.net/search.php?s_mode=s_tag_full&word="+sousuo)
    soup=BeautifulSoup(html,"html.parser")#//建一个BS4实例
    thumb = soup.find_all("img",class_ = "_thumbnail")#//找class 为_thumbnail的img标签
    for img in thumb:
        print img.get('data-id') #//获取img标签下的data-id值
        print img.get('data-src')
