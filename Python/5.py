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
        print u'\t解析成功'
    except urllib2.URLError:
        print u'\t 失败,在来一遍'
        retry
    except Exception as e:
        print e
        exit
    html = page.read()
    regre = re.compile(r'md5&quot;:&quot;(.+?)&quot;',re.S)
    md5 = re.findall(regre,html)
    regre = re.compile(r'murl&quot;:&quot;(.+?)&quot;',re.S)
    Link = re.findall(regre,html)
#    ID = getImgShowID(html)
#    Link = getImgLink(ID)
    for i in list(zip(Link,md5)):
        ext=re.findall(r'\.[^.\\/:*?"<>]+$',i[0])
        if len(ext) == 0 : ext = ['.jpg']
        downImg(i,ext[0])

def downImg(i,ext):
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper")):
        print u'wallpaper文件夹不存在，正在创建wallpaper文件夹并继续下载'
        os.makedirs(os.path.join(os.path.abspath(''),"wallpaper"))
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper",i[1]+ext)):
        try:
            pic= requests.get(i[0], timeout=20)
            if not pic.status_code == 200:
                print i[0]+u'\t图片出错了……\t'+str(pic.status_code)
                exit
            f = open(os.path.join(os.path.abspath(''),"wallpaper",i[1]+ext),'wb')
            f.write(pic.content)
            f.close
            print u'已将 '+i[0]+u'\t 下载到  \twallpaper/'+i[1]+ext
        except requests.exceptions.ConnectionError:
            print u'下载 '+i[0]+u'\t 时出错：\t链接错误'
        except requests.exceptions.ReadTimeout:
            print u'下载 '+i[0]+u'\t 时出错：\t链接超时'
        except KeyboardInterrupt:
            print u'正在退出……'
            sys.exit()
        except Exception as e:
            print e
            exit
    else:
        print u'wallpaper/'+i[1]+ext+u'\t 已经存在，跳过下载'
        exit

urlb="http://cn.bing.com/images/"
for l in ("%e7%bb%bf%e6%a4%8d","%e9%a3%8e%e6%99%af","%e8%8a%b1%e6%b5%b7%","%e6%b5%b7%e6%b4%8b"):
    url=urlb+'search?q='+l+'%e5%a3%81%e7%ba%b8'
#    t=threading.Thread(target=getHTML,args=(url,))
#    t.start()
    getHTML(url)
    for i in range(1,10):
        url = urlb+'async?q='+str(l)+'%e5%a3%81%e7%ba%b8&first='+str(i*36)+'&count=35&relp=35&lostate=r&mmasync=1'
        #t=threading.Thread(target=getHTML,args=(url,))
        #t.start()
        getHTML(str(url))


