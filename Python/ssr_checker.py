import requests
import os
import pymysql as mysql

port="65432"
times=5
full_path="/root/shadowsocksr/shadowsocks/local.py"
con=mysql.connect(host="localhost",port=3306,user='root',password='Bd960912',db='jerry',charset='utf8')
cursor=con.cursor()   
def Get():
    cursor.execute("SELECT `name`,`server`,`port`,`protocol`,`method`,`obfs`,`keys`,`obfsparam`,`protoparam` FROM `ssr` WHERE `Check` < SUBDATE(NOW(), INTERVAL 3 HOUR) AND `isValid` = 1 UNION SELECT `name`,`server`,`port`,`protocol`,`method`,`obfs`,`keys`,`obfsparam`,`protoparam` FROM `ssr` WHERE `Check` > SUBDATE(NOW(), INTERVAL 12 HOUR) AND `isValid` = 0 ;")
    data = cursor.fetchall()
    return data
def Update(i,Result):
    t_bsql="UPDATE `jerry`.`ssr` SET `isValid` = {isValid},`Check` = NOW() WHERE `server` = '{server}' AND `port` = '{port}' AND `protocol` = '{protocol}' AND `method` = '{method}' AND `obfs` = '{obfs}' AND `keys` = '{keys}' AND `obfsparam` = '{obfsparam}' AND `protoparam` = '{protoparam}';"
    f_bsql="UPDATE `jerry`.`ssr` SET `isValid` = {isValid} WHERE `server` = '{server}' AND `port` = '{port}' AND `protocol` = '{protocol}' AND `method` = '{method}' AND `obfs` = '{obfs}' AND `keys` = '{keys}' AND `obfsparam` = '{obfsparam}' AND `protoparam` = '{protoparam}';"
    if Result:
        sql=t_bsql.format(server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7],isValid=Result)
    else:
        sql=f_bsql.format(server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7],isValid=Result)
    cursor.execute(sql)
    con.commit()
def Run(i):
    bparam='-b 127.0.0.1 -l {lport} -s "{server}" -p "{port}" -k "{keys}" -m "{method}" -O "{protocol}" -o "{obfs}" -G "{protoparam}" -g "{obfsparam}" -d start'
    param = bparam.format(lport=port,server=i[1],port=i[2],keys=i[6],method=i[4],protocol=i[3],obfs=i[5],protoparam=i[8],obfsparam=i[7])
    os.system(full_path+" "+param)
    # print(full_path+" "+param)
def Kill(i):
    bparam='-s "{server}" -p "{port}" -d stop'
    param=bparam.format(server=i[1],port=i[2])
    os.system(full_path+" "+param)
    # print(full_path+" "+param)
def Test():
    proxy={
        "http":"socks5://127.0.0.1:"+port,
        "https":"socks5://127.0.0.1:"+port
    }
    try:
        requests.get("http://google.com",proxies=proxy,allow_redirects=False,timeout=5)
        return True
    except:
        return False
def Check():
    fail=0
    for __ in range(times):
        if Test():
            continue
        else:
            fail+=1
    if fail > times * 0.5:
        return False
    else:
        return True
def Main():
    data=Get()
    for i in data:
        Run(i)
        if Check():
            print("PASS:\t"+i[0])
            Update(i,True)
        else:
            print("FAIL:\t"+i[0])
            Update(i,False)
        Kill(i)
    # print(Check())
Main()
