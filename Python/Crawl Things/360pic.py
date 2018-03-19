#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os
import sys , threading , json
reload(sys)
sys.setdefaultencoding('utf8')

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    request = urllib2.Request(url,headers = headers)
    print u'正在解析目录，请稍候',
    try:
        page = urllib2.urlopen(request,None,10)
        print u'解析成功'
    except urllib2.URLError:
        print u'\t 失败,先休息一会在来吧'
        exit
    except Exception as e:
        print e
        exit
    Jdata = json.loads(page.read())
    for i in range(0,Jdata['count']):
        getJSON(Jdata['list'][i]['id'])
#    ID = getImgShowID(html)
#    Link = getImgLink(ID)
#    for i in list(zip(Link,gID)):
#        downImg(i)

def getJSON(ID):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    url='http://image.so.com/zvj?ch=wallpaper&t1=157&id='+ID
    request = urllib2.Request(url,headers = headers)
    #print u'正在解析链接，请稍候',
    try:
        page = urllib2.urlopen(request,None,10)
        print u'解析成功'
        gJson = json.loads(page.read())
        for i in range(0,len(gJson['list'])):
            ext = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',gJson['list'][i]['pic_url'])
            if len(ext) == 0 : ext = ['.jpg']
            downImg([gJson['list'][i]['pic_url'],ID+"_"+str(i),ext[0]])
    except urllib2.URLError:
        print u'\t 失败,先休息一会在来吧'
        exit
    except Exception as e:
        print e
        exit

def downImg(i):
    ext = i[2]
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper3")):
        print u'wallpaper3文件夹不存在，正在创建wallpaper3文件夹并继续下载'
        os.makedirs(os.path.join(os.path.abspath(''),"wallpaper3"))
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper3",i[1]+ext)):
        try:
            pic= requests.get(i[0], timeout=20)
            if not pic.status_code == 200:
                print u'图片出错了……'+str(pic.status_code)
                exit
            f = open(os.path.join(os.path.abspath(''),"wallpaper3",i[1]+ext),'wb')
            f.write(pic.content)
            f.close
            print u'已将 '+i[0]+u'\t 下载到  \twallpaper3/'+i[1]+ext
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
        print u'wallpaper3/'+i[1]+ext+u'\t 已经存在，跳过下载'
        exit


urlb="http://image.so.com/zj?ch=wallpaper&t1=157"
#t=threading.Thread(target=getHTML,args=(url,))
#t.start()
getHTML(urlb)
for i in range(1,10):
    url = urlb+l+'&sn='+str(i*30)
#    t=threading.Thread(target=getHTML,args=(url,))
#    t.start()
    getHTML(url)
urlc="http://image.so.com/zj?ch=go"
getHTML(urlc)
for j in range(1,10):
    url = urlc+'&sn='+str(j*30)
#    t=threading.Thread(target=getHTML,args=(url,))
#    t.start()
    getHTML(url)


