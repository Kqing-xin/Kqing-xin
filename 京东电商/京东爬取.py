# @time:2022/8/30 16:50
# @Author:玉衡Kqing
# @File:京东爬取.py
# @Software:PyCharm
import json
import random
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import re

def add_cookies():
    browser.delete_all_cookies()
    try:
        with open('jd.cookie', 'r') as f:
            cookie_list = json.load(f)
            for cookie in cookie_list:
                browser.add_cookie(cookie)
    except:
        print('未找到Cookie')
    return browser.refresh()

def search_goods(search):
    """
    拿到一页的url，60个
    :param search: 想搜索的商品名
    :return: 商品urls列表
    """
    browser.find_element(By.CSS_SELECTOR,'#key').send_keys(search)
    browser.find_element(By.CSS_SELECTOR,'#search > div > div.form > button').click()
    time.sleep(5)
    goods_urls = []
    for j in range(20):
        for i in range(1,61):
            browser.implicitly_wait(10)
            browser.execute_script(f"document.documentElement.scrollTop={random.randint(100000, 100900)}")
            href = browser.find_element(By.CSS_SELECTOR,
                                    f"#J_goodsList > ul > li:nth-child({i}) > div > div.p-name.p-name-type-2 > a").get_attribute('href')
            goods_urls.append(href)
        try:
            browser.find_element(By.CSS_SELECTOR,"#J_bottomPage > span.p-num > a.pn-next").click()
        except Exception as e:
            print(e)
        print(f"正在爬取第{j+1}页，还剩{20-(j+1)}页")
        time.sleep(random.randint(1,3))
    print(goods_urls,len(goods_urls))
    return goods_urls

