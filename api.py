from asyncio.events import new_event_loop
import json , os , traceback, aiohttp
from json import encoder
from lxml import etree

from aiohttp import ClientSession as session
from aiohttp import TCPConnector

api = "https://osu.ppy.sh/api/v2"
sayo = "https://api.sayobot.cn"
bloodcat = "https://api.chimu.moe/cheesegull/search"
ppplus = "https://syrin.me/pp+/u/"
yuziapi = ''
yuziapi1 = ''
token_json = os.path.join(os.path.dirname(__file__) , "token.json")
# print(token_json)

def getTokenJson():
    with open(token_json , encoding="utf-8") as f:
        i = json.load(f)
        client_id = i["client_id"]
        client_secret = i["client_secret"]
        access_token = i["access_token"]
        refresh_token = i["refresh_token"]
    return access_token, refresh_token, client_id, client_secret

async def getApiInfo(project , id = 0 , mode = "osu" , mapid = 0 , setid = 0):
    try:
        if not str(id).isdigit():
            url = f"{api}/users/{id}"
            info = await returnInfo(project , url)
            id = info["id"]
        if project in ["info" , "bind" , "update"]:
            url = f"{api}/users/{id}/{mode}"
        elif project in ["recent" , "pr"]:
            url = f"{api}/users/{id}/scores/recent?mode={mode}"
            if project == "recent":
                url += "&include_fails=1"
        elif project == "score":
            url = f"{api}/beatmaps/{mapid}/scores/users/{id}"
            if mode == "osu":
                url += f"?mode={mode}"
        elif project == "bp":
            url = f"{api}/users/{id}/scores/best?mode={mode}&limit=100"
        elif project == "map":
            url = f"{api}/beatmaps/{mapid}"
        elif project == "rank":
            url = f"{api}/beatmaps/{mapid}/scores"
        else:
            print("Project ERROR")
            return
        return await returnInfo(project , url)
    except:
        return False
    
async def getSayoInfo(project , mode = 1 , status = 1 , keyword = None , setid = 0):
    try:
        if project == "search":
            data = {
                'class' : status,
                'cmd' : 'beatmaplist',
                'keyword' : keyword,
                'limit' : 40,
                'mode' : mode,
                'offset' : 0,
                'type' : 'search'
            }
            url = f"{sayo}/?post"
            data = json.dumps(data)
        elif project == "mapinfo":
            url = f"{sayo}/v2/beatmapinfo?0={setid}"
            data = None
        else:
            print("Project ERROR")
            return
        return await returnInfo(project , url , data)
    except:
        return False

async def getChimuInfo(mode , status , keyword):
    try:
        url = f"{bloodcat}?query={keyword}&amount=10&status={status}&mode={mode}"
        async with session.get(url) as req:
            if req.status != 200:
                return "API请求失败，请稍后再试"
            return await req.json()
    except:
        return False

async def returnInfo(project , url ,data = None):
    try:
        if not data:
            if project != "mapinfo":
                headers = {'Authorization' : f'Bearer {getTokenJson()[0]}'}
            else:
                headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
                async with session.get(url , headers = headers) as req:
                    if req.status != 200:
                        print(req.status)
                        print(url)
                        if project in ["info" , "bind" , "recent" , "pr"]:
                            return "未找到该玩家"
                        elif project == "score":
                            return "未找到该地图"
                        elif project == "bp":
                            return "未找到该玩家BP"
                        elif project == "map":
                            return "未找到该地图"
                        else:
                            return "API请求失败"
                    if project != "mapinfo":
                        return await req.json()
                    return await req.json(content_type = "text/html" , encoding = "utf-8")
        else:
            async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
                async with session.post(url , data = data) as req:
                    print(req.status)
                    if req.status != 200:
                        return "API请求失败"
                    return await req.json()
    except Exception as e:
        return e

async def getAccessToken():
    token = getTokenJson()
    url = "https://osu.ppy.sh/oauth/token"
    data = {
        'grant_type' : 'refresh_token',
        'client_id' : token[2],
        'client_secret' : token[3],
        'refresh_token' : token[1]
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url , data = data) as req:
                if req.status != 200:
                    return "OAuth认证失败"
                newtoken = await req.json()
    except:
        return "OAuth认证失败"
    new_json = {
        'client_id' : token[2],
        'client_secret' : token[3],
        'access_token' : newtoken['access_token'],
        'refresh_token' : newtoken['refresh_token']
    }
    try:
        with open(token_json , "w" , encoding = "utf-8") as f:
            json.dump(new_json , f , ensure_ascii=False , indent=2)
    except:
        traceback.print_exc()
    return "OAuth认证更新完毕"

async def getPPPlus(id):
    url = ppplus + str(id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            html = await req.text()

    etreed = etree.HTML(html)
    try:
        jumpaim = etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[2]/td[2]/text()')[0]
        flowaim = etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[3]/td[2]/text()')[0]
        precision = etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[4]/td[2]/text()')[0]
        speed = etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[5]/td[2]/text()')[0]
        stamina = etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[6]/td[2]/text()')[0]
        accuracy =etreed.xpath('//div[@class="performance-table"]/table/tbody/tr[7]/td[2]/text()')[0]
        return [jumpaim , flowaim , precision , speed , stamina , accuracy]
    except:
        return 'pp+获取失败'

async def getOsuChan(id):
    url = f"https://osuchan.syrin.me/api/profiles/users/{str(id)}/stats/0?user_id_type=username"
    # print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            stat = await req.json()
           
    # return 0,0,0,0,0,0

    acc = round(stat['score_style_accuracy'] , 2)
    bpm = round(stat['score_style_bpm'])
    cs = round(stat['score_style_cs'] , 1)
    ar = round(stat['score_style_ar'] , 1)
    od = round(stat['score_style_od'] , 1)
    length = round(stat['score_style_length'])

    return acc , bpm , cs , ar , od , length

async def getKanonApi(bid, data):
    print('get kanon api')
    url = f'https://api.kanonbot.com/v1/osu/beatmaps/{bid}/calc'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data = data, timeout=30) as req:
                print(req.status)
                if req.status == 500 or req.status == 503:
                    print('500/503')
                    return 'pp计算中'
                elif req.status == 200:
                    r = await req.text()
                    print('SUCCESS')
                    return eval(r)['data']
                else:
                    print('timeout')
                    return 'timeout'
    except:
        return 'asyncio.exceptions.TimeoutError'


async def getYuziApi(bid, data):
    mode = {0: 'osu', 1: 'taiko', 2:'ctb', 3: 'mania'}
    '''
        bid: beatmapid
        data{
            mode: osu, mania, ctb, taiko
            acc: e.g 98.56
            g: great
            b: bad
            m: miss
            mods: 
            c: combo
            }
    '''
    
    osumode = mode[data["mode"]]
    # base = yuziapi + f'{osumode}?o={bid}&c={data["max_combo"]}'
    base = yuziapi1 + f'{osumode}?o={bid}&c={data["max_combo"]}'
    if osumode == 'osu':
        url = base + f'&a={data["accuracy"]}&g={data["ok"]}&b={data["meh"]}&m={data["miss"]}'
    elif osumode == 'taiko':
        url = base + f'&a={data["accuracy"]}&g={data["ok"]}&m={data["miss"]}'
    elif osumode == 'ctb':
        url = base + f'&a={data["accuracy"]}&m={data["miss"]}'
    elif osumode == 'mania':
        url = base + f'&s={data["total_score"]}'
    
    if data['mods']:
        url += f'&mods={data["mods"]}'
    # print(url)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            if req.status != 200:
                return None

            try:
                json = await req.json()
                return json
            except:
                return None
