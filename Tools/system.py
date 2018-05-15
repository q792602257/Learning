import requests
import json
import psutil as ps
import os
import re
from time import sleep,time
while True:
    _n={}
    _nR=ps.net_io_counters(True)
    for _t1 in _nR:
        if _nR[_t1].bytes_sent==0 and _nR[_t1].bytes_recv==0:
            continue
        _n[_t1]={
            'sB':_nR[_t1].bytes_sent,
            'rB':_nR[_t1].bytes_recv,
            'sP':_nR[_t1].packets_sent,
            'rP':_nR[_t1].packets_recv,
        }
    _d={}
    _dR=ps.disk_partitions(True)
    for _t2 in _dR:
        try:
            if ps.disk_usage(_t2.mountpoint).total==0:
                continue
            _d[_t2.mountpoint]={
                'total':ps.disk_usage(_t2.mountpoint).total,
                'used':ps.disk_usage(_t2.mountpoint).used,
                'free':ps.disk_usage(_t2.mountpoint).free,
            }
        except:
            pass
    _p=[]
    a = os.popen('last').readlines()
    for _t3 in a:
        b = re.findall(r'(.+?) +(.+?) +(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) +(.+?) [\- ] (.+?) +\(?(.+?)\)? ',_t3)
        if len(b) == 0:
            continue
        _p.append({
            'user' :b[0][0],
            'pts'  :b[0][1],
            'ip'   :b[0][2],
            'start':b[0][3],
            'stop' :b[0][4],
            'hold' :b[0][5],
        })
    data={
        'cpu':{
            'count':ps.cpu_count(),
            'percent':ps.cpu_percent(percpu=True),
            'stats':{
                'system':ps.cpu_times_percent().system,
                'user':ps.cpu_times_percent().user,
                'idle':ps.cpu_times_percent().idle,
            },
        },
        'mem':{
            'total':ps.virtual_memory().total,
            'avail':ps.virtual_memory().available,
            'free':ps.virtual_memory().free,
            'used':ps.virtual_memory().used,
            'swap':{
                'total':ps.swap_memory().total,
                'free':ps.swap_memory().free,
                'used':ps.swap_memory().used,
            },
        },
        'disk':{
            'partitions':_d,
            'io':{
                'r':ps.disk_io_counters().read_count,
                'w':ps.disk_io_counters().write_count,
                'rB':ps.disk_io_counters().read_bytes,
                'wB':ps.disk_io_counters().write_bytes,
            },
        },
        'network':{
            'per':_n,
            'total':{
                'sB':ps.net_io_counters().bytes_sent,
                'rB':ps.net_io_counters().bytes_recv,
                'sP':ps.net_io_counters().packets_sent,
                'rP':ps.net_io_counters().packets_recv,
            }
        },
        'login':_p,
        'boot':ps.boot_time(),
        'time':time(),
    }
    data=json.dumps(data)
    a = requests.post("url",data=data)
    # print(a.text)
    sleep(120)
    # break