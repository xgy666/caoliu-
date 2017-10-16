import requests       #草榴内容动态加载 需要用selenium
import re
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from hashlib import md5
import threading
import multiprocessing
import time

lock=threading.Lock()

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

def get_index(start,over):
    for page in range(start,over):
#        lock.acquire()

  #      try:
        print('正在运行%s'%threading.current_thread().name)
        url='http://t66y.com/thread0806.php?fid=16&search=&page=%d'%page
        print(url)
        get_hrefs(url)
   #     finally:
   #         lock.release()

def get_html(url):

    try:
        response=requests.get(url,headers=headers)
        time.sleep(5)    #延迟有猪狗的时间来获取html防止加载失败
      #      print(response.status_code)
        if response.status_code==200:
            html=response.text
            return html
        else:
            return None
    except Exception:
        print('false')
        return None

def get_hrefs(url):
    html=get_html(url)
    if html:
        if re.compile('<a href="(.*?)" target="_blank">'):
            pattern =re.compile('<a href="(.*?)" target="_blank">')
            hrefs=re.findall(pattern,html)
    #        get_images(hrefs[2:5])   #切片 只获取一部分网页
            get_images(hrefs)
def get_images(hrefs):

    for href in hrefs:
        url='http://t66y.com/'+href     #获得绝对地址
        print(url)
        html=get_html(url)
        if html:      #首先要判断html是否存在
            doc=pq(html)
            if doc('input[type="image"]'):      #PyQuery获取标签方法
                inputs=doc('input[type="image"]').items()   #items获取内部所有内容
         #       print(type(inputs))
          #      print(inputs)
                for kk in inputs:
                    images=kk.attr('src')    #soup获取src的方法

                    get_to_file(images)
num=0
def get_to_file(images):
    global num       #全局变量
    try:
        res=requests.get(images,headers=headers)
        file_path='{}/{}.{}'.format('f:\caoliu',md5(res.content).hexdigest(),'jpg')  #设置图片路径  并且使用md5排除重复路径

        with open(file_path, 'wb') as f:
            f.write(res.content)
            f.close
            num += 1
            print('正在写入第%d张' % num)
    except Exception:
        return None

def multiple_threads():
    threads=[]
    page_list=[
        (2,41),
        (41,81),
        (81,101)
        ]
    for page in page_list:
        th=threading.Thread(target=get_index,args=(page[0],page[1]))
        threads.append(th)
    for th in threads:
        th.start()
    for tr in threads:
        tr.join()

"""
def multiple_processing():
    pool=multiprocessing.Pool(processes=4)
    page_list = [
        (3, 41),
        (46, 81),
        (81, 101)
    ]
    for page in page_list:
        pool.apply_async(get_index,(page[0],page[1]))
    pool.close()
    pool.join()"""

if __name__=='__main__':
    multiple_threads()





