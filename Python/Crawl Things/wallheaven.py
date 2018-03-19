#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2 , re , requests , os
import sys , glob , threading
reload(sys)
sys.setdefaultencoding('utf8')

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    request = urllib2.Request(url,headers = headers)
    print u'正在解析，请稍候',
    try:
        page = urllib2.urlopen(request,None,10)
        print u'\t 成功'
    except urllib2.URLError:
        print u'\t 失败,先休息一会在来吧'
        sys.exit()
    except Exception as e:
        print u'\t 失败,先休息一会在来吧%s'%(e)
        sys.exit()
    html = page.read()
    ID = getImgID(html)
    Link = getImgLink(ID)
    for i in list(zip(ID,Link)):
        downImg(i)
    
def getImgLink(ID):
    Link = ["https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"+i for i in list(ID)]
    return Link

def getImgID(html):
    reg = r'https://alpha.wallhaven.cc/wallpaper/(\d+?)"'
    regre = re.compile(reg)
    IDlist = re.findall(regre,html)
    return IDlist
    
def downImg(i):
    ext = '.jpg'
    if not os.path.exists(os.path.join(os.path.abspath(''),"wallpaper")):
        print u'wallpaper文件夹不存在，正在创建wallpaper文件夹并继续下载'
        os.makedirs(os.path.join(os.path.abspath(''),"wallpaper"))
    if not len(glob.glob(os.path.join(os.path.abspath(''),"wallpaper",i[0]+".*"))):
        try:
            pic= requests.get(i[1]+ext, timeout=15)
            if not pic.status_code == 200:
                pic= requests.get(i[1]+'.png', timeout=15)
                ext = '.png'
            f = open(os.path.join(os.path.abspath(''),"wallpaper",i[0]+ext),'wb')
            f.write(pic.content)
            f.close
            print u'已将 '+i[1]+ext+u'\t 下载到  \twallpaper/'+i[0]+ext
        except requests.exceptions.ConnectionError:
            print u'下载 '+i[1]+ext+u'\t 时出错：\t链接错误'
        except requests.exceptions.ReadTimeout:
            print u'下载 '+i[1]+ext+u'\t 时出错：\t链接超时'
        except KeyboardInterrupt:
            print u'正在退出……'
            sys.exit()
    else:
        print u'文件 \twallpaper/'+i[0]+u'.jpg \t已存在，跳过下载……'
for i in range(1,20):
    t=threading.Thread(target=getHTML,args=("https://alpha.wallhaven.cc/search?q=&categories=100&purity=110&sorting=random&order=desc",))
    t.start()
