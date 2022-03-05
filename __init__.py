
import json
import re

from api import *
from cardmsg_renew import *
from funcs import *
from khl import Bot, Cert, TextMsg
from khl.message import BtnTextMsg
from sql import osusql

FGM = {'osu' : 0 , 'taiko' : 1 , 'fruits' : 2 , 'mania' : 3, 'std' : 1, 'fruit' : 2, 'ctb' : 2, 'catch': 2}
GM = {0 : 'osu', 1 : 'taiko', 2 : 'fruits', 3 : 'mania'}
GMN = {0 : 'Std', 1 : 'Taiko', 2 : 'Ctb', 3 : 'Mania'}
mode_ls = (0, 1, 2, 3)
mode_lsn = ('osu', 'taiko', 'fruits', 'mania', 'ctb', 'fruit', 'catch')

with open("./config/config.json" , "r" , encoding="utf-8") as f:
    config = json.load(f)
# init Cert and Bot

cert = Cert(client_id=config["client_id"], client_secret=config["client_secret"], token=config["token"])
bot = Bot(cmd_prefix=['.'], cert=cert)

helptxt = '''1️⃣ `bind` `osu name` 绑定osu账号
2️⃣ `info` `osu name(可选)` `:mode(可选)`查询个人信息
3️⃣ `setmode` `:num` 更改默认模式
4️⃣ `pr` / `recent` `osu name(可选)` `:mode(可选)` 查询24小时内最近pass / failed成绩
5️⃣ `bp` 查询bp1~5(best performance)
    └可选参数:
        ├`osu name` 同上
        ├`num` 查询指定bp，`num`不大于50
        ├`num1`~`num2` 限定查询上下限，`num1`与`num2`相差不大于5
        └`:mode` 同上
6️⃣ `bpme` `:mode(可选)`查询今日新bp
7️⃣ `socre` `beatmap title` / `-id beatmapID`查询某张地图的最佳成绩
    └可选参数:
        ├`osu name` ; 与`#num`互斥
            例：`score` `vaxei` `,` `tsukinami`
        └`#num` 查询某张地图第num名成绩;num不大于50 ; 与`osu name`互斥
            例: `score` `-id 1872396` `#2`
    注：如果以id模式查询指定玩家成绩，玩家名字后面不加`,`
8️⃣ `pp+` `osu name(可选)` 查询pp+数据
9️⃣ `music` `beatmap title` / `-id beatmapID` 点歌
🔟 `search` `beatmap title` / `-sid beatmapsetID` 搜图
---
`mode`可以为0~3的数字或模式名
    ├**0**:(ins)osu!(ins), **1**:(ins)osu!taiko(ins), **2**:(ins)osu!catch(ins), **3**:(ins)osu!mania(ins)
    └(ins)**osu**(ins) / (ins)**taiko**(ins) / (ins)**fruits** / **fruit** / **catch** / **ctb**(ins) / (ins)**mania**(ins)
`osu name`可换为@某人(`bind`和`bp`除外)
`beatmap title`的完整格式为`artist` `-` `title[version](creator)` , 其中`artist(艺术家)` `version(难度名)` `creator(作图者)`均可省略
---
todo~~咕咕咕~~:
    `pp+` 缺少个人能力雷达图
    `news` osu新闻推送(待定)'''

esql = osusql()
globalbid = {}
globalmode = 0

async def trySendCard(msg , card_msg ,reply = True):
    if len(card_msg) < 20:
        return await msg.reply(card_msg)
    card_error_msg = await msg.reply_card(card_msg) # 输出卡片内容
    print(card_error_msg)
    if card_error_msg == 'success':
        return
    num = 5
    while num:
        try:
            error_msg = card_error_msg[:15]
            if card_error_msg == '卡片消息没有通过验证或者不存在':
                await msg.reply_temp(f'卡片消息没有通过验证或者不存在,正在重试,剩余{num - 1}次')
                if not reply:
                    card_error_msg = await msg.ctx.send_card(card_msg)
                else:
                    card_error_msg = await msg.reply_card(card_msg) # 输出卡片内容
                num -= 1
            elif card_error_msg == 'cURL Error (28)':
                await msg.reply_temp(f'卡片发送失败(cURL Error (28)),正在重试,剩余{num - 1}次')
                if not reply:
                    card_error_msg = await msg.ctx.send_card(card_msg)
                else:
                    card_error_msg = await msg.reply_card(card_msg) # 输出卡片内容
                num -= 1
            else:
                await msg.reply_temp(f'{card_error_msg},正在重试,剩余{num - 1}次')
                if not reply:
                    card_error_msg = await msg.ctx.send_card(card_msg)
                else:
                    card_error_msg = await msg.reply_card(card_msg) # 输出卡片内容
                num -= 1
        except TypeError:
            return card_error_msg
    await msg.reply('卡片发送失败，请重试')
    return None


