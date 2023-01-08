import datetime

from pydub import AudioSegment
from pydub.audio_segment import AudioSegment

from api import *
from card import *
from file import colorStar, getProjectImage, mapDownload, upload
from mods import *
from sql import *

flags = {
    'A':'🇦','B':'🇧','C':'🇨','D':'🇩','E':'🇪','F':'🇫','G':'🇬',
    'H':'🇭','I':'🇮','J':'🇯','K':'🇰','L':'🇱','M':'🇲','N':'🇳',
    'O':'🇴','P':'🇵','Q':'🇶','R':'🇷','S':'🇸','T':'🇹','U':'🇺',
    'V':'🇻','W':'🇼','X':'🇽','Y':'🇾','Z':'🇿'
}
osu_mods = {
    "4K": "https://img.kaiheila.cn/assets/2021-08/24/G86hJnf5pt01900w.png",
    "5K": "https://img.kaiheila.cn/assets/2021-08/24/DEMNjj2veT01900w.png",
    "6K": "https://img.kaiheila.cn/assets/2021-08/24/qi3BCGpXKc01900w.png",
    "7K": "https://img.kaiheila.cn/assets/2021-08/24/lJdTF76QXX01900w.png",
    "8K": "https://img.kaiheila.cn/assets/2021-08/24/ZcxMoF5A4K01900w.png",
    "9K": "https://img.kaiheila.cn/assets/2021-08/24/d16QXjsswa01900w.png",
    "AP": "https://img.kaiheila.cn/assets/2021-08/24/UpWn1wxSSs00t00u.png",
    "DT": "https://img.kaiheila.cn/assets/2021-08/24/TegH8kcH8Z00w00w.png",
    "EZ": "https://img.kaiheila.cn/assets/2021-08/24/6745KIcYni00w00w.png",
    "FI": "https://img.kaiheila.cn/assets/2021-08/24/5lGGBIcX4000w00w.png",
    "FL": "https://img.kaiheila.cn/assets/2021-08/24/WEoxCDvh7200w00w.png",
    "HD": "https://img.kaiheila.cn/assets/2021-08/24/5Nr6RQbIol00w00w.png",
    "HR": "https://img.kaiheila.cn/assets/2021-08/24/231ZVvIs6200w00w.png",
    "HT": "https://img.kaiheila.cn/assets/2021-08/24/2qkSfOaKDL00w00w.png",
    "MR": "https://img.kaiheila.cn/assets/2021-08/24/gwRcHw7LON00w00w.png",
    "NC": "https://img.kaiheila.cn/assets/2021-08/24/0EAjmBasTH00w00w.png",
    "NF": "https://img.kaiheila.cn/assets/2021-08/24/4I15Bm2LxD00w00w.png",
    "NM": "https://img.kaiheila.cn/assets/2021-08/24/q7cBAzgiEc00w00w.png",
    "PF": "https://img.kaiheila.cn/assets/2021-08/24/siveuLluXc00w00w.png",
    "RX": "https://img.kaiheila.cn/assets/2021-08/24/WdQEuSA1KG01o01n.png",
    "SD": "https://img.kaiheila.cn/assets/2021-08/24/pzmSidFDs600w00w.png",
    "SO": "https://img.kaiheila.cn/assets/2021-08/24/SgmG9gzsDp00w00w.png",
    "TD": "https://img.kaiheila.cn/assets/2021-08/24/1lDWiFdcnw00u00u.png"
}
status = {
    "ranked": "https://img.kaiheila.cn/assets/2021-08/24/mojSFtVhCr03k03k.png",
    "loved": "https://img.kaiheila.cn/assets/2021-08/24/EM1IEcSZJq03k03k.png",
    "approved": "https://img.kaiheila.cn/assets/2021-08/24/T0rt0siC4d03k03k.png",
    'qualified': 'https://img.kaiheila.cn/assets/2021-08/24/T0rt0siC4d03k03k.png',
    "graveyard": "https://img.kaiheila.cn/assets/2021-08/24/YnutIhbXYQ03k03k.png",
    'wip': 'https://img.kaiheila.cn/assets/2021-08/24/YnutIhbXYQ03k03k.png',
    'pending': 'https://img.kaiheila.cn/assets/2021-08/24/YnutIhbXYQ03k03k.png'
}
ranking = {
    "A": "https://img.kaiheila.cn/assets/2021-08/24/dgHYPCcpFq03g01q.png",
    "B": "https://img.kaiheila.cn/assets/2021-08/24/WqoMKqSdYS03g01q.png",
    "C": "https://img.kaiheila.cn/assets/2021-08/24/kgfw32J6Gn03g01q.png",
    "D": "https://img.kaiheila.cn/assets/2021-08/24/OzS1w7hhvR03g01q.png",
    "F": "https://img.kaiheila.cn/assets/2021-08/24/r3mbUMxNxI03g01q.png",
    "S": "https://img.kaiheila.cn/assets/2021-08/24/3oSKxAlJRl03g01q.png",
    "SH": "https://img.kaiheila.cn/assets/2021-08/24/eangu6qc7o03f01q.png",
    "X": "https://img.kaiheila.cn/assets/2021-08/24/WybzjQ1Rav03g01q.png",
    "XH": "https://img.kaiheila.cn/assets/2021-08/24/EZGszN31qZ03g01q.png"
}
beatmap_status = {
    'fruits' : 'https://img.kaiheila.cn/assets/2021-08/hKKvcWTHYG0rs0rs.png',
    'mania' : 'https://img.kaiheila.cn/assets/2021-08/vyRb7w1Bgz0rs0rs.png',
    'osu' : 'https://img.kaiheila.cn/assets/2021-08/YRLap3CaH30rs0rs.png',
    'taiko' : 'https://img.kaiheila.cn/assets/2021-08/ft5Yli9Nrf0rs0rs.png'
}

color = {0 : "#EA669E" , 1 :"#E44116" , 2:"#71368A" , 3:"#66CCFF"}
FGM = {'osu' : 0 , 'taiko' : 1 , 'fruits' : 2 , 'mania' : 3, 'std' : 1, 'fruit' : 2, 'ctb' : 2}
GM = {0 : 'osu', 1 : 'taiko', 2 : 'fruits', 3 : 'mania'}
sayo = {'osu':1 , 'taiko':2 , 'fruits':4 , 'mania':8 , 
'ranked':1 , 'approved':1 , 'qualified':2 , 'loved':4 , 'pending':8 , 'wip':8 , 'graveyard':16
}
sayostatus = {1:'ranked', 2:'qualified', 4:'loved', -1:'wip', -2:'graveyard', 0:'pending'}
dictlist = ['a','b','c','d','e','f','g','h','i','j']