def get_goods_info(url,browser):
    """
    得到一个商品的详情信息
    :param url: 一个商品的详情页url
    :return: 详细信息
    """
    option = webdriver.ChromeOptions()  # 创建一个配置对象
    option.add_argument("--headless")  # 开启无界面模式
    browser.get(url)
    browser.implicitly_wait(10)
    info = []  # 存放一个商品的列表内容
    info_dict = {}   # 转为字典返回
    try:
        price = browser.find_element(By.CSS_SELECTOR,
                                     "body > div:nth-child(10) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span.p-price"
                                     ).text.replace("￥ ","")
        info.append("Price")
        info.append(price)
        title = browser.find_element(By.CSS_SELECTOR,
                                     "body > div:nth-child(10) > div > div.itemInfo-wrap > div.sku-name").text
        news = browser.find_element(By.CSS_SELECTOR,
                                    "body > div:nth-child(10) > div > div.itemInfo-wrap > div.news").text
        info.append("Title")
        info.append(title)
        info.append("News")
        info.append(news)
        brand = browser.find_element(By.CSS_SELECTOR, "#parameter-brand > li").text.split("：")
        main_info = browser.find_element(By.CSS_SELECTOR,
                                         "#detail > div.tab-con > div:nth-child(1) > div.p-parameter > ul.parameter2.p-parameter-list").text
        main_info = re.split("：|\n", main_info)
        # print(main_info)
        # print(brand + main_info)
        browser.find_element(By.CSS_SELECTOR, "#detail > div.tab-main.large > ul > li:nth-child(2)").click()
        browser.implicitly_wait(10)
        test = browser.find_elements(By.CSS_SELECTOR,
                                     "#detail > div.tab-con > div:nth-child(2) > div.Ptable > div.Ptable-item > dl > dl")
        qingdan = browser.find_element(By.CSS_SELECTOR,
                                       '#detail > div.tab-con > div:nth-child(2) > div.package-list').text.split(f"\n")
        info = info + brand + main_info + qingdan
        more_info = []
        for i in test:
            chulihou = i.text.split(f"\n")  # 这是一个list
            more_info = more_info + chulihou
        info = info + more_info
        browser.find_element(By.CSS_SELECTOR, "#detail > div.tab-main.large > ul > li:nth-child(5)").click()
        browser.implicitly_wait(10)
        comment = browser.find_element(By.CSS_SELECTOR,
                                       "#comment > div.mc > div.comment-info.J-comment-info > div.comment-percent").text.split(
            f"\n")
        character = browser.find_element(By.CSS_SELECTOR,
                                         "#comment > div.mc > div.comment-info.J-comment-info > div.percent-info > div").text
        character = re.sub('[\d]', '', character).replace("(", "").replace(")", "").split(f"\n")
        # print(character)
        info = info + comment
        info.append("评价特性")
        info = info + character
        # print(info)
        i = 0
        while i != len(info):
            info_dict[info[i]] = info[i + 1]
            i = i + 2
    except Exception:
        try:
            print("出错了,正在尝试采用备用方案")
            price = browser.find_element(By.CSS_SELECTOR,
                                         "body > div:nth-child(11) > div > div.itemInfo-wrap > div.summary.summary-first > div > div.summary-price.J-summary-price > div.dd > span").text.replace("￥","")
            info.append("Price")
            info.append(price)
            print(f"已获取到正确的Price{price}")
            title = browser.find_element(By.CSS_SELECTOR,
                                         "body > div:nth-child(11) > div > div.itemInfo-wrap > div.sku-name").text
            news = browser.find_element(By.CSS_SELECTOR,
                                        "body > div:nth-child(11) > div > div.itemInfo-wrap > div.news").text
            info.append("Title")
            info.append(title)
            info.append("News")
            info.append(news)
            print("已经获取到正确的news")
            brand = browser.find_element(By.CSS_SELECTOR, "#parameter-brand > li").text.split("：")
            main_info = browser.find_element(By.CSS_SELECTOR,
                                             "#detail > div.tab-con > div:nth-child(1) > div.p-parameter > ul.parameter2.p-parameter-list").text
            main_info = re.split("：|\n", main_info)
            # print(main_info)
            # print(brand + main_info)
            browser.find_element(By.CSS_SELECTOR, "#detail > div.tab-main.large > ul > li:nth-child(2)").click()
            browser.implicitly_wait(10)
            test = browser.find_elements(By.CSS_SELECTOR,
                                         "#detail > div.tab-con > div:nth-child(2) > div.Ptable > div.Ptable-item > dl > dl")
            qingdan = browser.find_element(By.CSS_SELECTOR,
                                           '#detail > div.tab-con > div:nth-child(2) > div.package-list').text.split(f"\n")
            info = info + brand + main_info + qingdan
            more_info = []
            for i in test:
                chulihou = i.text.split(f"\n")  # 这是一个list
                more_info = more_info + chulihou
            info = info + more_info
            browser.find_element(By.CSS_SELECTOR, "#detail > div.tab-main.large > ul > li:nth-child(4)").click()
            comment = browser.find_element(By.CSS_SELECTOR,
                                           "#comment > div.mc > div.comment-info.J-comment-info > div.comment-percent").text.split(
                f"\n")
            character = browser.find_element(By.CSS_SELECTOR,
                                             "#comment > div.mc > div.comment-info.J-comment-info > div.percent-info > div").text
            character = re.sub('[\d]', '', character).replace("(", "").replace(")", "").split(f"\n")
            # print(character)
            info = info + comment
            info.append("评价特性")
            info = info + character
            # print(info)
            i = 0
            while i != len(info):
                info_dict[info[i]] = info[i + 1]
                i = i + 2
        except Exception:
            print("获取失败")
    print(info_dict)
    return info_dict

def get_proxies():
    """
    此函数用来获取可用的ip地址
    :return: 返回一个proxies_list列表
    """
    import requests
    from pyquery import PyQuery as pq
    proxies_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54"
    }
    response = requests.get("https://www.beesproxy.com/free",headers=headers).text
    doc_obj = pq(response)
    ip = doc_obj("#article-copyright > figure > table > tbody > tr >td:nth-child(1)").items()
    port = doc_obj("#article-copyright > figure > table > tbody > tr >td:nth-child(2)").items()
    for j,k in zip(ip,port):
        url = "http://www.baidu.com"
        ip, port = j.text(),k.text()
        proxy = {'http':f"{ip}:{port}"}
        # print(proxy)
        try:
            res = requests.get(url, proxies=proxy, headers=headers,timeout=2)
            print(res.status_code)
            if res.status_code == 200:
                proxies_list.append(f"{ip}:{port}")
        except:
            print(f"{proxy}响应失败")
        continue
    # print(proxies_list)
    return proxies_list   #返回了一个代理ip列表

