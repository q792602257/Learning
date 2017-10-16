#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import threadpool
import time

def sayhello(str):
    print "Hello %s"%str
    time.sleep(2)
start_time = time.time()
name_list =['00','77','aa','bb','cc','1','2','3','4','5','6']
pool = threadpool.ThreadPool(10) 
requests = threadpool.makeRequests(sayhello, name_list) 
[pool.putRequest(req) for req in requests] 
pool.wait() 
print '%.3fs'% (time.time()-start_time)