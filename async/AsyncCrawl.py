import os
import time
import json
import asyncio

from aiohttp import ClientSession


async def fetch(url, session):
    """
    异步获取请求数据

    :param url: 请求链接
    :param session: Session 实例
    :return: 请求数据
    """
    try:
        async with session.get(url) as response:
            data = response.status
        if data != 404:  # 只返回有效数据
            return url

    except Exception as e:
        print(e)


async def run(start, stop):
    """
    运行主函数

    :param start: range start
    :param stop: range stop
    :return: 请求数据列表
    """
    # url = "https://api.bilibili.com/archive_stat/stat?aid={}"
    url = "http://qn-stastic.duoqin.com/download/ota/OEM_duoqin/PRO_sp9820e2h10/REG_zh/OPE_open/1.0.0/{}package.zip"
    # 创建 Semaphore 实例
    # sem = asyncio.Semaphore(MAX_CONNECT_COUNT)

    # 创建可复用的 Session，减少开销
    async with ClientSession() as session:
        tasks = [
            asyncio.ensure_future(fetch(url.format(i), session))
            for i in range(start, stop)
        ]
        # 使用 gather(*tasks) 收集数据，wait(tasks) 不收集数据
        return await asyncio.gather(*tasks)


async def save_to_files(start, stop, label):
    """
    异步存储数据至文件

    :param start: range start
    :param stop: range stop
    :param path: 文件路径
    :param label: 任务名称
    """
    print(f"Running: job {label}")
    data = await asyncio.gather(asyncio.ensure_future(run(start, stop)))
    result = [d for d in data[0] if d]
    print(result)
    print(f"Fetch data: {len(result)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [save_to_files(1533052800, 1537585054, 'Labeld')]
    loop.run_until_complete(asyncio.gather(*tasks))