@bot.command(name = "oauth")
async def OAuth(msg: TextMsg):
    r = await getAccessToken()
    return await msg.reply(r)


@bot.command(name = "bind")
async def bindUser(msg:TextMsg , *wargs):
    khl_id = msg.ctx.user_id
    user_id = ""
    for i in wargs:
        user_id += i + " "
    user_id = user_id[:-1]
    if not user_id:
        return await msg.reply("请输入osu id")
    if esql.get_name_mod(khl_id):
        return await msg.reply("你已经绑定过了")
    message = await bindInfo("bind" , user_id , khl_id)
    if message[:2] == f"用户":
        user_info = await infoCard(bot, user_id, 0)
        if not user_info:
            return await msg.reply('未查询到该玩家')
    else:
        return await msg.reply('未查询到该玩家')
    return await msg.reply('绑定成功')
    # return await msg.ctx.send_card(user_info)


@bot.command(name = 'unbind')
async def unbind(msg:TextMsg):
    khl_id = msg.ctx.user_id
    sel_result = esql.get_id_mod(khl_id)
    if sel_result: 
        del_result = esql.delete_user(khl_id)
        if del_result:
            await msg.reply('解绑成功！')
            esql.delete_newinfo(sel_result[0][0])
        else:
            return await msg.reply('数据库错误')
    else:
        return await msg.reply('尚未绑定，无需解绑')


@bot.command(name = 'info')
async def info(msg:TextMsg, *args):
    at_id = msg.mention
    if not at_id:
        khl_id = msg.ctx.user_id
    else:khl_id = at_id[0]
    result = esql.get_id_mod(khl_id)
    if not args:
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for i in result:
            id = i[0]
            mode = i[1]
    else:
        while '' in args:
            args.remove('')
        mlen = len(args)
        if ':' in args[-1] and mlen == 1:
            id = re.search(".*:", args[0]).group()[:-1]
            if not id:
                for i in result:
                    id = i[0]
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        elif ':' in args[-1]:
            id = ' '.join(args[:mlen-1])
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        else:
            id = ' '.join(args[:mlen])
            if khl_id in id:
                if not result:
                    return await msg.reply('该账号尚未绑定')
                for i in result:
                    id = i[0]
            mode = 0
    card_msg = await infoCard(bot, id, mode)
    if not card_msg:
        return await msg.reply('该玩家不存在')
    # await msg.ctx.send(card_msg)
    await trySendCard(msg, card_msg)
    # await msg.reply_card(card_msg)


@bot.command(name = "recent" , aliases=('r'))
async def recent(msg:TextMsg, *args):
    guild_id = msg.guild_id
    at_id = msg.mention
    if not at_id:
        khl_id = msg.ctx.user_id
    else:khl_id = at_id[0]
    result = esql.get_id_mod(khl_id)
    if not args:
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for i in result:
            id = i[0]
            mode = i[1]
    else:
        while '' in args:
            args.remove('')
        mlen = len(args)
        if ':' in args[-1] and mlen == 1:
            id = re.search(".*:", args[0]).group()[:-1]
            print(id)
            if not id:
                for i in result:
                    id = i[0]
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        elif ':' in args[-1]:
            id = ' '.join(args[:mlen-1])
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        else:
            id = ' '.join(args[:mlen])
            if khl_id in id:
                if not result:
                    return await msg.reply('该账号尚未绑定')
                for i in result:
                    id = i[0]
            mode = 0
    
    card_msg , newid = await scoreCard(bot, 'recent', id, mode)
    if not card_msg:
        return await msg.reply('未查询到最近游玩的记录')
    if card_msg == '404':
        return await msg.reply('网页查询失败，请联系管理或稍后查询')
    if card_msg == 'iderror':
        return await msg.reply('不可以查询别人的最近成绩呦')
    # await msg.ctx.send(card_msg)
    await trySendCard(msg, card_msg)
    if newid:
        global globalbid, globalmode
        globalbid[guild_id] = newid
        globalmode = mode


