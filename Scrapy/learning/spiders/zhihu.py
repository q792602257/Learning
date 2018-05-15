import scrapy
from scrapy.http import Request
import json

class ZhihuDailyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()
    date=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()

class ZhihuDaily(scrapy.Spider):
    name="zhihu"
    host = 'news-at.zhihu.com'
    start_urls=["http://news-at.zhihu.com/api/4/news/latest"]

    def start_requests(self,*args,**kwargs):
        yield Request("http://news-at.zhihu.com/api/4/news/latest",callback=self.parse_1)

    def parse_1(self,response):
        data=json.loads(response.body)
        date=data['date']
        for i in data["stories"]:
            url = "http://news-at.zhihu.com/api/4/news/"+str(i['id'])
            title=i['title']
            req=Request(url,callback=self.parse_2)
            req.meta["date"]=date
            yield req

    def parse_2(self,response):
        data=json.loads(response.body)
        item=ZhihuDailyItem()
        item['id']=data['id']
        item['content']=data['body']
        item['date']=response.meta['date']
        item['title']=data['title']
        yield item
