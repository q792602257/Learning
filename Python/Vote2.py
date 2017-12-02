import requests
import json
import datetime

s=requests.Session()
h={
	"Connection":"Keep-Alive",
}
url = "https://www.wjx.cn/handler/processjq.ashx?curid=18585971&starttime=%s&source=directphone&submittype=1&rn=663012162.38318390&t=%d" % (
    datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000))
data = "submitdata=1$1}2$2}3$1}4$2}5$2}6$2}7$3}8$2}9$3}10$2"
page = s.post(url,headers=h,data=data)
print(page.text)
