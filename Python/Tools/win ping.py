import subprocess    
import re

class LinkState(object):
    def __init__(self,ip):
        self.ip = ip
        self.getLinkState(self.ip)

    def getLinkState(self,ip):
        #运行ping程序
        p = subprocess.Popen(["ping.exe", ip], 
             stdin = subprocess.PIPE, 
             stdout = subprocess.PIPE, 
             stderr = subprocess.PIPE, 
             shell = True)  

        #得到ping的结果
        out = p.stdout.read()
        #把Bytes类型转换成Str
        out = bytes.decode(out)
        #找出丢包率，通过'%'匹配
        packetLossRateList = re.findall(r'\w*%\w*',out)
        self.packetLossRate = packetLossRateList[0]

        #找出往返时间，通过'ms'匹配
        timeList = re.findall(r'\w*ms',out)
        self.minTime = timeList[-3]
        self.maxTime = timeList[-2]
        self.averageTime = timeList[-1]


if __name__ == '__main__':
    ip = 'baidu.com'    #要ping的主机
    a = LinkState(ip)
    print(a.averageTime)