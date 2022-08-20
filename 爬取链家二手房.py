# -*- codeing = utf-8 -*-
# @time :2022/8/15 16:11
# @Author :玉衡Kqing
# @File   :爬取链家二手房.py
# @Software:PyCharm
import requests
import time
import random
import pandas as pd
from pyquery import PyQuery as pq
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
}
# 1.发出请求获取源码
def get_urls(baseurl):
    """
    得到一个区的所有url
    :param baseurl: 基本地区
    :return: 形如[{"金水区":'url'},{"XX区":"url"}]的元素为字典的列表
    """
    response = requests.get(baseurl,headers=headers).text
    doc_obj = pq(response)      #Pyquery实例化对象
    ul = doc_obj('body > div:nth-child(12) > div > div.position > dl:nth-child(2) > dd > div:nth-child(1) > div a ').items()
    urls = []
    for i in ul:
        dic = {}
        url = baseurl[0:-15] + i.attr("href")
        name = i.text()
        dic[name] = url
        urls.append(dic)
    # print(urls)
    return urls

def get_info(url):
    """
    得到一页内容
    :param url: 每个区的url
    :return: 每个区的数据
    """
    #这里应该有个循环
    init_url = url
    response = requests.get(url,headers=headers).text
    doc_obj = pq(response)
    num_page = doc_obj('#content > div.leftContent > div.contentBottom.clear > div.page-box.fr > div').attr(
        "page-data")  # 获取总页数
    num_page = json.loads(num_page)['totalPage']  # 用json将字符串转为字典
    # print(num_page)
    name = doc_obj('body > div:nth-child(12) > div > div.position > dl:nth-child(2) > dd > div:nth-child(1) > div:nth-child(1) a.selected').text()
    urls = []
    for page in range(1,num_page+1):
        url = init_url + 'pg' + str(page) + "/"
        print(url)
        response = requests.get(url,headers=headers).text
        doc_obj = pq(response)
        ul = doc_obj('#content > div.leftContent > ul > li > div.info.clear > div.title > a').items()
        for i in ul:
            urls.append(i.attr('href'))
        print(f"已完成{name}第{page}页数据的获取")
        # print(urls)
        time.sleep(0.01)
    print('\n')
    print(f"{name}共拿到{len(urls)}个房屋信息")  # 已经获取到一个页面的详情页
    return urls



# 2.数据提取
def get_content(url):
    response = requests.get(url,headers=headers).text
    doc_obj = pq(response)
    # 获取主要信息
    # main_info = doc_obj('body > div.overview > div.content')
    # print(main_info)
    price = doc_obj('div.price span.total,span.unit').text().replace(' ','')   #房价
    # print(price)
    info_0 = doc_obj('body > div.overview > div.content > div.aroundInfo > div.communityName')
    info_0 = info_0('span.label,a.info').text().split(' ')
    info_1 = doc_obj('body > div.overview > div.content > div.aroundInfo > div.areaName')
    info_content = []
    info_name = info_1('span.label').text()
    info_value = info_1('a').text()
    info_content.append(info_name)
    info_content.append(info_value)
    info_dict = {}
    info_dict[info_0[0]] = info_0[1]
    info_dict['price'] = price
    info_dict[info_content[0]] = info_content[1]
    # print(info_dict)
    # 获取基本属性
    ul = doc_obj('#introduction > div > div')
    base_content = ul('.base > .content li')
    titles = base_content('span').items()
    contents = base_content.children().remove().end().items() #这一行会先执行，为了保证2有内容，它必须在2的后面执行。
    titles_list,content_list = [],[]
    for i in titles:
        titles_list.append(i.text())
    for y in contents:
        content_list.append(y.text())
    base_attribute = {}
    for title,content in zip(titles_list,content_list):
        base_attribute[title] = content
    # 获取交易属性
    ul = doc_obj("#introduction > div > div > div.transaction > div.content li")
    label = ul('span').items()
    titles = []
    for i in label:
        titles.append(i.text())
    # print(titles)
    i = 0
    transaction_attribute = {}     # 这是一个{"属性":"内容"}的字典
    while i != len(titles):
        transaction_attribute[titles[i]] = titles[i+1]
        i = i + 2
    base_content = dict(base_attribute, **transaction_attribute)
    all_content = dict(info_dict,**base_content)
    print(all_content)
    return all_content               #返回一个{"title":"content"}字典保存单页数据，至此已经能完成单页数据获取


# 3.数据存储(excel)
def save_data(info_list):
    data = pd.DataFrame(info_list)
    data.to_csv("链家二手房信息.csv",encoding="utf_8_sig")      #记得to_csv选择encoding


# url = "https://zz.lianjia.com/ershoufang/104109115486.html"
baseurl = "https://zz.lianjia.com/ershoufang/rs/"
urls = get_urls(baseurl)     # 得到了一个 [{name:url}] 形式的列表
info_url_list = []           # 详情页的链接
info_list = []               # 详情页数据
for i in urls:
    for url in i.values():
        # print(url)
        main_urls = get_info(url)
        # print(main_urls)
        time.sleep(1)
        info_url_list = info_url_list + main_urls
    # break
print(info_url_list,f"总共拿到{len(info_url_list)}个网页信息，接下来将开始爬取数据")
for url_info in info_url_list:
    info = get_content(url_info)
    info_list.append(info)
    time.sleep(0.01)       #设置休眠时间
save_data(info_list)




