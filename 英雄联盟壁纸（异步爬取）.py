# -*- codeing = utf-8 -*-
# @time :2021/3/24 19:29
# @Author :玉衡Kqing
# @File   ：英雄联盟壁纸.py
# @Software:PyCharm

# from bs4 import BeautifulSoup                    #网页解析，获取数据
# import re                                        #正则表达式，进行文字匹配
# import urllib.request,urllib.error               #指定url获取网页数据
# import sqlite3                                   #进行SQLite数据库操作
# import requests
# import os
# import json
# import jsonpath                                  #用于筛选json数据
# url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?v=40"
# response = requests.get(url).json()
# hero_ids = jsonpath.jsonpath(response,'$..heroId')
# for hero_id in hero_ids:
#     hero_info_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js".format(hero_id)
#     hero_info = requests.get(hero_info_url).json()         #请求每个英雄的详细信息
#     skin_info_list = hero_info['skins']                   #皮肤信息列表
#     skin_id_list = jsonpath.jsonpath(skin_info_list,'$..skinId')   #保存单个英雄的所有皮肤ID
#     skin_name_list = jsonpath.jsonpath(skin_info_list, '$..name')
#
#     for skin_id,skin_name in zip(skin_id_list,skin_name_list):
#         img_url = "https://game.gtimg.cn/images/lol/act/img/skin/big" + str(skin_id) + '.jpg'
#         image = requests.get(img_url)     #请求皮肤图片数据
#
#         with open('./英雄联盟壁纸/%s.jpg'%skin_name,"wb") as f:
#             f.write(image.content)
#         print('《%s》下载成功'%skin_name)


#自己写的
'''
import re
import requests
import json
import os
findID = re.compile(r'"heroId":"(.*?)"')
#1.获取JS源代码
#2.拼接URL地址
#3.获取下载图片地址
#4.下载图片

def getLOLImage():
    url_js = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    re_js = requests.get(url_js).content          #.content返回的是字节,不能直接使用，需要转码成字符串类型!!!!!!!!!!!!!!
    html_js = re_js.decode("utf-8")                      #decode解码，转成字符串!!!!!!!!!!!!!!!!!!
    #print(html_js)
    hero_ID = re.findall(findID,html_js)              #获取每个英雄ID ！！！！！！！！！！！
    for id in hero_ID:                                  #id存的是英雄ID
        #print(i)
        for i in range(20):
            num = str(i)
            if len(num) == 1:
                hero_num = "00" + num
            elif len(num) == 2:
                hero_num = "0" + num
            hero_skinID = id + hero_num                #每个英雄皮肤的网址变动部分
            url_skin = "https://game.gtimg.cn/images/lol/act/img/skin/big"+hero_skinID+".jpg"
            #print(url_skin)
            #print(hero_skinID)
            response = requests.get(url_skin)
            path = "./LOLskin"
            if not os.path.exists(path):
                os.mkdir(path)
            with open("LOLskin"+hero_skinID+".jpg","wb") as f:
                f.write(response.content)

#https://game.gtimg.cn/images/lol/act/img/skin/big1001.jpg  皮肤样式

getLOLImage()
'''

import os
import json
import urllib.request,urllib.error
import re
import time
import random
import requests

def main():
    url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?v=25"
    askURL(url)
    path = 'C:\\Users\\86178\\PycharmProjects\\视频学习\\venv'
    if not os.path.exists("英雄联盟壁纸"):
        os.mkdir("英雄联盟壁纸")
    result_hero = open("英雄联盟英雄IDjson.html","r")
    hero_ID = re.findall(r'"heroId": "(.+?)",',str(result_hero.readlines()))      #拿到了所有英雄ID
    #print(hero_ID)
    for i in hero_ID:
        #url = "https://game.gtimg.cn/images/lol/act/img/js/hero/2.js"
        url = "https://game.gtimg.cn/images/lol/act/img/js/hero/"+ str(i) + ".js"
        html = askURL(url)
        html = html.encode().decode("unicode_escape")             #unicode转中文
        #print(html)
        hero_skinID = re.findall(r'"skinId":"(.+?)",',html)      #所有皮肤ID
        hero_skin_Name = re.findall(r'"name":"(.*?)",',html)    #所有皮肤名字
        del hero_skin_Name[0]
        del hero_skin_Name[-1]
        del hero_skin_Name[-1]
        del hero_skin_Name[-1]
        del hero_skin_Name[-1]
        del hero_skin_Name[-1]
        #print(hero_skinID)
        #print(hero_skinName)
        for item,name in zip(hero_skinID,hero_skin_Name):                 #zip打包多个列表，进行平行遍历
            #print(item,name)
            skin_url = "https://game.gtimg.cn/images/lol/act/img/skin/big" + item + ".jpg"
            head = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
            }
            data = requests.get(skin_url, headers=head).content          #下载图片  .content就是转为二进制
            with open("英雄联盟壁纸\\"+ name + ".png","wb") as f:
                print("正在下载：%s"%name)
                f.write(data)
            # with open(name + ".png","wb") as f:
            #     print("正在下载: %s"%name)
            #     f.write(data)

#间隔时间爬取
#代理

def askURL(url):
    head = {                                                                  #模拟浏览器头部向服务器发送信息
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }                                                                         #用户代理告诉浏览器我们是什么类型机器
    request = urllib.request.Request(url,headers= head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gbk")
    except urllib.error.URLError as e :
        if hasattr(e,"code"):                                                 #hasattr() 函数用于判断对象是否包含对应的属性。hasattr(object, name)
            print(e.code)                                                     #获取的错误代码
        if hasattr(e,"reason"):
            print(e.reason)                                                   #获取的错误原因
    return  html

if __name__ == '__main__':
    main()


