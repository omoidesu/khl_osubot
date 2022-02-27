from api import getApiInfo
from sql import osusql
import time

# import numpy as np
# import matplotlib.pyplot as plt

GM = {0:"osu" , 1:"taiko" , 2:"fruits" , 3:"mania"}

async def bindInfo(project , user_id , khl_id):
    esql = osusql()
    info = await getApiInfo(project , user_id , GM[0])
    if not info:
        return "未查询到该玩家"
    elif isinstance(info , str):
        return info
    osu_id = info['id']
    name = info['username']
    esql.insert_user(khl_id , osu_id , name)
    await user(osu_id)
    msg = f"用户{name}绑定成功"
    return msg

async def user(osu_id , update = False):
    esql = osusql()
    for mode in range(4):
        if not update:
            new = esql.get_all_newinfo(osu_id , mode)
            if new:
                continue

        info = await getApiInfo("update" , osu_id , GM[mode])
        if info["statistics"]["play_count"] != 0:
            username = info["username"]
            play = info["statistics"]
            count = play["total_hits"]
            pc = play["play_count"]
            g_ranked = play["global_rank"] if play["global_rank"] else 0
            pp = play["pp"]
            acc = round(play["hit_accuracy"] , 2)
            c_ranked = play["country_rank"] if play["country_rank"] else 0
            if update:
                esql.update_all_info(osu_id , c_ranked , g_ranked , pp , acc , pc , count , mode)
            else:
                esql.insert_all_info(osu_id , c_ranked , g_ranked , pp , acc , pc , count , mode)
        else:
            username = info["username"]
            if update:
                esql.update_all_info(osu_id , 0 , 0 , 0 , 0 , 0 , 0 , mode)
            else:
                esql.insert_all_info(osu_id , 0 , 0 , 0 , 0 , 0 , 0 , mode)
        now = time.strftime("%H:%M:%S")
        print(f"<{now}>玩家:[{username}]{GM[mode]}模式更新完毕")

# def draw(name , results):
#     data_length = len(results[0])

#     # 将极坐标根据数据长度进行等分
#     angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
#     labels = [key for key in results[0].keys()]
#     score = [[v for v in result.values()] for result in results]

#     # 使雷达图数据封闭
#     score_a = np.concatenate((score[0], [score[0][0]]))
#     score_b = np.concatenate((score[1], [score[1][0]]))
#     angles = np.concatenate((angles, [angles[0]]))
#     labels = np.concatenate((labels, [labels[0]]))

#     # 设置图形的大小
#     fig = plt.figure(figsize=(8, 6), dpi=100)

#     # 新建一个子图
#     ax = plt.subplot(111, polar=True)

#     # 绘制雷达图
#     ax.plot(angles, score_a, color='g')
#     ax.plot(angles, score_b, color='b')

#     # 设置雷达图中每一项的标签显示
#     ax.set_thetagrids(angles*180/np.pi, labels)

#     # 设置雷达图的0度起始位置
#     ax.set_theta_zero_location('N')

#     # 设置雷达图的坐标刻度范围

#     ax.set_rlim(0, 5000)
#     # 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
#     ax.set_rlabel_position(270)

#     plt.legend(name, loc='best')

#     plt.show()