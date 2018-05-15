import asyncio
import aiohttp
import time
import json
from fake_useragent import UserAgent

headers={"User-Agent":UserAgent().firefox}

async def getHtml(url):
    async with aiohttp.ClientSession() as session:
        print("->  ",time.time())
        async with session.get(url,headers=headers) as r:
            print("  ->",time.time())
            Parse(await r.text())

def Parse(text):
    print("<---",time.time())
    # try:
    #     json.loads(text)
    # except:
    #     print(text)

loop = asyncio.get_event_loop()
task = [getHtml("https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(i)) for i in range(5,60)]
loop.run_until_complete(asyncio.wait(task))
# print(headers)