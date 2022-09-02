# @time:2022/8/31 18:11
# @Author:玉衡Kqing
# @File:test_multiprocessing.py
# @Software:PyCharm

import time
import requests
from multiprocessing.dummy import Pool
#测试多线程



def query(url):
    requests.get(url)
start = time.time()
for i in range(1,17):
    query("https://www.csdn.net/")
end = time.time()
dan = end - start
print(f"单线程循环访问16次csdn，耗时{dan}")


url_list = []
for i in range(17):
    url_list.append("https://www.csdn.net/")
for j in range(2,17):
    pool = Pool(j)
    start = time.time()
    pool.map(query,url_list)
    end = time.time()
    duo = end - start
    print(f"{j}线程循环访问16次csdn，耗时{duo}")
    print(f"{j}线程比单线程优化了{duo/dan}")
    time.sleep(10)

# 结论:  9线程性价比最高，在不大幅度提升损耗的情况下，优化进程速度