def change_proxy(browser,proxies_list):
    ip = random.choice(proxies_list)
    print(f"使用{ip}获取当前页")
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': ip  # 这里放ip就好
    })
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    proxy.add_to_capabilities(desired_capabilities)
    browser.start_session(desired_capabilities)

def save_datas(info_list):
    """
    将爬取到的数据保存至csv文件和数据库中
    :param info_list:
    :return:
    """
    from sqlalchemy import create_engine
    df = pd.DataFrame(info_list)
    df.to_csv("京东固态硬盘.csv",encoding="utf_8_sig")
    print(df.head(10))
    conn = create_engine('mysql+pymysql://root:xin010727@localhost:3306/jd_goods')  # pymysql链接数据库
    try:
        df.to_sql('goods_gutaiyingpan', conn, if_exists='replace', index=False)
    except:
        print('error')

if __name__ == '__main__':
    proxies_list = get_proxies()
    print(proxies_list)
    option = webdriver.ChromeOptions()  # 创建一个配置对象
    option.add_argument("--headless")  # 开启无界面模式
    browser = webdriver.Chrome(options=option)  # 实例化1个谷歌浏览器对象
    browser.get('https://www.jd.com/')
    add_cookies()
    search = input("请输入想要搜索的商品:")
    goods_info = search_goods(search)
    # goods_info = ['https://item.jd.com/100028004984.html', 'https://item.jd.com/4311182.html', 'https://item.jd.com/100018768506.html', 'https://item.jd.com/100010169471.html',
    #               'https://item.jd.com/100036659879.html', 'https://item.jd.com/4311178.html', 'https://item.jd.com/100008757393.html', 'https://item.jd.com/10049066548800.html', 'https://item.jd.com/100029718998.html', 'https://item.jd.com/100019517363.html', 'https://item.jd.com/100016385967.html', 'https://item.jd.com/100036659927.html', 'https://item.jd.com/100007847303.html', 'https://item.jd.com/100011216263.html', 'https://item.jd.com/100016875251.html', 'https://item.jd.com/100011213836.html', 'https://item.jd.com/100016795946.html', 'https://item.jd.com/100022451554.html', 'https://item.jd.com/100004001433.html', 'https://item.jd.com/100018768480.html', 'https://item.jd.com/100019517343.html', 'https://item.jd.com/100038325615.html', 'https://item.jd.com/100018551171.html', 'https://item.jd.com/100015242141.html', 'https://item.jd.com/10053843564657.html', 'https://item.jd.com/100002089896.html', 'https://item.jd.com/100036840219.html', 'https://item.jd.com/100007080969.html', 'https://item.jd.com/100010169469.html', 'https://item.jd.com/100004001441.html', 'https://item.jd.com/100018768506.html', 'https://item.jd.com/100025277353.html', 'https://item.jd.com/100029922516.html', 'https://item.jd.com/100036659931.html', 'https://item.jd.com/100020584692.html', 'https://item.jd.com/100035447985.html', 'https://item.jd.com/100007080969.html', 'https://item.jd.com/100022451598.html', 'https://item.jd.com/8882543.html', 'https://item.jd.com/100005493141.html', 'https://item.jd.com/100015879489.html']
    info_list = []         # 用来存放爬取到的所有数据
    flag = 0               # 用来计算每爬取几个数据就换一个ip地址
    for good in goods_info:
        try:
            info = get_goods_info(good,browser=browser)
            info_list.append(info)
            flag += 1
            if flag%10 == 0:
                change_proxy(browser=browser,proxies_list=proxies_list)
                browser.quit()
                browser = webdriver.Chrome(options=option)
                print(f"已经获取{flag}个")
        except Exception:
            print("已自动跳过")
            continue
    save_datas(info_list)
    print(f"爬取结束,共爬取到{len(info_list)}个数据,请移至csv文件 or Mysql数据库过目")




