#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    request = urllib2.Request(url,headers = headers)
    print u'正在解析，请稍候'
    try:
        page = urllib2.urlopen(request,None,10)
        html = page.read()
        print u'解析成功'
    except urllib2.URLError:
        print u'无法解析,先休息一会在来吧1'
        sys.exit()
    except socket.timeout:
        print u'解析超时，在来一遍'
        retry
    except:
        print '????'
        sys.exit()
    Title = getTitle(html)
    VC = getViewCount(html)
    Link = getLink(html)
    Like = getLike(html)
    ID = getID(html)
    return list(zip(Title,Link,VC,Like,ID))

def getViewCount(html):
    reg = r'<i class="iconfont ic-list-read"></i> (\d+?)\n</a>'
    regre = re.compile(reg)
    ViewCount = re.findall(regre,html)
    return ViewCount
    
def getTitle(html):
    reg = r'<a class="title" target="_blank" href="/p/.+?">(.+?)</a>'
    regre = re.compile(reg)
    Title = re.findall(regre,html)
    return Title

def getLink(html):
    reg = r'<a class="title" target="_blank" href="/p/(.+?)">'
    regre = re.compile(reg)
    Link = ['http://www.jianshu.com/p/' + i for i in list(re.findall(regre,html))]
    return Link

def getLike(html):
    reg = r'<i class="iconfont ic-list-like"></i> (\d+?)</span>'
    regre = re.compile(reg)
    Like = re.findall(regre,html)
    return Like

def getID(html):
    reg = r'<li id="note-\d+?" data-note-id="(\d+?)"'
    regre = re.compile(reg)
    ID = re.findall(regre,html)
    return ID

url="http://www.jianshu.com/trending/weekly?utm_medium=index-banner-s&utm_source=desktop"
for n in range(1,6):
    temp = getHTML(url+'&page='+str(n))
    for i in temp:
        print u'标题： '+i[0]
        print u'链接： '+i[1]
        print u'阅读量 '+i[2]+u'\t喜欢量 '+i[3]+u'\t文章ID '+i[4]
        url = url + '&seen_snote_ids[]=' + i[4]
    
    


