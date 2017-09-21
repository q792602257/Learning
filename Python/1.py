#!/usr/bin/python
# -*- coding:utf-8 -*-
#coding = utf-8
import urllib , re , json , MySQLdb
import sys , time
reload(sys)
sys.setdefaultencoding('utf8')

def SQLAdd(title,info,date):
    conn= MySQLdb.connect(
            host='www.himei.top',
            port = 3306,
            user='jerry',
            passwd='admin',
            db ='jerry',
            charset="utf8",
            )
    sql = conn.cursor()
    sql.execute('INSERT INTO zhihudaily VALUES(%s,\"%s\",%s)',(title.encode("utf-8"),MySQLdb.escape_string(info.encode("utf-8")),date))
    print "MySQL Add OK"
    sql.close()
    conn.commit()
    conn.close()

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'}
    page = urllib.urlopen(url)
    html = page.read()
    return html

temp = json.loads(getHTML("http://news-at.zhihu.com/api/4/news/latest"))
for tmp in (temp["top_stories"]+temp["stories"]):
    t_title = tmp["title"]
    t_id = tmp["id"]
    tmp_info = json.loads(getHTML("http://news-at.zhihu.com/api/4/news/"+str(t_id)))
    t_info = tmp_info["body"]
    t_date = time.strftime("%Y%m%d")
    SQLAdd(t_title,t_info,t_date)
sys.exit()