class scorejson:
    def __init__(self , info):
        print(type(info))
        self.acc = round(info['accuracy'] * 100 , 2)
        self.mods = info['mods']
        self.score = info['score']
        self.combo = info['max_combo']
        self.isfc = info['perfect']
        self.count = info['statistics']
        self.c300 = self.count['count_300']
        self.c100 = self.count['count_100']
        self.c50 = self.count['count_50']
        self.cmiss = self.count['count_miss']
        self.cgeki = self.count['count_geki']
        self.ckatu = self.count['count_katu']
        self.rank = info['rank']
        self.createtime = info['created_at'].replace("T" , " ")[:-1]
        self.startTime = datetime.datetime.strptime(self.createtime, "%Y-%m-%d %H:%M:%S")
        self.playTime = (self.startTime + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        self.pp = info['pp']
        self.mode = info['mode']
        self.score = format(self.score , ',')
        if self.pp == None:
            self.pp = 0
        self.pp = round(self.pp , 2)
        # if len(str(self.acc).split('.')[1]) == 1:
        #     self.acc = str(self.acc)[:-1] + '0'
        try:
            accsp = str(self.acc).split('.')
            if len(accsp[1]) == 1:
                self.acc = str(self.acc) + '0'
        except:
            self.acc = str(self.acc) + '.00'


class beatmap():
    def __init__(self , info , map = False):
        if not map:
            self.beatmap = info['beatmap']
        else:
            self.beatmap = info
        self.stars = self.beatmap['difficulty_rating']
        self.mapid = self.beatmap['id']
        self.status = self.beatmap['status']
        self.length = self.beatmap['total_length']
        self.difficult = self.beatmap['version']
        self.od = self.beatmap['accuracy']
        self.ar = self.beatmap['ar']
        self.setid = self.beatmap['beatmapset_id']
        self.bpm = self.beatmap['bpm']
        self.circle = self.beatmap['count_circles']
        self.slider = self.beatmap['count_sliders']
        self.spinner = self.beatmap['count_spinners']
        self.cs = self.beatmap['cs']
        self.hp = self.beatmap['drain']


class beatmapset():
    def __init__(self , info):
        self.beatmapset = info['beatmapset']
        self.artist = self.beatmapset['artist']
        self.artist_unicode = self.beatmapset['artist_unicode']
        self.cover = self.beatmapset['covers']['list@2x']
        self.musicover = self.beatmapset['covers']['card@2x']
        self.searchcover = self.beatmapset['covers']['slimcover@2x']
        self.creator = self.beatmapset['creator']
        self.mp3 = 'https:' + self.beatmapset['preview_url'].replace("\\" , "")
        self.source = self.beatmapset['source']
        self.title = self.beatmapset['title'].replace('"', '\\"')
        self.title_unicode = self.beatmapset['title_unicode'].replace('"', '\\"')
        self.sid = self.beatmapset['id']


class bp():
    def __init__(self , info):
            self.weight = info['weight']
            self.percent = round(self.weight['percentage'])
            self.pp_after = round(self.weight['pp'] , 2)


class user():
    def __init__(self , info):
        self.user = info['user']
        self.username = self.user['username']
        self.avatar = self.user['avatar_url']
        self.id = self.user['id']
        self.profile = f'https://osu.ppy.sh/users/{self.id}'


async def getMaxCombo(mapid):
    # print(mapid)
    mapinfo = await getApiInfo('map' , mapid = mapid)
    maxcombo = mapinfo['max_combo']
    # print(maxcombo)
    return maxcombo


def modText(mods):
    mod = ""
    for i in mods:
        mod += f'''{{
            "type": "image",
            "src":"{osu_mods[i]}"
            }},'''
    return mod


def infoCalc(n1 , n2 , rank=False , pp=False , acc=False):
    num = n1 - n2
    if num <0:
        if rank:
            return f'(↑{str(num * -1)})'
        elif pp:
            return f'(↓{str(round(abs(num) , 2))} pp)'
        elif acc:
            return f'(↓{str(round(abs(num) , 2))} %)'
        else:
            return f'(↓{str(num * -1)})'
    elif num > 0:
        if rank:
            return f'(↓{str(num)})'
        elif pp:
            return f'(↑{str(round(num , 2))} pp)'
        elif acc:
            return f'(↑{str(round(num , 2))} %)'
        else:
            return f'(+{str(round(num , 2))})'
    else:
        return "(-)"


async def infoCard(bot , osu_id , mode = 0):
    
    info = await getApiInfo('info' , id = osu_id , mode = GM[mode])
    if not info:
        return False
    elif isinstance(info, str):
        return False
    country = ""
    esql = osusql()
    try:
        icon = info['avatar_url']
    except:
        icon = 'avatar-guest.png'
    country_code = info['country_code']
    if country_code != "TW":
        for i in country_code:
            country += flags[i]
    else:country = ":tw:"
    friends = info['follower_count']
    uid = info['id']
    supporter = info['is_supporter']
    robot = info['is_bot']
    name = info['username']
    cover = info['cover_url']
    play = info['statistics']
    level = play['level']
    current = level['current']
    progress = level['progress']
    grank = play['global_rank'] if play['global_rank'] else 0
    pp = round(play['pp'], 2)
    acc = round(play['hit_accuracy'], 2)
    pc = play['play_count']
    play_time = play['play_time']
    if play_time == None:play_time = 0
    play_time = time_change(play_time)
    g_counts = play['grade_counts']
    ssh = str(g_counts['ssh']) if len(str(g_counts['ssh'])) != 1 else str(g_counts['ssh']) + '  '
    ss = str(g_counts['ss']) if len(str(g_counts['ss'])) != 1 else str(g_counts['ss']) + '  '
    sh = str(g_counts['sh']) if len(str(g_counts['sh'])) != 1 else str(g_counts['sh']) + '  '
    s = str(g_counts['s']) if len(str(g_counts['s'])) != 1 else str(g_counts['s']) + '  '
    a = str(g_counts['a']) if len(str(g_counts['a'])) != 1 else str(g_counts['a']) + '  '
    # crank = play['country_rank'] if play['country_rank'] else 0
    crank = play.get('country_rank', 0)
    if supporter:
        spt = ":heart: "
    else:spt = ":black_heart: "
    if robot:
        isbot = ":robot:"
    else:isbot = ""

    # upload assets
    iconpath = await getProjectImage('icon' , icon , uid=uid)
    iconurl = await upload(bot, iconpath)
    coverpath = await getProjectImage('usercover' , cover , uid=uid)
    coverurl = await upload(bot, coverpath)

    result = esql.get_all_newinfo(uid , mode)
    if result:
        for i in result:
            n_crank = infoCalc(crank , i[2], rank = True)
            n_grank = infoCalc(grank , i[3], rank = True)
            n_pp = infoCalc(pp , i[4], pp = True)
            n_acc = infoCalc(acc, i[5], acc = True)
            n_pc = infoCalc(pc, i[6])
    else:
        n_crank, n_grank, n_pp, n_acc, n_pc = '', '', '', '', ''

    infomsg = f'''[
    {{
        "type": "card",
        "theme": "secondary",
        "color": "{color[mode]}",
        "size": "lg",
        "modules": [
        {{
            "type": "header",
            "text": {{
                "type": "plain-text",
                "content": "{name} {spt}{isbot}{country}\\t#{grank}{n_grank}\\tLevel:{current}({progress}%)"
            }}
        }},
        {{
            "type": "context",
            "elements": [{{
                "type": "image",
                "src":"{beatmap_status[GM[mode]]}"
            }},
            {{
              "type" : "kmarkdown",
              "content" : "{GM[mode]} | {friends}个关注者 | [主页](https://osu.ppy.sh/users/{uid})"
            }}]
        }},
        {{
            "type": "divider"
        }},
        {{
            "type": "container",
            "elements": [
            {{
                "type": "image",
                "src": "{coverurl}"
            }}
            ]
        }},
        {{
            "type": "divider"
        }},
        {{
            "type": "section",
            "text": {{
            "type": "plain-text",
            "content": "国内/区域排名\\t#{crank}{n_crank}\\npp\\t\\t\\t{pp} pp{n_pp}\\n准确率\\t\\t{acc} %{n_acc}\\n游戏次数\\t\\t{pc}{n_pc}\\nplay time\\t\\t{play_time}"
            }},
            "mode": "right",
            "accessory": {{
            "type": "image",
            "src": "{iconurl}",
            "size": "sm"
            }}
        }},
        {{
            "type": "divider"
        }},
        {{
            "type": "context",
            "elements": [
            {{
                "type": "image",
                "src": "{ranking['XH']}"
            }},
            {{
                "type": "plain-text",
                "content": "{ssh}\\t"
            }},
            {{
                "type": "image",
                "src": "{ranking['X']}"
            }},
            {{
                "type": "plain-text",
                "content": "{ss}\\t"
            }},
            {{
                "type": "image",
                "src": "{ranking['SH']}"
            }},
            {{
                "type": "plain-text",
                "content": "{sh}\\t"
            }},
            {{
                "type": "image",
                "src": "{ranking['S']}"
            }},
            {{
                "type": "plain-text",
                "content": "{s}\\t"
            }},
            {{
                "type": "image",
                "src": "{ranking['A']}"
            }},
            {{
                "type": "plain-text",
                "content": "{a}"
            }}
            ]
        }}
        ]
    }}
    ]'''
    return infomsg


def time_change(time):
    day = int(time / 86400)
    hour = int((time - (day*86400)) / 3600)
    mine = int((time % 3600) / 60)
    return f"{day}d {hour}h {mine}m"


def map_time_change(time):
    hour = int(time / 3600)
    mine = int((time % 3600) / 60)
    sec = int(time % 60)
    if len(str(sec)) == 1:
        sec = "0" + str(sec)
    if not hour:
        if not mine:
            return f"{sec}s"
        return f"{mine}:{sec}"
    if mine < 10:
        return f"{hour}:0{mine}:{sec}"
    return f"{hour}:{mine}:{sec}"


def set_mod_list(json, mods):
    vnum =[]
    for index, v in enumerate(json):
        if v['mods']:
            num = get_mods_num(v['mods'])
            if num == mods:
                vnum.append(index)
    return vnum


async def scoreCard(bot , project, id, mode, **kwargs):
    # try:
    if project in ['recent', 'pr']:
        info = await getApiInfo(project, id, GM[mode])
        if not info:
            # return '未查询到最近游玩的记录'
            return False , None
        elif isinstance(info, str):
            print(info)
            return '404' , None
        else:
            score = scorejson(info[0])
            bmap = beatmap(info[0])
            bmapset = beatmapset(info[0])
            play_user = user(info[0])
        ranktext = ''
    elif project == 'score':
        if not kwargs['mapid']:
            title , artist , creator , version = kwargs['title'], kwargs['artist'], kwargs['creator'], kwargs['version']
            data , _ = await search(title , artist , creator , version , status=7)
            if isinstance(data , str):
                return data , None
            elif isinstance(data ,list):
                mapid = 0
                setID = data[0]['sid']
                mapdata = await getSayoInfo('mapinfo' , setid = setID)
                lenth = mapdata['data']['bids_amount']
                mapdata = mapdata['data']['bid_data']
                mapdata.sort(key=lambda x: x['star'] , reverse=True)
                for i in range(lenth):
                    mapidt = mapdata[i]['bid']
                    mapinfo = await getApiInfo(project , id , mode , mapid = mapidt)
                    if mapinfo != '未找到该地图':
                        mapid = mapidt
                        break
                if not mapid:
                    return '找不到成绩' , None
            elif isinstance(data , dict):
                mapid = data['bid']
                if not mapid:
                    mapid = 0
                    setID = data['sid']
                    mapdata = await getSayoInfo('mapinfo' , setid = setID)
                    lenth = mapdata['data']['bids_amount']
                    mapdata = mapdata['data']['bid_data']
                    mapdata.sort(key=lambda x: x['star'] , reverse=True)
                    for i in range(lenth):
                        mapidt = mapdata[i]['bid']
                        mapinfo = await getApiInfo(project , id , mode , mapid = mapidt)
                        if mapinfo != '未找到该地图':
                            mapid = mapidt
                            break
                    if not mapid:
                        return '找不到成绩' , None
        else:
            mapid = kwargs['mapid']

        info = await getApiInfo(project, id = id ,mapid = mapid)
        beatmapinfo = await getApiInfo('map' , mapid=mapid)
        if not info:
            return '未查询到该地图的成绩' , None
        elif isinstance(info, str):
            return '未查询到该玩家的成绩' , None
        else:
            if not kwargs['rank']:
                score = scorejson(info['score'])
                bmap = beatmap(info['score'])
                grank = info['position']
                bmapset = beatmapset(beatmapinfo)
                play_user = user(info['score'])
            else:
                info = await getApiInfo('rank' , mapid = mapid)
                grank = kwargs['rank']
                score = scorejson(info['scores'][grank - 1])
                bmap = beatmap(beatmapinfo , map = True)
                bmapset = beatmapset(beatmapinfo)
                play_user = user(info['scores'][grank - 1])

        ranktext = f" | #{grank}"

    else:
        return False , None

    maxcombo = await getMaxCombo(bmap.mapid)
    data = {
        'mode': FGM[score.mode],
        'max_combo': score.combo,
        # 'great': score.c300,
        'ok': score.c100,
        'meh': score.c50,
        'miss': score.cmiss,
    }
    
    # data['accuracy'] = eval(score.acc) / 100 if isinstance(score.acc, str) else score.acc / 100
    data['accuracy'] = score.acc
    if '+'.join(score.mods):
        data['mods'] = '+'.join(score.mods)
    else:
        data['mods'] = None

    if score.mode == 'mania':
        data['total_score'] = eval(score.score.replace(',' , ''))

    smod = False
    for i in ['HR', 'EZ', 'DT', 'NC', 'HT']:
        if i in score.mods:
            smod = True
            break

    ar = bmap.ar
    od = bmap.od
    cs = bmap.cs
    hp = bmap.hp
    stars = bmap.stars
    pp = int(score.pp)
    req = await getYuziApi(bmap.mapid, data)
    if score.pp == 0 or smod:
        # req = await getKanonApi(bmap.mapid, data)
        if isinstance(req, dict):
            if score.pp == 0:
                pp = round(req['pp'])
                # pp = int(req['PPInfo']['Total'])
            if smod:
                ar = req['mapinfo']['ar_rating']
                od = req['mapinfo']['od_rating']
                # cs = round(req['CS'], 1)
                # hp = round(req['HP'], 1)
                stars = req['mapinfo']['star_rating']
        else:
            print(req)
    else:
        pp = int(score.pp)


    ifpp_n = '-'
    pp_ls_n = ['-', '-', '-', '-', '-', '-']
    if score.mode in ['osu', 'taiko']:
        # data['is_more'] = True
        # req = await getKanonApi(bmap.mapid, data)
        if isinstance(req, dict):
            ifpp_n = round(req['ifpp'])
            pp_ls_n = []
            for i in req['accpp']:
                pp_ls_n.append(round(i))

    speed_arr , ar_arr , od_arr , cs_arr , hp_arr , star_arr = "" , "" , "" , "" , "" , ""
    if 'DT' in score.mods or 'NC' in score.mods:
        speed_arr = "↑"
        speed = 1.5
    elif 'HT' in score.mods:
        speed_arr = "↓"
        speed = 0.5
    else:
        speed = 1

    if ar > bmap.ar:
        ar_arr = "△"
    elif ar < bmap.ar:
        ar_arr = "▽"
    if od > bmap.od:
        od_arr = "△"
    elif od < bmap.od:
        od_arr = "▽"
    if cs > bmap.cs:
        cs_arr = "△"
    elif cs < bmap.cs:
        cs_arr = "▽"
    if hp > bmap.hp:
        hp_arr = "△"
    elif hp < bmap.hp:
        hp_arr = "▽"

    if score.mods == []:
        mods = ["NM"]
    else:mods = score.mods
    if not bmapset.source:
        lbracket = ""
        rbracket = ""
    else:
        lbracket = "("
        rbracket = ")"
    
    if stars > bmap.stars:
        star_arr = "↑"
    elif stars < bmap.stars:
        star_arr = "↓"
    

    # dl
    iconpath = await getProjectImage('icon' , play_user.avatar , uid= play_user.id)
    mapcardpath = await getProjectImage('list' , bmapset.cover , uid= bmapset.sid)

    # upload
    iconurl = await upload(bot , iconpath)
    mapcardurl = await upload(bot , mapcardpath)

    modeurl = await colorStar(bot, GM[mode], bmap.stars)
    
    if mode < 2:
        if mode == 0:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300}**/ {score.c100}/ {score.c50}/ {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / **{maxcombo}x**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
        else:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300 + score.cgeki}**/ {score.c100 + score.ckatu}/ {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / **{maxcombo}x**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
    else:
        if mode == 2:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n[**{score.c300}**/ {score.c100}/ {score.ckatu}/ {score.cmiss}]"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo}x / {maxcombo}x"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "{pp} **pp**\\n**Score** {score.score}"
                        }}
                    ]
                }}
            }}'''
        else:
            game_result = f'''{{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "Rank **{score.rank}**\\n{pp} **pp**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**{score.acc}%**\\n{score.combo} **combo**"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**Score** {score.score}"
                        }}
                    ]
                }}
                }},
                {{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "**max** : {score.cgeki}\\n**300** : {score.c300}"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**200** : {score.ckatu}\\n**100** : {score.c100}"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**  50  **: {score.c50}\\n**miss** : {score.cmiss}"
                        }}
                    ]
                }}
            }}'''
    if mode == 3:
        iffc = "max pp"
    else:iffc = "if fc"

    scoremsg = f"""[
    {{
        "type": "card",
        "theme": "secondary",
        "color": "{color[FGM[score.mode]]}",
        "size": "lg",
        "modules": [
            {{
            "type": "header",
            "text": {{
                "type": "plain-text",
                "content": "{bmapset.source}{lbracket}{bmapset.artist_unicode}{rbracket} - {bmapset.title_unicode}[{bmap.difficult}]"
                }}
            }},
            {{
                "type": "context",
                "elements": [
                    {{
                        "type": "plain-text",
                        "content": "{bmapset.artist} - {bmapset.title} | "
                    }},
                    {{
                        "type": "image",
                        "src": "{iconurl}"
                    }},
                    {{
                        "type": "kmarkdown",
                        "content": "[{play_user.username}]({play_user.profile})"
                    }}
                ]
            }},
            {{
                "type": "context",
                "elements": [
                    {{
                        "type": "image",
                        "src":"{modeurl}"
                    }},
                    {{
                        "type": "plain-text",
                        "content": " | "
                    }},
                    {{
                        "type": "image",
                        "src": "{status[bmap.status]}"
                    }},
                    {{
                        "type": "plain-text",
                        "content": " | "
                    }},
                    {{
                        "type": "image",
                        "src": "{ranking[score.rank]}"
                    }},
                    {{
                        "type": "plain-text",
                        "content": " | mods:"
                    }},
                    {modText(mods)}
                    {{
                        "type": "plain-text",
                        "content": " | {score.playTime}{ranktext}"
                    }}
                ]
            }},
            {{
                "type": "divider"
            }},
            {{
                "type": "section",
                "text": {{
                    "type": "plain-text",
                    "content": "▸作者: {bmapset.creator} ▸BeatmapID: {bmap.mapid}\\n▸长度: {map_time_change(bmap.length/speed)} {speed_arr} ▸BPM: {round(bmap.bpm*speed)} {speed_arr} ▸物件数: {bmap.circle + bmap.slider + bmap.spinner}\\n▸圈数: {bmap.circle} ▸滑条数: {bmap.slider} ▸转盘数: {bmap.spinner}\\n▸CS:{cs}{cs_arr} ▸AR:{ar}{ar_arr} ▸OD:{od}{od_arr} ▸HP:{hp}{hp_arr} ▸Stars:{stars}{star_arr}★"
                }},
                "mode": "right",
                "accessory": {{
                    "type": "image",
                    "src": "{mapcardurl}",
                    "size": "sm"
                }}
            }},
            {{
                "type": "divider"
            }},
            {game_result},
            {{
                "type": "divider"
            }},
            {{
                "type": "section",
                "text": {{
                    "type": "paragraph",
                    "cols": 3,
                    "fields": [
                        {{
                            "type": "kmarkdown",
                            "content": "**{iffc}** : {ifpp_n}pp\\n**95%** : {pp_ls_n[0]}pp"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**97%** : {pp_ls_n[2]}pp\\n**98%** : {pp_ls_n[3]}pp"
                        }},
                        {{
                            "type": "kmarkdown",
                            "content": "**99%** : {pp_ls_n[4]}pp\\n ***SS***   : {pp_ls_n[5]}pp"
                        }}
                    ]
                }}
            }},
            {{
                "type": "divider"
            }},
            {{
                "type": "section",
                "text": {{
                "type": "kmarkdown",
                "content": "下载地址：[ppy](https://osu.ppy.sh/beatmapsets/{bmap.setid}#osu/{bmap.mapid}) | [sayobot](https://dl.sayobot.cn/beatmaps/download/novideo/{bmap.setid}) | [chimu](https://api.chimu.moe/v1/download/{bmap.setid}?n=1) | [btct](https://beatconnect.io/b/{bmap.setid}) | [nerina](https://nerina.pw/d/{bmap.setid})"
                }}
            }},
            {{
                "type": "audio",
                "title": "{bmapset.title_unicode}",
                "src": "{bmapset.mp3}",
                "cover": "{mapcardurl}"
            }}
            ]
        }}
        ]"""
    return scoremsg , bmap.mapid
    # except Exception as e:
        # print(f'Error: {e}')


async def bpCard(bot, project , id , mode , bpmin = 1 , bpmax = 5): # project = bp
    try:
        info = await getApiInfo(project , id , GM[mode])
        if not info:
            return False
        elif isinstance(info , str):
            print(info)
            return '404'
    
    except Exception as e:
        return f'Error: {e}'

    
    minbp = info[bpmin - 1]
    score = scorejson(minbp)
    bmap = beatmap(minbp)
    bmapset = beatmapset(minbp)
    bpp = bp(minbp)
    if score.mods == []:
        mods = ['NM']
    else:mods = score.mods

    maplistpath = await getProjectImage('list', bmapset.cover , bmapset.sid)
    maplisturl = await upload(bot, maplistpath)
    modeurl = await colorStar(bot, GM[mode], bmap.stars)

    bpmsg = f'''[{{
    "type": "card",
    "theme": "secondary",
    "color": "{color[mode]}",
    "size": "lg",
    "modules": [{cardBp(score,bmap,bmapset,bpp , bpmin , await getMaxCombo(bmap.mapid) , modeurl , ranking , modText(mods) , mode , maplisturl)}'''
    
    if bpmin != bpmax:
        for num in range(bpmin , bpmax):
            infobp = info[num]

            score = scorejson(infobp)
            bmap = beatmap(infobp)
            bmapset = beatmapset(infobp)
            bpp = bp(infobp)
            if score.mods == []:
                mods = ['NM']
            else:mods = score.mods

            maplistpath = await getProjectImage('list', bmapset.cover , bmapset.sid)
            maplisturl = await upload(bot, maplistpath)

            bpmsg += f''',{cardBp(score,bmap,bmapset,bpp , num + 1 , await getMaxCombo(bmap.mapid) , modeurl , ranking , modText(mods) , mode, maplisturl)}'''

    bpmsg_end = bpmsg[:-23] + "]}]"
    return bpmsg_end


async def bpToday(bot, project , id , mode):
    try:
        info = await getApiInfo(project , id , GM[mode])
        if info == 'iderror':
            return 'iderror'
        if not info:
            return False
        elif isinstance(info , str):
            print(info)
            return '404'
    
    except Exception as e:
        return f'Error: {e}'

    now = datetime.datetime.now()
    # end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = now - datetime.timedelta(days=1)
    todaybp = []

    leninfo = len(info)
    for i in range(leninfo):
        creat_time = info[i]['created_at'].replace('T' , ' ')[:-6]
        startTime = datetime.datetime.strptime(creat_time , "%Y-%m-%d %H:%M:%S")
        playTime = startTime + datetime.timedelta(hours = 8)
        if playTime > start_time and playTime < now:
            todaybp.append(i)

    if not len(todaybp):
        return False
    if len(todaybp) > 10:
        numlist = todaybp[:10]
    else:
        numlist = todaybp
    
    bpmemsg = cardHead(mode)

    for num in numlist:
        score = scorejson(info[num])
        bmap = beatmap(info[num])
        bmapset = beatmapset(info[num])
        bpp = bp(info[num])
        if score.mods == []:
            mods = ["NM"]
        else:mods = score.mods
        if not bmapset.source:
            lbracket = ""
            rbracket = ""
        else:
            lbracket = "("
            rbracket = ")"

        maplistpath = await getProjectImage('list', bmapset.cover , bmapset.sid)
        maplisturl = await upload(bot, maplistpath)
        modeurl = await colorStar(bot, GM[mode], bmap.stars)

        if mode == 3:
            result = f'''{{
              "type": "kmarkdown",
              "content": "      **BP{num + 1}**\\n\\n    **{score.score}**"
            }},
            {{
              "type": "kmarkdown",
              "content": "**{score.acc}%**\\n{score.combo}x\\n{bmap.stars}★"
            }},
            {{
              "type": "kmarkdown",
              "content": "**{score.pp} PP**\\nweight: {bpp.percent}%\\n{bpp.pp_after} pp"
            }}'''
        else:
            result = f'''{{
                "type": "kmarkdown",
                "content": "\\n     **BP{num + 1}**\\n"
            }},
            {{
                "type": "kmarkdown",
                "content": "**{score.acc}%**\\n{score.combo}x / **{await getMaxCombo(bmap.mapid)}x**\\n{bmap.stars}★"
            }},
            {{
                "type": "kmarkdown",
                "content": "**{score.pp} PP**\\nweight: {bpp.percent}%\\n{bpp.pp_after} pp"
            }}'''

        bpmemsg += f'''{{
            "type": "header",
            "text": {{
            "type": "plain-text",
            "content": "{bmapset.source}{lbracket}{bmapset.artist_unicode}{rbracket} - {bmapset.title_unicode}[{bmap.difficult}]"
            }}
        }},
        {{
            "type": "section",
            "text":{{
                "type": "paragraph",
                "cols": 3,
                "fields": [{result}
                ]
            }},
            "mode": "right",
            "accessory": {{
                "type": "image",
                "src": "{maplisturl}",
                "size": "sm"
            }}
        }},
        {{
            "type": "context",
            "elements": [
                {{
                    "type": "image",
                    "src": "{modeurl}"
                }},
                {{
                    "type": "plain-text",
                    "content": " | "
                }},
                {{
                    "type": "image",
                    "src": "{ranking[score.rank]}"
                }},
                {{
                    "type": "plain-text",
                    "content": " | mods: "
                }},
                {modText(mods)}
                {{
                    "type": "plain-text",
                    "content": " | {score.playTime}"
                }}
            ]
        }},
            {{
                "type": "section",
                "text" : {{
                "type": "kmarkdown",
                "content": "下载地址：[ppy](https://osu.ppy.sh/beatmapsets/{bmap.setid}#osu/{bmap.mapid}) | [sayobot](https://dl.sayobot.cn/beatmaps/download/novideo/{bmap.setid}) | [chimu](https://api.chimu.moe/v1/download/{bmap.setid}?n=1) | [btct](https://beatconnect.io/b/{bmap.setid}) | [nerina](https://nerina.pw/d/{bmap.setid})"
                }}
            }},{{"type": "divider"}},'''

    mebpmsg = bpmemsg[:-23] + "}]}]"
    # with open(r'C:\Users\Administrator\Desktop\khl\bpme.json' , 'w' , encoding = 'utf-8') as f:
    #     f.write(mebpmsg)

    return mebpmsg


async def search(title , artist , creator , version , mode=1 , status=1):
    while True:
        req = await getSayoInfo("search" , mode , status , title)
        # print(req)
        if type(req) == dict:
            break
        elif req == 'API请求失败':
            return 'sayobot API请求失败', None
    print(type(req))
    if req['status'] == -1:
        return "无搜索结果" , None
    if isinstance(req , dict):
        data = req['data']
        lenth = len(data)
        if lenth:
            data.sort(key=lambda x: x['favourite_count'] , reverse=True)

        if creator:
            for i in data:
                # print(creator.lower() , i['creator'].lower())
                if creator.lower() == i['creator'].lower():
                    if version:
                        req_new = await getSayoInfo('mapinfo' , setid = i['sid'])
                        data_new = req_new['data']['bid_data']
                        for j in data_new:
                            if version.lower() == j['version'].lower():
                                return {'sid':i['sid'] , 'bid' : j['bid']} , None
                    else:return {'sid':i['sid'], 'bid':None} , None
        
        elif version:
            for i in data:
                req_new = await getSayoInfo('mapinfo', setid=i['sid'])
                data_new = req_new['data']['bid_data']
                for j in data_new:
                    if version.lower() == j['version'].lower():
                        return {'sid':i['sid'] , 'bid' : j['bid']} , None
        
        else:
            data_ori = data.copy()
            for i in range(lenth-1 , -1 , -1):
                # print(i)
                if title.lower() not in data[i]['title'].lower() and data[i]['title'].lower() not in title.lower():
                    titleU = data[i]['titleU']
                    if titleU:
                        if title not in data[i]['titleU'] and data[i]['titleU'] not in title:
                            data.pop(i)
                    else:
                        data.pop(i)
            if not data:
                data = data_ori
            
            if artist:
                lenth = len(data)
                for i in range(lenth -1 , -1 , -1):
                    if artist.lower() not in data[i]['artist'].lower() and data[i]['artist'].lower() not in artist.lower():
                        artistU = data[i]['artistU']
                        if artistU:
                            if artist not in data[i]['artistU'] and data[i]['artistU'] not in artist:
                                data.pop(i)
                        else:
                            data.pop(i)

            if not data:
                return '未查询到地图' , None
            else:
                return data , len(data)
    return '未查询到地图' , None


async def musicCard(bot, title , artist , creator , version , mapid = None):
    if mapid:
        mapid = mapid
        mapinfo = await getApiInfo('map' , mapid = mapid)
        try:
            info = beatmapset(mapinfo)
            setID = info.sid
            mapdata = await getSayoInfo('mapinfo' , setid = setID)
            filename = mapdata['data']['bid_data'][0]['audio']
        except:
            return mapinfo
    else:
        data , _ = await search(title , artist , creator , version , mode = 15 , status = 31)
        print('music search over')
        if isinstance(data , str):
            return data
        elif isinstance(data , list):
            setID = data[0]['sid']
            while True:
                mapdata = await getSayoInfo('mapinfo' , setid = setID)
                if type(mapdata) == dict:
                    break
            mapid = mapdata['data']['bid_data'][0]['bid']
            filename = mapdata['data']['bid_data'][0]['audio']
            mapinfo = await getApiInfo('map' , mapid = mapid)
            if isinstance(mapinfo, str):
                return mapinfo
            info = beatmapset(mapinfo)
        elif isinstance(data , dict):
            setID , mapid = data['sid'], data['bid']
            mapdata = await getSayoInfo('mapinfo' , setid = setID)
            filename = mapdata['data']['bid_data'][0]['audio']
            mapinfo = await getApiInfo('map' , mapid = mapid)
            if isinstance(mapinfo, str):
                return mapinfo
            info = beatmapset(mapinfo)

    print('start downloading')
    musicpath = await mapDownload(setID) + '/' + filename
    if filename[-3:] == "ogg":
        print("开始转换")
        musicpath = oggToMp3(musicpath)
        print("转换结束")
        
    mp3_url = 'http://dl.omoipro.xyz/' + '/'.join(musicpath.split('/')[-3:])
    mp3_url.replace(' ', '%20')
    print(mp3_url)
    # mp3_url = await upload(bot , musicpath)
    # else:
    # mp3_url = f'https://dl.sayobot.cn/beatmaps/files/{setID}/{filename}'.replace(' ' , '%20')

    # if filename[-3:] == 'ogg':
    #     musicpath = await mapDownload(setID) + '/' + filename
    #     print('start ogg2mp3')
    #     musicpath = oggToMp3(musicpath)
    #     print('ogg2mp3 over')
    #     mp3_url = await upload(bot, musicpath)
    # else:
    #     mp3_url = f'http://dl.sayobot.cn/beatmaps/files/{setID}/{filename}'.replace(' ' , '%20')

    if not info.source:
        lbracket = ""
        rbracket = ""
    else:
        lbracket = "("
        rbracket = ")"

    # dl
    maplistcover = await getProjectImage('list' , info.cover , uid=info.sid)
    if not maplistcover:
        listurl = 'https://tupian.li/images/2021/07/05/mapbg.png'
    else:
        listurl = await upload(bot, maplistcover)
    mapcardcover = await getProjectImage('card' , info.musicover , uid = info.sid)
    if not mapcardcover:
        cardurl = 'https://tupian.li/images/2021/07/05/mapbg.png'
    else:
        cardurl = await upload(bot,mapcardcover)

    musicmsg = f'''[
  {{
    "type": "card",
    "theme": "secondary",
    "color": "#F1C40F",
    "size": "lg",
    "modules": [
      {{
        "type": "header",
        "text": {{
          "type": "plain-text",
          "content": "{info.source}{lbracket}{info.artist_unicode}{rbracket} - {info.title_unicode}"
        }}
      }},
      {{
        "type": "container",
        "elements": [
          {{
            "type": "image",
            "src": "{cardurl}"
          }}
        ]
      }},
      {{
        "type": "divider"
      }},
      {{
        "type": "section",
        "text" : {{
            "type": "kmarkdown",
            "content": "下载地址：[ppy](https://osu.ppy.sh/beatmapsets/{setID}#osu/{mapid}) | [sayobot](https://dl.sayobot.cn/beatmaps/download/novideo/{setID}) | [chimu](https://api.chimu.moe/v1/download/{setID}?n=1) | [btct](https://beatconnect.io/b/{setID}) | [nerina](https://nerina.pw/d/{setID})"
            }}
      }},
      {{
        "type": "audio",
        "title": "{info.title}",
        "src": "{mp3_url}",
        "cover": "{listurl}"
      }}
    ]
  }}]'''

    return musicmsg


def oggToMp3(filepath):
    song = AudioSegment.from_file(filepath, "ogg")
    filename = filepath.split(".")[0]
    song.export(f"{filename}.mp3", format="mp3")
    return(f"{filename}.mp3")


async def ppp(bot, name:list):
    results = []
    if name[1] == 'None':
        info = await getApiInfo('info' , name[0])
        if not info:
            return False
        icon = info['avatar_url']
        path = await getProjectImage('icon', icon , uid=info['id'])
        iconurl = await upload(bot, path)
        user_name = info['username']
        data = await getPPPlus(user_name) # jumpaim , flowaim , precision , speed , stamina , accuracy
        if isinstance(data , str):
            return data
        osuacc , bpm , cs , ar , od , length = await getOsuChan(user_name)
        length = map_time_change(length)
        pppmsg = f'''[
  {{
    "type": "card",
    "theme": "secondary",
    "color": "{color[0]}",
    "size": "lg",
    "modules": [
      {{
        "type": "section",
        "text": {{
          "type": "kmarkdown",
          "content": "*{user_name}的pp+数据*\\n**Aim(Jump):**\\t{data[0]}\\n**Aim(Flow):**\\t{data[1]}\\n**Precision:**\\t{data[2]}\\n**Speed:**\\t\\t{data[3]}\\n**Stamina:**\\t\\t{data[4]}\\n**Accuracy:**\\t{data[5]}"
        }},
        "mode": "right",
        "accessory": {{
          "type": "image",
          "src": "{icon}",
          "size": "lg"
        }}
      }},
      {{
        "type": "divider"
      }},
      {{
        "type": "section",
        "text": {{
          "type": "paragraph",
          "cols": 3,
          "fields": [
            {{
              "type": "kmarkdown",
              "content": "**Accuracy: **{osuacc}%\\n**最佳BPM: **{bpm}"
            }},
            {{
              "type": "kmarkdown",
              "content": "**最佳长度: **{length}\\n**最佳CS: **{cs}"
            }},
            {{
              "type": "kmarkdown",
              "content": "**最佳AR: **{ar}\\n**最佳OD: **{od}"
            }}
          ]
        }}
      }}
    ]
  }}]'''
        return pppmsg
    else:
        # for i in name:
        #     jumpaim , flowaim , precision , speed , stamina , accuracy = await getPPPlus(i)
        #     result_list = {"锐角移动能力":int(jumpaim[:-2]),
        #     "间距连打能力":int(flowaim[:-2]),
        #     "点击精准度":int(accuracy[:-2]),
        #     "长串稳定能力":int(stamina[:-2]),
        #     "整体手速能力":int(speed[:-2]),
        #     "小圈精准度":int(precision[:-2])}
        #     results.append(result_list)
        return "vs功能还没做完qwq"


async def searchSid(bot , title , artist , creator , version , startid=0):        
    # start = int(round(time.time() * 1000) + 120000)
    data , lenthg = await search(title , artist , creator , version , mode = 15 , status = 15)
    if lenthg:
        page = int(startid / 5) + 1
        pageall = int(lenthg / 5)
        if lenthg % 5:
            pageall += 1
        setmsg = f'''[
        {{
        "type": "card",
        "theme": "secondary",
        "color": "#98C379",
        "size": "lg",
        "modules": [
        {{
            "type": "context",
            "elements": [
            {{
                "type": "plain-text",
                "content": "{title}的搜索结果: (第{page}页 / 共{pageall}页)"
            }}
            ]
        }},
        {{
            "type": "divider"
        }},'''
        if isinstance(data , str):
            return data
        elif isinstance(data , dict):
            setID = data['sid']
            return int(setID)
        elif isinstance(data , list):
            mapdict = {}
            lenth = len(data)
            if lenth > startid + 5:
                end = startid + 5
            else:end = lenth
            for i in range(startid, end):
                # print(i)
                setID = data[i]['sid']
                mapinfo = await getSayoInfo('mapinfo' , setid = setID)
                if isinstance(mapinfo , str):
                    continue
                info = mapinfo['data']
                beatmaps = info['bid_data']
                beatmaps.sort(key=lambda x: x['star'] , reverse=False)
                mapstatus = sayostatus[info['approved']]
                diffmsg = f'''{{
                    "type": "context",
                    "elements": [
                        {{
                        "type": "image",
                        "src": "{status[mapstatus]}"
                        }},
                        {{
                        "type": "plain-text",
                        "content": " | "
                        }},'''
                mapslenth = len(beatmaps)
                # for beatmap in beatmaps:
                for m in ['osu', 'taiko', 'fruits', 'mania']:
                    for j in range(mapslenth):
                        if j == 8:
                            break
                        mode = GM[beatmaps[j]['mode']]
                        if mode == m:
                            star = beatmaps[j]['star']
                            modeurl = await colorStar(bot, mode, star)
                            diffmsg += f'''{{"type": "image","src": "{modeurl}"}},'''
                diffmsg = diffmsg[:-1] + ']},'
                coverurl = f'https://cdn.sayobot.cn:25225/beatmaps/{setID}/covers/cover.jpg'
                path = await getProjectImage('card', coverurl , uid=setID)
                if not path:
                    coverurl = 'https://tupian.li/images/2021/07/05/mapbg.png'
                else:coverurl = await upload(bot , path)
                if not info['source']:
                    lbracket = ""
                    rbracket = ""
                else:
                    lbracket = "("
                    rbracket = ")"
                
                artist = info['artistU'] if info['artistU'] else info['artist']
                title = info['titleU'] if info['titleU'] else info['title']

                setmsg += f'''{{
            "type": "container",
            "elements": [
            {{
                "type": "image",
                "src": "{coverurl}"
            }}
            ]
        }},
        {{
            "type": "header",
            "text": {{
            "type": "plain-text",
            "content": "{info['source']}{lbracket}{artist}{rbracket} - {title}"
            }}
        }},
        {diffmsg}
        {{
            "type": "section",
            "text": {{
            "type": "plain-text",
            "content": "▸作图者: {info['creator']}"
            }},
            "mode": "right",
            "accessory": {{
            "type": "button",
            "theme": "success",
            "value": ".search -sid {setID}",
            "click": "return-val",
            "text": "sid: {setID}"
            }}
        }},{{"type": "divider"}},'''
                mapdict[dictlist[i]] = setID
            if startid == 0 and lenthg <= startid + 5:
                setr = setmsg[:-23] + "}]}]"
            elif startid == 0 and lenthg > startid + 5:
                setr = setmsg + '''{
                "type": "action-group",
                "elements": [
                {
                    "type": "button",
                    "theme": "danger",
                    "value": "next",
                    "click": "return-val",
                    "text": {
                    "type": "plain-text",
                    "content": "→下一页"
                    }
                }]}]}]'''
            elif startid !=0 and lenthg <= startid + 5:
                setr = setmsg + '''{
                "type": "action-group",
                "elements": [
                {
                    "type": "button",
                    "theme": "primary",
                    "value": "previous",
                    "click": "return-val",
                    "text": {
                    "type": "plain-text",
                    "content": "←上一页"
                    }
                }]}]}]'''
            else:
                setr = setmsg + '''{
                "type": "action-group",
                "elements": [
                {
                    "type": "button",
                    "theme": "primary",
                    "value": "previous",
                    "click": "return-val",
                    "text": {
                    "type": "plain-text",
                    "content": "←上一页"
                    }
                },
                {
                    "type": "button",
                    "theme": "danger",
                    "value": "next",
                    "click": "return-val",
                    "text": {
                    "type": "plain-text",
                    "content": "→下一页"
                    }
                }]}]}]'''
            return setr , mapdict
    else:
        return data, None


async def searchBySid(bot , sid = 0):   
    mapinfo = await getSayoInfo('mapinfo' , setid = sid)
    if isinstance(mapinfo , str):
        return mapinfo
    info = mapinfo['data']
    mapstatus = sayostatus[info['approved']]
    artist = info['artistU'] if info['artistU'] else info['artist']
    title = info['titleU'] if info['titleU'] else info['title']
    coverurl = f'https://cdn.sayobot.cn:25225/beatmaps/{sid}/covers/cover.jpg'
    path = await getProjectImage('card', coverurl , uid=sid)
    if not path:
        # coverurl = 'https://osu.sayobot.cn/assets/img/home/nobg.jpg'
        coverurl = 'https://tupian.li/images/2021/07/05/mapbg.png'
    else:coverurl = await upload(bot, path)
    if not info['source']:
        lbracket = ""
        rbracket = ""
    else:
        lbracket = "("
        rbracket = ")"
    mapmsg = f'''[
  {{
    "type": "card",
    "theme": "secondary",
    "color": "#98C379",
    "size": "lg",
    "modules": [
      {{
        "type": "header",
        "text": {{
          "type": "plain-text",
          "content": "{info['source']}{lbracket}{artist}{rbracket} - {title}"
        }}
      }},
      {{
        "type": "container",
        "elements": [
          {{
            "type": "image",
            "src": "{coverurl}"
          }}
        ]
      }},
      {{
        "type": "divider"
      }},'''
    beatmaps = info['bid_data']
    lenth = len(beatmaps)
    if lenth:
        beatmaps.sort(key=lambda x: x['star'] , reverse=False)
        for m in ['osu', 'taiko', 'fruits', 'mania']:
            for i in beatmaps:
                bid = i['bid']
                stars = round(i['star'], 2)
                mode = GM[i['mode']]
                if mode == m:
                    version = i['version']
                    od = i['OD']
                    ar = i['AR']
                    cs = i['CS']
                    hp = i['HP']
                    maplenth = i['length']
                    maplenth = map_time_change(maplenth)
                    modeurl = await colorStar(bot, mode, stars)

                    mapmsg += f'''{{
                            "type": "section",
                            "text": {{
                            "type": "kmarkdown",
                            "content": "> ▸难度: {version} ▸BeatmapID: {bid}\\n▸CS: {cs} ▸AR: {ar} ▸OD: {od} ▸HP: {hp} ▸Stars:{stars}★"
                            }},
                            "mode": "left",
                            "accessory": {{
                            "type": "image",
                            "src": "{modeurl}",
                            "size": "sm"
                            }}
                        }},
                        {{
                            "type": "divider"
                        }},'''
        map1 = await getApiInfo('map' , mapid = bid)
        if isinstance(map1 , str):
            return map1
        setinfo = beatmapset(map1)
        mp3coverpath = await getProjectImage('list' , setinfo.cover , uid = sid)
        if mp3coverpath:
            mp3coverurl = await upload(bot , mp3coverpath)
        else:
            mp3coverurl = 'https://tupian.li/images/2021/07/05/osu_logo.png'
        mapmsg += f'''{{
                "type": "section",
                "text": {{
                "type": "kmarkdown",
                "content": "下载地址：[ppy](https://osu.ppy.sh/beatmapsets/{sid}) | [sayobot](https://dl.sayobot.cn/beatmaps/download/novideo/{sid}) | [chimu](https://api.chimu.moe/v1/download/{sid}?n=1) | [btct](https://beatconnect.io/b/{sid}) | [nerina](https://nerina.pw/d/{sid})"
                }}
            }},
            {{
                "type": "audio",
                "title": "{setinfo.title_unicode}",
                "src": "{setinfo.mp3}",
                "cover": "{mp3coverurl}"
            }}
            ]
        }}
        ]'''

    return mapmsg
