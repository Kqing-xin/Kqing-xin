# @time:2022/9/22 9:20
# @Author:玉衡Kqing
# @File:change_proxy.py
# @Software:PyCharm
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def changeProxy(browser):
    option = webdriver.ChromeOptions()  # 创建一个配置对象
    option.add_argument("--headless")  # 开启无界面模式
    from selenium.webdriver.common.proxy import Proxy, ProxyType
    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': '47.95.199.44:80'   #这里放ip就好
    })
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    proxy.add_to_capabilities(desired_capabilities)
    return browser.start_session(desired_capabilities,option=option)


browser = webdriver.Chrome()
changeProxy(browser)
browser.get("http://httpbin.org/get")
print(browser.page_source)