@bot.command(name = "pr")
async def recent(msg:TextMsg, *args):
    guild_id = msg.guild_id
    at_id = msg.mention
    if not at_id:
        khl_id = msg.ctx.user_id
    else:khl_id = at_id[0]
    result = esql.get_id_mod(khl_id)
    if not args:
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for i in result:
            id = i[0]
            mode = i[1]
    else:
        while '' in args:
            args.remove('')
        mlen = len(args)
        if ':' in args[-1] and mlen == 1:
            id = re.search(".*:", args[0]).group()[:-1]
            if not id:
                for i in result:
                    id = i[0]
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        elif ':' in args[-1]:
            id = ' '.join(args[:mlen-1])
            try:
                mode = int(re.search(":.*", args[-1]).group()[1:])
            except:
                mode = re.search(":.*", args[-1]).group()[1:]
                if mode not in mode_lsn:
                    return await msg.reply('模式错误')
                mode = FGM[mode]
            if mode not in mode_ls:
                return await msg.reply('模式错误')
        else:
            id = ' '.join(args[:mlen])
            if khl_id in id:
                if not result:
                    return await msg.reply('该账号尚未绑定')
                for i in result:
                    id = i[0]
            mode = 0
    
    card_msg , newid = await scoreCard(bot, 'pr', id, mode)
    if not card_msg:
        await msg.reply('未查询到最近pass的记录')
    if card_msg == '404':
        await msg.reply('网页查询失败，请联系管理或稍后查询')
    if card_msg == 'iderror':
        await msg.reply('不可以查询别人的最近成绩呦')
    await trySendCard(msg, card_msg)
    if newid:
        global globalbid, globalmode
        globalbid[guild_id] = newid
        globalmode = mode


@bot.command(name = 'setmode')
async def update(msg:TextMsg, *args):
    khl_id = msg.ctx.user_id
    if len(args) != 1:
        return await msg.reply('请输入需要更新内容的参数 0-3')
    result = esql.get_id_mod(khl_id)
    if not result:
        botmsg = '该账号尚未绑定，请输入 bind 用户名 绑定账号'
    elif args[0][0] == ':':
        try:
            mode = int(args[0][1:])
        except:
            return await msg.reply('请输入需要更新内容的参数 0-3')
        if mode >= 0 or mode < 4:
            result = esql.update_mode(khl_id, mode)
            if result:
                botmsg = f'已将默认模式更改为 {GMN[mode]}'
            else:
                botmsg = '数据库错误'
        else:
            botmsg = '请输入正确的模式 0-3'
    else:
        botmsg = '参数错误，请输入正确的参数'
    return await msg.reply(botmsg)


