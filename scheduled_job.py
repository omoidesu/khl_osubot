import time , aiohttp, asyncio
from api import getAccessToken
from funcs import user
from sql import osusql


esql = osusql()

async def update_token():
    while True:
        msg = await getAccessToken()
        if msg == "OAuth认证更新完毕":
            now = time.strftime("%H:%M:%S")
            break
    return f"<{now}> token update success"

async def update_sql():
    result = esql.get_all_id()
    for n , uid in enumerate(result):
        await user(uid[0] , True)
    now = time.strftime("%H:%M:%S")
    return f"<{now}> sql update success"

async def run():
    now = time.strftime("%H:%M")
    while True:
        while now != "02:00":
            now = time.strftime("%H:%M")
            print(now)
            time.sleep(60)
        print(await update_token())
        print(await update_sql())
        timenow = time.strftime("%Y-%M-%d %H:%M:%S")
        print(f"<{timenow}> update success")
        time.sleep(24*3600)

tasks = [run()]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))