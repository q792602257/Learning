from threading import Thread
import queue
import requests
from time import sleep
import sys
import json

DownQ = queue.Queue()
ParseQ = queue.Queue()

def getHtml(url):
    _p = requests.get(url)
    return _p.text

def worker():
    while True:
        try:
            _a = DownQ.get()
        except queue.Empty:
            continue
        # print(_a['id'])
        if _a['url']=="END":
            ParseQ.put_nowait({"id":_a['id'],"url":_a["url"],"data":"END"})
            break
        html = getHtml(_a["url"])
        ParseQ.put_nowait({"id":_a['id'],"url":_a["url"],"data":html})

def parser():
    while True:
        sleep(0.005)
        try:
            _a = ParseQ.get()
        except queue.Empty:
            continue
        if _a['data']=="END":
            break
        try:
            json.loads(_a["data"])
        except:
            print(_a['id'])
        # print(_a['data'])

def main():
    for i in range(1,1000):
        DownQ.put_nowait({"id":i,"func":"getHtml","url":"https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(i)})
    DownQ.put_nowait({"id":0,"func":"QUIT","url":"END"})

class MainThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name="Main Thread"
    def run(self):
        print("-> %s <- RUNNING"%(self.name))
        main()

class DownloadThread(Thread):
    def __init__(self,ID):
        Thread.__init__(self)
        self.name="Download Thread %d"%(ID)
    def run(self):
        print("-> %s <- RUNNING"%(self.name))
        worker()

class ParseThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name="Parse Thread"
    def run(self):
        print("-> %s <- RUNNING"%(self.name))
        parser()

MainThread().start()
for _i in range(0,16):
    DownloadThread(_i).start()
ParseThread().start()
while DownQ.qsize() > 0 or ParseQ.qsize() > 0:
    sleep(0.5)
    print("Download Queue : %5d | Parse Queue : %5d"%(DownQ.qsize(),ParseQ.qsize()),end="\r"*40)
