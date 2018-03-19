#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os
import sys , threading
reload(sys)
sys.setdefaultencoding('utf8')

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    request = urllib2.Request(url,headers = headers)
    print u'正在解析目录，请稍候',
    try:
        page = urllib2.urlopen(request,None,10)
        print u'\t 解析成功'
    except urllib2.URLError:
        print u'\t 失败,先休息一会在来吧'
        sys.exit()
    except Exception as e:
        print e
        sys.exit()
    html = page.read()
    regre = re.compile(r'<li><a href="/desk/(.*?).htm"',re.S)
    ID = re.findall(regre,html)
#    ID = getImgShowID(html)
#    Link = getImgLink(ID)
    temp = getImgShowLink(ID)
#    return list(zip(ID,Link))

def getImgShowLink(ID):
    for i in ID:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
        url = 'http://www.netbian.com/desk/'+i+'-1920x1080.htm'
        request = urllib2.Request(url,headers = headers)
        print u'正在解析链接，请稍候',
        try:
            page = urllib2.urlopen(request,None,10)
        except urllib2.URLError:
            print u'\t 失败,先休息一会在来吧'
            retry
        except Exception as e:
            print e
            continue
        html = page.read()
        regre = re.compile(r'<table id="endimg".+?<img src="(.+?)"',re.S)
        Link = re.findall(regre,html)
        if len(Link) == 0 : 
            print u'\t誓死不开VIP'
            continue
        print u'\t 解析成功'
        downImg([Link[0],i])
    
def downImg(i):
    ext = '.jpg'
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper")):
        print u'wallpaper文件夹不存在，正在创建wallpaper文件夹并继续下载'
        os.makedirs(os.path.join(os.path.abspath(''),"wallpaper"))
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper",i[1]+ext)):
        try:
            pic= requests.get(i[0], timeout=10)
            if not pic.status_code == 200:
                print u'图片出错了……\t' + str(pic.status_code)
                exit
            f = open(os.path.join(os.path.abspath(''),"wallpaper",i[1]+ext),'wb')
            f.write(pic.content)
            f.close
            print u'已将 '+i[0]+u'\t 下载到  \twallpaper/'+i[1]+ext
        except requests.exceptions.ConnectionError:
            print u'下载 '+i[0]+u'\t 时出错：\t链接错误'
            exit
        except requests.exceptions.ReadTimeout:
            print u'下载 '+i[0]+u'\t 时出错：\t链接超时'
            exit
        except KeyboardInterrupt:
            print u'正在退出……'
            sys.exit()
        except Exception as e:
            print e
            exit
    else:
        print u'wallpaper/'+i[1]+ext+u'\t 已经存在，跳过下载'
        exit

urlb="http://www.netbian.com/"
for l in ('fengjing','jianzhu','huahui',"sheji"):
    url=urlb+l+'/'
    #t=threading.Thread(target=getHTML,args=(url,))
    #t.start()
    getHTML(url)
    for i in range(2,10):
        url = urlb+l+'/index_'+str(i)+'.htm'
        getHTML(url)
        #t=threading.Thread(target=getHTML,args=(url,))
        #t.start()


