#coding:utf8
from selenium import webdriver
from time import sleep
from time import time
from bs4 import BeautifulSoup as Soup
import pymysql as mysql

s=webdriver.PhantomJS()
con=mysql.connect(host="localhost",port=3306,user='root',password='Bd960912',db='jerry',charset='utf8')
cursor=con.cursor()
def get_share_html():
    url="https://tool.ssrshare.com/tool/share_ssr"
    s.get(url)
    sleep(5)
    return s.page_source
def get_free_html():
    url="https://tool.ssrshare.com/tool/free_ssr"
    s.get(url)
    sleep(5)
    return s.page_source
def Add(i,isK=1):
    if i[1]=="" or i[2]=="" or i[3]=="" or i[4]=="" or i[5]=="" or i[6]=="":
        print(i)
        print("ERROR")
        return False
    I_bsql="INSERT INTO `ssr` (`name`,`server`,`port`,`protocol`,`method`,`obfs`,`keys`,`obfsparam`,`protoparam`,`isKey`) VALUES ('{name}','{server}','{port}','{protocol}','{method}','{obfs}','{keys}','{obfsparam}','{protoparam}','{isK}');"
    Q_bsql="SELECT COUNT(1) FROM `ssr` WHERE `server` = '{server}' AND `port` = '{port}' AND `protocol` = '{protocol}' AND `method` = '{method}' AND `obfs` = '{obfs}' AND `keys` = '{keys}' AND `obfsparam` = '{obfsparam}' AND `protoparam` = '{protoparam}'; "
    Q_sql=Q_bsql.format(server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7])
    cursor.execute(Q_sql)
    if cursor.fetchall()[0][0] > 0:
        print("EXIST")
        return False
    print(i)
    I_sql=I_bsql.format(name=i[0],server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7],isK=isK)
    cursor.execute(I_sql)
    con.commit()
    return True
def html_parser(html):
    soup = Soup(html,"html.parser")
    table = soup.select_one("div.dx-datagrid-rowsview div.dx-datagrid-content table")
    columns = table.select("tr")
    columns.pop(0)
    columns.pop()
    for i in columns:
        rows=i.select("td")
        rows.pop(0)
        server=rows[0].get_text()
        port = rows[1].get_text()
        passwd=rows[2].get_text()
        method=rows[3].get_text()
        proto =rows[4].get_text().strip()
        protoparam=rows[5].get_text().strip()
        obfs = rows[6].get_text().strip()
        obfsparam=rows[7].get_text().strip()
        lat  = int(rows[10].get_text())
        if "已墙" in rows[11].get_text():
            print("BANNED")
            continue
        if lat<240:
            i=[]
            i.append("Other Share "+str(int(time()*100)))
            i.append(server)
            i.append(port)
            i.append(proto)
            i.append(method)
            i.append(obfs)
            i.append(passwd)
            i.append(obfsparam)
            i.append(protoparam)
            Add(i,0)
        else:
            i=[]
            i.append("Others Share "+str(int(time()*100)))
            i.append(server)
            i.append(port)
            i.append(proto)
            i.append(method)
            i.append(obfs)
            i.append(passwd)
            i.append(obfsparam)
            i.append(protoparam)
            Add(i,2)            


html_parser(get_free_html())