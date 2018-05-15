#coding:utf8
import requests
from time import sleep
from time import time
import json
from datetime import datetime
from bs4 import BeautifulSoup as Soup
import pymysql as mysql
import random
import re

All_Method=["none","aes-128-ctr","aes-192-ctr","aes-256-ctr",'aes-128-cfb','aes-192-cfb','aes-256-cfb','rc4','rc4-md5','rc4-md5-6','aes-128-cfb8','aes-192-cfb8','aes-256-cfb8','salsa20','chacha20','xsalsa20','xchacha20','chacha20-ietf']
All_Protocol=['origin','verify_deflate','auth_sha1_v4','auth_aes128_md5','auth_aes128_sha1','auth_chain_a','auth_chain_b','auth_chain_c','auth_chain_d','auth_chain_e','auth_chain_f']
All_Obfs=['plain','http_simple','http_post',"random_head",'tls1.2_ticket_auth','tls1.2_ticket_fastauth']
s=requests.Session()
proxy={
    "http":"socks5://127.0.0.1:1080",
    "https":"socks5://127.0.0.1:1080"
}
def code_getter():
    p=s.get("https://tool.ssrshare.com/tool/share_ssr",proxies=proxy)
    soup=Soup(p.text,"html.parser")
    print(p.headers)
    for i in soup.select("script"):
        if 'subkey' in i.get_text().strip():
            al=i.get_text().strip()
            break
    # a = re.findall("'(.+)';",al)
    return '1524240000_66_aqs'
    # return a[0]
con=mysql.connect(host="localhost",port=3306,user='root',password='Bd960912',db='jerry',charset='utf8')
cursor=con.cursor()
def get_share_html():
    url="https://tool.ssrshare.com/tool/api/share_ssr?key=%s&page=1&limit=200"%(code_getter())
    p=s.get(url,proxies=proxy)
    return p.text
def get_free_html():
    url="https://tool.ssrshare.com/tool/api/free_ssr?key=%s&page=1&limit=200"%(code_getter())
    p=s.get(url,proxies=proxy)
    return p.text
def Add(i,isK=1):
    if i[1]=="" or i[2]=="" or i[3]=="" or i[4]=="" or i[5]=="" or i[6]=="":
        print(i)
        print("ERROR")
        return False
    I_bsql="INSERT INTO `ssr` (`name`,`server`,`port`,`protocol`,`method`,`obfs`,`keys`,`obfsparam`,`protoparam`,`isKey`) VALUES ('{name}','{server}','{port}','{protocol}','{method}','{obfs}','{keys}','{obfsparam}','{protoparam}','{isK}');"
    Q_bsql="SELECT COUNT(1) FROM `ssr` WHERE `server` = '{server}' AND `port` = '{port}'"
    Q_sql=Q_bsql.format(server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7])
    cursor.execute(Q_sql)
    print(i)
    if cursor.fetchall()[0][0] > 0:
        print("EXIST")
        return False
    I_sql=I_bsql.format(name=i[0],server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7],isK=isK)
    cursor.execute(I_sql)
    con.commit()
    print("OK")
    return True
def html_parser(html):
    data=json.loads(html)
    for row in data['data']:
        if (datetime.now()-datetime.strptime(row['data'], "%Y-%m-%d %H:%M:%S")).seconds > 3600*18:
            print(row)
            print("Too Long Not Check")
            continue
        if row["status"]!='true' or row["m_station_cn_status"]!="true":
            print(row)
            print("BANNED")
            continue            
        latency = row['m_station_cn_ms']
        server  = row['server']
        port    = row['server_port']
        passwd  = row['password']
        method  = row['method']
        proto   = row['protocol']
        if proto=='origin':
            protop  = ""
        elif row['protocolparam']=='null' or row['protocolparam']==None or row['protocolparam']=="None":
            protop  = ""
        else:
            protop  = row['protocolparam']
        obfs    = row['obfs']
        if obfs=='plain':
            obfsp   = ""
        elif row['obfsparam']=='null' or row['obfsparam']==None or row['obfsparam']=="None":
            obfsp   = ""
        else:
            obfsp   = row['obfsparam']
        if latency<200:
            i=["Other "+str(latency)+"ms "+str(int(time()*100)),server,port,proto,method,obfs,passwd,obfsp,protop]
            Add(i,1)
        else:
            i=["Others "+str(latency)+"ms "+str(int(time()*100)),server,port,proto,method,obfs,passwd,obfsp,protop]
            Add(i,[0,2][random.randint(0,1)])

html_parser(get_share_html())
html_parser(get_free_html())