@bot.command(name = 'bp')
async def bp(msg:TextMsg , *args):
    """
    return bp_num id _mod
    if len == 1:
        bp_nums and mode and name
    if len == 2:
        id and bp_nums and mode
    
    """
    at_id = msg.mention
    if not at_id:
        khl_id = msg.ctx.user_id
    else:khl_id = at_id[0]
    result = esql.get_id_mod(khl_id)

    if not args:        # 输入长度为0
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for i in result:
            id = i[0]
            mode = i[1]
        bp_num_min, bp_num_max = 1, 5

    if len(args) == 1:      # 输入长度为1
        
        if ':' in args[0]:
            other, mode = args[-1].split(':')[0], args[-1].split(':')[-1]
        else:
            other = args[0]
            mode = 0
        try:
            mode = int(mode)
            if mode not in mode_ls:
                return await msg.reply('请输入正确的mode')
        except:
            try:
                mode = FGM[mode]
            except:
                return await msg.reply('模式错误，请重新查询')
        """
        mode
        other:
            name
            num name
            bp
            bp_nums
        """

        if not other:
            if not result:
                return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
            for i in result:
                id = i[0]
            bp_num_min, bp_num_max = 1, 5    
        else:
            if '~' in other:
                bp_num_min = re.search('.*~', other).group()[:-1]
                bp_num_max = re.search('~.*', other).group()[1:]
                try:
                    bp_num_min, bp_num_max = int(bp_num_min), int(bp_num_max)
                    if bp_num_min > bp_num_max:
                        bp_num_max, bp_num_min = bp_num_min, bp_num_max
                    if bp_num_max - bp_num_min > 4:
                        return await msg.reply('一次最多只能查询5张地图')
                    if bp_num_min < 50 and bp_num_max > 50 :
                        bp_num_max = 50
                    if bp_num_min < 1:
                        return await msg.reply('请输入正确的bp 1-50')
                    if bp_num_min > 50:
                        return await msg.reply('只能查询前50的成绩')
                    if not result:
                        return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                    for i in result:
                        id = i[0]
                except ValueError:
                    return await msg.reply('请输入正确的bp区间')
                
            else:
                try:
                    bp_num_min, bp_num_max = int(other), int(other)
                    if bp_num_min > 99:
                        raise 'error'   # num name
                    if bp_num_min < 1:
                        return await msg.reply('请输入正确的bp 1-50')
                    if bp_num_min > 50:
                        return await msg.reply('只能查询前50的成绩')
                    if not result:
                        return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                    for i in result:
                        id = i[0]   
                except:
                    id = other
                    bp_num_min, bp_num_max = 1, 5
    
    if len(args) > 1:
        len_args = len(args)
        bps_c, mode_c = '', ''
        for i in range(0, len_args):
            if '~' in args[i]:
                bps_c = i
            if ':' in args[i]:
                mode_c = i
        if isinstance(bps_c, int) and isinstance(mode_c, int):
            other, mode = args[bps_c].split(':')[0], args[mode_c].split(':')[-1]
            try:
                mode = int(mode)
                if mode not in mode_ls:
                    return await msg.reply('请输入正确的mode')
            except:
                try:
                    mode = FGM[mode]
                except:
                    return await msg.reply('模式错误，请重新查询')
            bp_num_min = re.search('.*~', other).group()[:-1]
            bp_num_max = re.search('~.*', other).group()[1:]
            # bp_num_min , bp_mun_max = other.split('~')[0] , other.split('~')[1]
            try:
                bp_num_min, bp_num_max = int(bp_num_min), int(bp_num_max)
                if bp_num_min > bp_num_max:
                    bp_num_max, bp_num_min = bp_num_min, bp_num_max
                if bp_num_max - bp_num_min > 4:
                    return await msg.reply('一次最多只能查询5张地图')
                if bp_num_min < 50 and bp_num_max > 50 :
                    bp_num_max = 50
                if bp_num_min < 1:
                    return await msg.reply('请输入正确的bp 1-50')
                if bp_num_min > 50:
                    return await msg.reply('只能查询前50的成绩')
            except ValueError:
                return await msg.reply('请输入正确的bp区间')
            
            for num in range(0, len_args):
                if ':' in args[num] or '~' in args[num]:
                    break

            # if bps_c < 0 and args[num-1] > 0 and args[num - 1] < 51:
            #     bp_num_min, bp_num_max = args[num - 1], args[num - 1]
            #     num = num - 1

            id = ' '.join(args[:num])
            if not id:
                if not result:
                    return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                for i in result:
                    id = i[0]
        
        if isinstance(bps_c, int) and not isinstance(mode_c, int):
            other = args[bps_c]
            bp_num_min = re.search('.*~', other).group()[:-1]
            bp_num_max = re.search('~.*', other).group()[1:]
            try:
                bp_num_min, bp_num_max = int(bp_num_min), int(bp_num_max)
                if bp_num_min > bp_num_max:
                    bp_num_max, bp_num_min = bp_num_min, bp_num_max
                if bp_num_max - bp_num_min > 4:
                    return await msg.reply('一次最多只能查询5张地图')
                if bp_num_min < 50 and bp_num_max > 50 :
                    bp_num_max = 50
                if bp_num_min < 1:
                    return await msg.reply('请输入正确的bp 1-50')
                if bp_num_min > 50:
                    return await msg.reply('只能查询前50的成绩')
            except ValueError:
                return await msg.reply('请输入正确的bp区间')

            for num in range(0, len_args):
                if ':' in args[num] or '~' in args[num]:
                    break
            id = ' '.join(args[:num])
            if not id:
                if not result:
                    return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                for i in result:
                    id = i[0]
                    mode = i[1]
            else :
                mode = 0
        
        if not isinstance(bps_c, int) and isinstance(mode_c, int):
            other, mode = args[mode_c].split(':')[0], args[mode_c].split(':')[-1]      # name 1:3
            try:
                mode = int(mode)
                if mode not in mode_ls:
                    return await msg.reply('请输入正确的mode')
            except:
                try:
                    mode = FGM[mode]
                except:
                    return await msg.reply('模式错误，请重新查询')
        
            for num in range(0, len_args):      # name 1 :3
                    if ':' in args[num] or '~' in args[num]:
                        break
            
            name_bak = ''
            try:
                num_bak = int(other)
                if num_bak < 0 or num_bak > 51:
                    return await msg.reply('请输入正确的bp 1-50')
                bp_num_min, bp_num_max = num_bak, num_bak
            except:
                if other:
                    name_bak = other
                    bp_num_min, bp_num_max = 1, 5
                else:
                    try:
                        if int(args[num-1]) > 0 and int(args[num - 1]) < 51:
                            bp_num_min, bp_num_max = args[num - 1], args[num - 1]
                            num = num - 1
                        else:
                            bp_num_min, bp_num_max = 1, 5
                    except:
                        bp_num_min, bp_num_max = 1, 5

            id = ' '.join(args[:num])
            if name_bak:
                id = id + f" {name_bak}"
            if not id:
                if not result:
                    return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                for i in result:
                    id = i[0]
        
        if not isinstance(bps_c, int) and not isinstance(mode_c, int):
            num = len(args)
            try:
                num_t = int(args[-1])
                if num_t > 0 and num_t < 51:
                    bp_num_min, bp_num_max = num_t, num_t
                    num -= 1
            except:
                bp_num_min, bp_num_max = 1, 5
            id = id = ' '.join(args[:num])
            if not id:
                if not result:
                    return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                for i in result:
                    id = i[0]
                    mode = i[1]
            else:
                mode = 0

    card_msg = await bpCard(bot, 'bp' , id , mode , bpmin=bp_num_min ,bpmax=bp_num_max)
    # await msg.ctx.send(card_msg)
    # await msg.ctx.send(' ')
    if not card_msg:
        return await msg.reply('未查询到best performance')
    if card_msg == '404':
        return await msg.reply('网页查询失败，请联系管理或稍后查询')
    await trySendCard(msg, card_msg)


