# -*- coding: utf-8 -*-
import requests
import json
import sqlite3
import time

# 爬取B站up主的信息，包括：id号，姓名，性别，粉丝数，关注数，等级
# 由于B站数据太多，这里不能全部爬取，建议改进：多线程， 分布式
# 包含爬取数据进度保存，可以随时爬取


def get_html(url):  # 向网站发送请求，代码格式固定
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    cookie = {'Cookie': "fts=1504349387; buvid3=1C1CB246-90F7-4641-994C-875348FCC9DA31841infoc; LIVE_BUVID=923027b89ab5074df00ddeb74bd1bc4c; LIVE_PLAYER_TYPE=1; LIVE_BUVID__ckMd5=213686949aed5aa3; sid=jszx4g3e; stardustvideo=1; CURRENT_FNVAL=16; rpdid=kmwpioxopmdospssmioww; CURRENT_QUALITY=32; bp_t_offset_105511477=225519300968954321; finger=888236dc; im_notify_type_105511477=0; UM_distinctid=169200905bf184-0820062ee695d58-4c312f7f-100200-169200905c039c; DedeUserID=105511477; DedeUserID__ckMd5=e312e81cda67c220; SESSDATA=f560bc58%2C1553994772%2C44a40231; bili_jct=90910cb604d93fccf748794b4007ba13; bsource=seo_baidu; _dfcaptcha=d2c62b90ce5116dd8e1dd97aec364e73"}
    r = requests.get(url=url, headers=headers, cookies=cookie)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.content.decode()


def get_information(url):  # 得到页面信息
    html = get_html(url)  # 得到json
    value = json.loads(html)  # 加载json
    print(value)
    flag = True  # flag，判断是否有这个页面
    mid = value.get("data").get("card").get("mid")  # json得到mid号
    name = value.get("data").get("card").get("name")
    face = value.get("data").get("card").get("face")
    sex = value.get("data").get("card").get("sex")
    fans = value.get("data").get("card").get("fans")
    sign = value.get("data").get("card").get("sign")
    attention = value.get("data").get("card").get("attention")
    level = value.get("data").get("card").get("level_info").get("current_level")
    if mid == "":  # mid号为空，则没有这个用户
        flag = False
    return flag, mid, name, sex, fans, attention, level, face, sign # 返回信息

up_lst = [326499679, 546195, 9824766, 321173469, 777536, 122879, 20165629, 517327498, 14110780, 1532165]
conn = sqlite3.connect("bilistat.db")
for i in up_lst:
    mid = str(i)
    # 生成url
    url = "https://api.bilibili.com/x/web-interface/card?mid=%s&jsonp=jsonp&article=true" % mid
    flag, mid, name, sex, fans, attention, level, face, sign = get_information(url)  # 得到数据

    c = conn.cursor()
    c.execute('''INSERT INTO USER (MID, NAME, SEX, FANS, ATTENTION, LEVEL, FACE, SIGN)
        VALUES (?,?,?,?,?,?,?,?);
    ''', (mid, name, sex, fans, attention, level, face, sign))
    conn.commit()
    time.sleep(0.1) 
conn.close()

