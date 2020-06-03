import sqlite3
import requests, re, time, os

category_dic = {
    "all": "全站榜",
    # "origin": "原创榜",
    # "rookie": "新人榜",
}
# , 3: "三日排行榜", 7: "周排行榜", 
day_dic = {1: "日排行榜", 30: "月排行榜"}
all_or_origin_dic = {
    0: "全站",
    # 1: "动画",
    # 168: "国创相关",
    # 3: "音乐",
    # 129: "舞蹈",
    # 4: "游戏",
    # 36: "科技",
    # 188: "数码",
    # 160: "生活",
    # 119: "鬼畜",
    # 155: "时尚",
    # 5: "娱乐",
    # 181: "影视",
}

rookie_dic = {
    0: "全站",
    # 1: "动画",
    # 3: "音乐",
    # 129: "舞蹈",
    # 4: "游戏",
    # 36: "科技",
    # 188: "数码",
    # 160: "生活",
    # 119: "鬼畜",
    # 155: "时尚",
    # 5: "娱乐",
    # 181: "影视",
}

BaseDict = {
    "all": all_or_origin_dic,
    # "origin": all_or_origin_dic,
    # # "bangumi": bangumi_dic,
    # # "cinema": cinema_dic,
    # "rookie": rookie_dic,
}

dic = {
    "all": 1,
    # "origin": 2,
    # "rookie": 3,
}

base_path = "/home/miragelyu"       # 文件保存的位置


def get_url():
    result = []
    for first in category_dic.keys():
        if first in ["all", "origin", "rookie"]:
            for second in BaseDict.get(first).keys():
                for third in day_dic.keys():
                    url = "https://api.bilibili.com/x/web-interface/ranking?jsonp=jsonp&rid={}&day={}&type={}&arc_type=0&callback=__jp1".format(second, third, dic.get(first))
                    result.append(url)
    return result


s = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Referer": "https://www.bilibili.com/ranking/all/0/0/3"
}
url_list = get_url()
print(url_list)
conn = sqlite3.connect("bilistat.db")

print("向{}发请求".format(url_list[0]))
response = s.get(url=url_list[0], headers=headers)
print(response.text)
data = response.text.replace('"', "")
pattern = r'.*?bvid:(?P<bvid>.*?),.*?author:(?P<author>.*?),.*?coins:(?P<coins>.*?),.*?duration:(?P<duration>.*?),.*?pic:(?P<pic>.*?),.*?play:(?P<play>.*?),.*?pts:(?P<pts>.*?),.*?title:(?P<title>.*?),'
result_list = re.findall(pattern, data)
# print(result_list)
c = conn.cursor()
for l in result_list:
    c.execute('''INSERT INTO DAYRANK (AUTHOR, PLAY, PTS, TITLE, BVID, PIC, COINS, DURATION)
        VALUES(?,?,?,?,?,?,?,?)
    ''', (l[1], l[5], l[6], l[7], l[0], l[4], l[2], l[3]))
conn.commit()
time.sleep(2)

print("向{}发请求".format(url_list[0]))
response = s.get(url=url_list[1], headers=headers)
data = response.text.replace('"', "")
pattern = r'.*?bvid:(?P<bvid>.*?),.*?author:(?P<author>.*?),.*?coins:(?P<coins>.*?),.*?duration:(?P<duration>.*?),.*?pic:(?P<pic>.*?),.*?play:(?P<play>.*?),.*?pts:(?P<pts>.*?),.*?title:(?P<title>.*?),'
result_list = re.findall(pattern, data)
c = conn.cursor()
for l in result_list:
    c.execute('''INSERT INTO MONTHRANK (AUTHOR, PLAY, PTS, TITLE, BVID, PIC, COINS, DURATION)
        VALUES(?,?,?,?,?,?,?,?)
    ''', (l[1], l[5], l[6], l[7], l[0], l[4], l[2], l[3]))
conn.commit()
conn.close()