@bot.command(name = 'bpme')
async def todaybp(msg:TextMsg, *args):
    khl_id = msg.ctx.user_id
    result = esql.get_id_mod(khl_id)
    if not args:
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
    for i in result:
        id = i[0]
        mode = i[1]

    if len(args) > 1:
        return await msg.reply("不可以查询别人的bp")
    elif len(args) == 1:
        if ":" in args[-1]:
            mode = args[-1].split(":")[-1]
            try: 
                mode = int(mode)
                if mode not in mode_ls:
                    return await msg.reply('请输入正确的mode')
            except:
                try:
                    mode = FGM[mode]
                except:
                    return await msg.reply('模式错误，请重新查询')
        else:
            return await msg.reply("不可以查询别人的bp")
    
    card_msg = await bpToday(bot, "bp" , id , mode)
    # await msg.ctx.send(card_msg)
    if not card_msg:
        return await msg.reply('未查询到bp(best performance)')
    if card_msg == '404':
        return await msg.reply('网页查询失败，请联系管理或稍后查询')
    await trySendCard(msg, card_msg)
    

@bot.command(name = 'score') # eg:score name | artist(author)-title[version] #rank stat=loved
async def score(msg:TextMsg, *args):
    guild_id = msg.guild_id
    at_id = msg.mention
    if not at_id:
        khl_id = msg.ctx.user_id
    else:khl_id = at_id[0]
    result = esql.get_id_mod(khl_id)

    if not args:
        return await msg.reply('请输入地图名')
    
    name, rank, mode, author, artist, version, title, bid, stat =\
         None, None, 0, None, None, None, None, None, 'ranked'

    num_name, num_artist = 0, 0
    start_num, end_num = 0, 0
    ver_num = None
    aut_num = None

    for i in range(0, len(args)):
        if args[i] == '-id':
            bid = args[i + 1]
            try:
                bid = int(bid)
            except:
                return await msg.reply('请输入正确的beatmap id')
            if i != 0:
                name = " ".join(args[:i])
                if str(khl_id) in str(name):
                    if not result:
                        return await msg.reply('该账号尚未绑定')
                    for i in result:
                        name = i[0]
            if not name:
                if not result:
                    return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                for res in result:
                    name = res[0]

        if args[i][0] == '#':
                rank = args[i][1:]
                try:
                    rank = int(rank)
                    if rank < 1 or rank > 50:
                        return await msg.reply('只能查询前50的成绩')
                except:
                    return await msg.reply('#后请输入1-50的整数')

        if not bid:
            if not num_name:
                if args[i] == ',':
                    name = ' '.join(args[:i])
                    num_name += 1
                    start_num = i + 1

            if args[i][:5] == 'stat=':
                stat = re.search('=.*?', args[i]).group()[1:]
                if stat != 'loved' and stat != 'qualified' and stat != 'ranked':
                    return await msg.reply('stat错误，请输入loved or qualified')
                
            if args[i][0] == ':':
                mode = args[i][1:]
                try:
                    mode = int(mode)
                    if mode not in mode_ls:
                        return await msg.reply('请输入正确的mode')
                except:
                    try:
                        mode = FGM[mode]
                    except:
                        return await msg.reply('模式错误，请重新查询')
            
            if num_artist == 0:
                if args[i] == '-':
                    end_num = i
                    num_artist += 1
                    artist = " ".join(args[start_num:end_num])
                    artist = artist.strip()
                    if not artist:
                        artist = None
                    start_num = i + 1

            if '[' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '[':
                        if title:
                            title = title + ' ' + re.search('.*?\[', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_n = i + 1
                else:
                    len_n = i
                for n in range(i, len_n):
                    if ']' in args[n]:
                        ver_num = i

            if ']' in args[i]:
                if isinstance(ver_num, int):
                    if ver_num == i:
                        version = re.search('\[(.*?)\]', args[i]).group()[1:-1]
                    else:
                        version = re.search('\[.*', args[ver_num]).group()[1:] + \
                                    " ".join(args[ver_num+1:i]) + \
                                    ' ' + re.search('.*?\]', args[i]).group()[:-1]

            if '(' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '(':
                        if title:
                            title = title + ' ' + re.search('.*?\(', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_m = i + 1
                else:
                    len_m = i
                for n in range(i, len_m):
                    if ')' in args[n]:
                        aut_num = i

            if ')' in args[i]:
                if isinstance(aut_num, int):
                    if aut_num == i:
                        author = re.search('\((.*?)\)', args[i]).group()[1:-1]
                    else:
                        author = re.search('\(.*', args[aut_num]).group()[1:] + \
                                    " ".join(args[aut_num+1:i]) + \
                                    ' ' + re.search('.*?\)', args[i]).group()[:-1]

    tit_num = None
    if not isinstance(aut_num, int) and not isinstance(ver_num, int) and not bid:
        for i in range(0, len(args)):
            if args[i][0] == ':' or args[i][0] == '#':
                tit_num = i
                break
        if isinstance(tit_num, int):
            title = " ".join(args[start_num:i])
        else:
            title = ' '.join(args[start_num:])


    if not name:
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for i in result:
            name = i[0]
    else:
        if str(khl_id) in str(name):
            if not result:
                return await msg.reply('该账号尚未绑定')
            for i in result:
                name = i[0]
    # await msg.reply(f"{name}, {rank}, {mode}, {author}, {artist}, {version}, {title}, {bid}, {stat}")

    card_msg , newid = await scoreCard(bot, 'score', name, mode, title=title, artist=artist, creator=author, version=version, mapid=bid, rank=rank)
    # await msg.ctx.send(card_msg)
    await trySendCard(msg , card_msg)
    if newid:
        global globalbid, globalmode
        globalbid[guild_id] = newid
        globalmode = mode
        

@bot.command(name = 'music') 
async def music(msg:TextMsg, *args):
    '''
    eg
        music okazaki taiiku - kimi no bouken
        music -id 884581
    '''
    if not args:
        return await msg.reply('请输入地图名')

    title, artist, author, version, bid = None, None, None, None, None

    num_artist = 0
    start_num, end_num = 0, 0
    ver_num = None
    aut_num = None

    for i in range(0 , len(args)):
        if args[i] == '-id':
            bid = args[i + 1]
            try:
                bid = int(bid)
            except:
                return await msg.reply('请输入正确的beatmap id')
        
        if not bid:
            if num_artist == 0:
                if args[i] == '-':
                    end_num = i
                    num_artist += 1
                    artist = " ".join(args[start_num:end_num])
                    artist = artist.strip()
                    if not artist:
                        artist = None
                    start_num = i + 1
        
            if '[' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '[':
                        if title:
                            title = title + ' ' + re.search('.*?\[', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_n = i + 1
                else:
                    len_n = i
                for n in range(i, len_n):
                    if ']' in args[n]:
                        ver_num = i

            if ']' in args[i]:
                if isinstance(ver_num, int):
                    if ver_num == i:
                        version = re.search('\[(.*?)\]', args[i]).group()[1:-1]
                    else:
                        version = re.search('\[.*', args[ver_num]).group()[1:] + \
                                    " ".join(args[ver_num+1:i]) + \
                                    ' ' + re.search('.*?\]', args[i]).group()[:-1]

            if '(' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '(':
                        if title:
                            title = title + ' ' + re.search('.*?\(', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_m = i + 1
                else:
                    len_m = i
                for n in range(i, len_m):
                    if ')' in args[n]:
                        aut_num = i

            if ')' in args[i]:
                if isinstance(aut_num, int):
                    if aut_num == i:
                        author = re.search('\((.*?)\)', args[i]).group()[1:-1]
                    else:
                        author = re.search('\(.*', args[aut_num]).group()[1:] + \
                                    " ".join(args[aut_num+1:i]) + \
                                    ' ' + re.search('.*?\)', args[i]).group()[:-1]
                
    tit_num = None
    if not isinstance(aut_num, int) and not isinstance(ver_num, int) and not bid:
        for i in range(0, len(args)):
            if args[i][0] == ':' or args[i][0] == '#':
                tit_num = i
                break
        if isinstance(tit_num, int):
            title = " ".join(args[start_num:i])
        else:
            title = ' '.join(args[start_num:])
    
    card_msg = await musicCard(bot, title, artist, author, version, mapid=bid)
    # await msg.ctx.send(card_msg)
    await trySendCard(msg, card_msg , reply=False)


@bot.command(name = 'pp+') 
async def ppplus(msg:TextMsg, *args):
    ls_id = ['None', 'None']
    at_id = msg.mention
    khl_id = msg.ctx.user_id
    if not at_id:
        if not args:
            result = esql.get_id_mod(khl_id)
            if not result:
                return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
            for i in result:
                ls_id[0] = i[0]
        else:
            num = None
            for i in range(len(args)):
                if ',' in args[i]:
                    num = i
                    break
            if not isinstance(num, int):
                ls_id[0] = " ".join(args[:])
            else:
                text_l = (" ".join(args[:num]) + ' ' + re.search('.*?,', args[num]).group()[:-1]).strip()
                if num == len(args):
                    text_r = re.search(',.*?').group()[1:]
                else:
                    text_r = re.search(',.*?').group()[1:] + ' ' + " ".join(args[num+1:])
                if not text_l and not text_r:
                    return await msg.reply('请输入正确的格式')
                elif text_l and text_r:
                    ls_id[0] = text_l
                    ls_id[1] = text_r
                else:
                    result = esql.get_id_mod(khl_id)
                    if not result:
                        return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
                    for i in result:
                        ls_id[0] = i[0]
                    ls_id[1] = text_l if text_l else text_r

    
    if len(at_id) == 1:
        num = None
        for i in range(len(args)):
            if ',' in args[i]:
                num = i
                break
        if not isinstance(num, int):
            result = esql.get_id_mod(at_id[0])
            if not result:
                return await msg.reply('该账号尚未绑定')
            for i in result:
                ls_id[0] = i[0]

        else:
            text_l = (" ".join(args[:num]) + ' ' + re.search('.*?,', args[num]).group()[:-1]).strip()
            if num == len(args):
                text_r = re.search(',.*?').group()[1:]
            else:
                text_r = re.search(',.*?').group()[1:] + ' ' + " ".join(args[num+1:])
            if text_l[0] != '@' and text_r[0] != '@':
                return await msg.reply('请输入正确的格式')
            if not text_l or not text_r:
                result = esql.get_id_mod(at_id[0])
                if not result:
                    return await msg.reply('该账号尚未绑定')
                for i in result:
                    ls_id[0] = i[0]
                ls_id[1] = text_l if text_l else text_r
            else:
                ls_id[0] = text_l if text_l[0] != '@' else text_r
                result = esql.get_id_mod(at_id[0])
                if not result:
                    return await msg.reply('该账号尚未绑定')
                for i in result:
                    ls_id[1] = i[0]

    if len(at_id) == 2:
        num = None
        for i in range(len(args)):
            if ',' in args[i]:
                num = i
                break
        if not isinstance(num, int):
            return await msg.reply('请输入正确的格式')
        for i in range(0, 2):
            result = esql.get_id_mod(at_id[i])
            if not result:
                return await msg.reply('该账号尚未绑定')
            for i in result:
                ls_id[i] = i[0]

    if len(at_id) > 2:
        return await msg.reply('最多同时查询2人')

    msg_card = await ppp(bot, ls_id)
    # await msg.ctx.send(msg_card)
    await trySendCard(msg, msg_card)


@bot.command(name = 'help')
async def helptext(msg:TextMsg):
    await msg.ctx.send(helptxt)


@bot.command(name='search')
async def search(msg:BtnTextMsg , *args):
    if not args:
        return await msg.reply('请输入地图名')

    title, artist, author, version, sid = None, None, None, None, None

    num_artist = 0
    start_num, end_num = 0, 0
    ver_num = None
    aut_num = None
    start = 0

    for i in range(0 , len(args)):
        if args[i] == '-sid':
            sid = args[i + 1]
            try:
                sid = int(sid)
            except:
                return await msg.reply('请输入正确的beatmapset id')
        
        if not sid:
            if num_artist == 0:
                if args[i] == '-':
                    end_num = i
                    num_artist += 1
                    artist = " ".join(args[start_num:end_num])
                    artist = artist.strip()
                    if not artist:
                        artist = None
                    start_num = i + 1
        
            if '[' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '[':
                        if title:
                            title = title + ' ' + re.search('.*?\[', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_n = i + 1
                else:
                    len_n = i
                for n in range(i, len_n):
                    if ']' in args[n]:
                        ver_num = i

            if ']' in args[i]:
                if isinstance(ver_num, int):
                    if ver_num == i:
                        version = re.search('\[(.*?)\]', args[i]).group()[1:-1]
                    else:
                        version = re.search('\[.*', args[ver_num]).group()[1:] + \
                                    " ".join(args[ver_num+1:i]) + \
                                    ' ' + re.search('.*?\]', args[i]).group()[:-1]

            if '(' in args[i]:
                if not title:
                    title = " ".join(args[start_num:i])
                    if args[i][0] != '(':
                        if title:
                            title = title + ' ' + re.search('.*?\(', args[i]).group()[:-1]
                        else:
                            title = re.search('.*?\[', args[i]).group()[:-1]
                if i == len(args) - 1:
                    len_m = i + 1
                else:
                    len_m = i
                for n in range(i, len_m):
                    if ')' in args[n]:
                        aut_num = i

            if ')' in args[i]:
                if isinstance(aut_num, int):
                    if aut_num == i:
                        author = re.search('\((.*?)\)', args[i]).group()[1:-1]
                    else:
                        author = re.search('\(.*', args[aut_num]).group()[1:] + \
                                    " ".join(args[aut_num+1:i]) + \
                                    ' ' + re.search('.*?\)', args[i]).group()[:-1]
                
    tit_num = None
    if not isinstance(aut_num, int) and not isinstance(ver_num, int) and not sid:
        for i in range(0, len(args)):
            if args[i][0] == ':' or args[i][0] == '#':
                tit_num = i
                break
        if isinstance(tit_num, int):
            title = " ".join(args[start_num:i])
        else:
            title = ' '.join(args[start_num:])

    if not sid:
        while True:
            sid_card , mapdict = await searchSid(bot , title , artist, author, version , startid=start)
            print('search over')
            if isinstance(sid_card , int):
                sid = sid_card
            else:
                # await msg.ctx.send(sid_card)
                sendmsg = await trySendCard(msg, sid_card)
                if not sendmsg:
                    return
                step = await msg.ctx.wait_btn(sendmsg['msg_id'] , 190)
                if not step:
                    return
                else:
                    todo = step.body['value']
                    if todo == 'previous':
                        start = start - 5
                        await bot.delete(sendmsg['msg_id'])
                    elif todo == 'next':
                        start = start + 5
                        await bot.delete(sendmsg['msg_id'])
                    else:
                        sid = mapdict[todo]
                        await bot.delete(sendmsg['msg_id'])
                        break
                    

    map_card = await searchBySid(bot , sid = sid)
    print('sending')
    # await msg.ctx.send(map_card)
    await trySendCard(msg , map_card)


@bot.command(name='compare' , aliases=('c'))
async def compare(msg:TextMsg):
    global globalbid, globalmode
    guild_id = msg.guild_id
    try:
        mapid = globalbid[guild_id]
        khl_id = msg.ctx.user_id
        result = esql.get_id_mod(khl_id)
        if not result:
            return await msg.reply('该账号尚未绑定，请输入 .bind 用户名 绑定账号')
        for res in result:
            name = res[0]

        compare_msg , _ = await scoreCard(bot , 'score' , name , globalmode , mapid = mapid , rank = None)
        await trySendCard(msg , compare_msg)
        return
    except Exception as e:
        print(e)
        return await msg.reply("没有最近查询的成绩")

@bot.command(name='prpr')
async def ping(msg:TextMsg):
    return await msg.reply('(> <)')
    


bot.run()

