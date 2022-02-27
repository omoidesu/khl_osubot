import aiohttp , os , re , zipfile , shutil , math
from PIL import Image

from aiohttp import TCPConnector


osufile = os.path.join(os.path.dirname(__file__) , 'osufile')
# mapfile = os.path.join(osufile , 'map')
mapfile = '/root/hgame/music'
iconfile = os.path.join(osufile , 'icon')
usercover = os.path.join(osufile , 'usercover')
maplist = os.path.join(osufile , 'maplist')
mapcard = os.path.join(osufile , 'mapcard')
colorstar = os.path.join(osufile, 'color')

async def mapDownload(mapid , DL = False):
    mapid = str(mapid)

    # 判断文件是否存在
    if not DL:
        for file in os.listdir(mapfile):
            if mapid in file:
                if os.path.exists(os.path.join(mapfile , file)):
                    return os.path.join(mapfile , file)
    
    # url = f'https://txy1.sayobot.cn/beatmaps/download/novideo/{mapid}'
    # url = f'https://api.chimu.moe/v1/download/{mapid}?n=1'
    url = f'https://beatconnect.io/b/{mapid}'
    # try:
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url , allow_redirects = False) as req:
    #             sayo = req.headers['Location']
    # except:
    #     print('请求失败/超时')
    #     return

    # if DL:
    #     filename = await get_osz(sayo , mapid , True)
    #     return os.path.join(mapfile , filename) , filename

    # filename = await get_osz(sayo , mapid)
    filename = await get_osz(url , mapid)
    filepath = os.path.join(mapfile , filename)

    # 解压
    myzip = zipfile.ZipFile(filepath)
    mystr = myzip.filename.split(".")
    myzip.extractall(mystr[0])
    myzip.close()

    removeFile(filepath[:-4])
    os.remove(filepath)
    return filepath[:-4]

async def get_osz(sayo , mapid , DL = False):
    try:
        print("Start Download Map")
        async with aiohttp.ClientSession() as session:
            async with session.get(sayo) as req:
                filename = f'{mapid}.osz'
                if DL:
                    filename = req.content_disposition.filename
                chunk = await req.read()
                open(os.path.join(mapfile , filename) , 'wb').write(chunk)
        print('Map Download Complete')
        return filename

    except:
        print('Map Download Failed')
        return

def removeFile(path):
    s = []
    for file in os.listdir(path):
        if '.osu' in file:
            # bg = get_pic_music('pic' , os.path.join(path , file))
            # if bg not in s:
            #     s.append(bg)
            music = getMusic('music' , os.path.join(path , file))
            if music not in s:
                s.append(music)
            s.append(file)

    for root , dir , files in os.walk(path , topdown = False):
        for name in files:
            if name not in s:
                os.remove(os.path.join(root , name))
        for dirname in dir:
            shutil.rmtree(os.path.join(root , dirname))

    return True

def getMusic(project , path):
    sre = r'AudioFilename:(.+)'
    with open(path , 'r' , encoding='utf-8') as f:
        text = f.read()
    result = re.search(sre , text)
    return result.group(1).strip()

def getFile(path , mapid , version):
    for file in os.listdir(path):
        if '.osu' in file:
            with open(os.path.join(path , file) , 'r' , encoding='utf-8') as f:
                text = f.read()
            result = re.search(r'BeatmapID:(.+)' , text)
            if result:
                rmapid = result.group(1)
                if str(mapid) == rmapid:
                    filepath = os.path.join(path , file)
                    return filepath
            ver = re.search(r'Version:(.+)' , text)
            if ver:
                mapver = ver.group(1)
                if version == mapver:
                    filepath = os.path.join(path , file)
                    return filepath

async def getProjectImage(project , url , uid=0):
    uid = str(uid)
    if project == 'icon':
        name = f'{uid}_icon.png'
        path = os.path.join(iconfile , name)
    elif project == 'usercover':
        name = f'{uid}_cover.png'
        path = os.path.join(usercover , name)
    elif project == 'list':
        name = f'{uid}_list@2x.png'
        path = os.path.join(maplist , name)
    elif project == 'card':
        name = f'{uid}_card@2x.png'
        path = os.path.join(mapcard , name)

    # if os.path.exists(path):
    #     return path

    try:
        if 'avatar-guest.png' in url:
            url = 'https://osu.ppy.sh/images/layout/avatar-guest.png'
        # print('get image')
        async with aiohttp.ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(url) as req:
                if req.status != 200:
                    print(req.status)
                    return False
                chunk = await req.read()
                open(path , 'wb').write(chunk)
        return path
    except Exception as e:
        print(e)
        return e

async def upload(bot , path):
    asset = await bot.upload_asset(path)
    url = asset['url']
    return url

async def colorStar(bot, mode, stars):
    # print('start draw color')
    '''mode: osu, taiko, fruits, mania'''
    stars = round(stars, 2)
    path = colorstar + '/' + mode + '/' + f'{stars}.png'
    if not os.path.exists(path):
        default = 115
        if 0 <= stars < 1:
            xp = 0
            default = 120
        elif 1 <= stars < 2:
            xp = 120
            default = 120
        elif 2 <= stars < 3:
            xp = 240
        elif 3 <= stars < 4:
            xp = 355
        elif 4 <= stars < 5:
            xp = 470
        elif 5 <= stars < 6:
            xp = 585
        elif 6 <= stars < 7:
            xp = 700
        elif 7 <= stars < 8:
            xp = 815
        else:
            if mode == 'osu':
                return 'https://img.kaiheila.cn/assets/2021-08/F23yrEJKXR0dw0dw.png'
            elif mode == 'taiko':
                return 'https://img.kaiheila.cn/assets/2021-08/LNETy7CryN0dw0dw.png'
            elif mode == 'fruits':
                return 'https://img.kaiheila.cn/assets/2021-08/38JlboF4L70dw0dw.png'
            elif mode == 'mania':
                return 'https://img.kaiheila.cn/assets/2021-08/ZpbkNfUxqo0dw0dw.png'

        # 取色
        x = (stars - math.floor(stars)) * default + xp
        color = Image.open(os.path.join(osufile, 'color', 'color.png')).load()
        r, g, b = color[x, 1]
        # 打开底图
        im = Image.open(os.path.join(osufile, 'color', f'{mode}.png')).convert('RGBA')
        xx, yy = im.size
        # 填充背景
        sm = Image.new('RGBA', im.size, (r, g, b))
        sm.paste(im, (0, 0, xx, yy), im)
        # 把白色变透明
        for i in range(xx):
            for z in range(yy):
                data = sm.getpixel((i, z))
                if (data.count(255) == 4):
                    sm.putpixel((i, z), (255, 255, 255, 0))

        sm.save(path)
    url = await upload(bot, path)
    return url


# colorStar('osu', 7.27)