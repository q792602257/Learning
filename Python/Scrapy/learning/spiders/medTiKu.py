import scrapy
from scrapy.http import Request
import json
import base64
import re

class MedTiKu(scrapy.Item):
    id=scrapy.Field()
    ti=scrapy.Field()
    a=scrapy.Field()
    b=scrapy.Field()
    c=scrapy.Field()
    d=scrapy.Field()
    e=scrapy.Field()
    daan=scrapy.Field()
    jiexi=scrapy.Field()
    leibie=scrapy.Field()
    tiku=scrapy.Field()
    bigLei=scrapy.Field()
    sid=scrapy.Field()

url="http://www.medtiku.com/subject.php?id=69"

def leibie_gen():
    ret=[4,5,6,7,8,10,11,12,13,14,16,17,18,19,20,22,37,69,95,126]
    for i in range(70,95):
        ret.append(i)
    return ret

class MedTiKuCrawler(scrapy.Spider):
    name="medTiKu"
    host="www.medtiku.com"

    def start_requests(self,*args,**kwargs):
        for i in leibie_gen():
            req = Request("http://www.medtiku.com/subject.php?id="+str(i),callback=self.parse_1)
            req.meta['sid']=i
            yield req
    def parse_1(self,response):
        Lei=response.selector.xpath("//div[@class='header-containor']/h1/text()").extract()[0]
        titles = response.selector.xpath("//ul[@class='ogre-list']/li/a/text()").extract()
        hrefs = response.selector.xpath("//ul[@class='ogre-list']/li/a/@href").extract()
        for i in range(len(titles)):
            title=titles[i]
            href=hrefs[i]
            cid = re.findall(r"id=(\d+)&",href)[0]
            req=Request("http://www.medtiku.com/api/ques.php?cid="+str(cid),callback=self.parse_2)
            req.headers["Referer"]="http://www.medtiku.com/quiz.php?id="+str(cid)+"&sid="+str(response.meta['sid'])
            req.headers["X-Requested-With"]="XMLHttpRequest"
            req.meta['title']=title
            req.meta['Lei']=Lei
            req.meta['sid']=response.meta['sid']            
            yield req
    def parse_2(self,response):
        jdata=json.loads(response.body)
        if jdata['status']==1:
            data=json.loads(base64.b64decode(jdata['data']))
        else:
            data=[]
        for i in data:
            item=MedTiKu()
            item['tiku']=response.meta['title']
            item['id']=i["id"]
            item["ti"]=i['title'].replace("\"","“")
            item['a']=i['a'].replace("\"","“")
            item['b']=i['b'].replace("\"","“")
            item['c']=i['c'].replace("\"","“")
            item['d']=i['d'].replace("\"","“")
            item['e']=i['e'].replace("\"","“")
            item['daan']=i['answer'].replace("\"","“")
            item['jiexi']=i['note'].replace("\"","“")
            item["leibie"]=i['type']
            item["bigLei"]=response.meta['Lei']
            item["sid"]=response.meta['sid']
            yield item