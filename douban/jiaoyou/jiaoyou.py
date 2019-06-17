from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import datetime
import pymongo
from pymongo import MongoClient
from dateutil import parser

start=datetime.datetime.now() 
driver=webdriver.Chrome()             
driver.get("https://www.douban.com/gallery/topic/51644/?sort=new&from=gallery_following_post&guest_only=0")
client = MongoClient('localhost', 27017) 
collection=client.dou.jiaoyou

def scroll_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print('scroll number:'+str(i))
        time.sleep(5)


# driver.find_element_by_link_text('登录').click()
def analyze_topic():
    html=driver.page_source
    bs=BeautifulSoup(html,'lxml')
#     topics=bs.find_all(class_='topic-item item-status')
    topics=bs.select('.topic-item')
    for topic in topics:
        user={}
        img_url_list=[]
        author=topic.find("a",class_="author")
        time=topic.find("time")
        user['name']=author.text
        user['url']=author['href']
        user['create_time']=parser.parse(time.text)
        desc=topic.find("p",class_='status-full')
        if desc is not None:
            user['desc']=desc.text
            user['note']=False
        else:
            desc=topic.find(class_='note-preview-content')
            user['desc']=desc.text
            user['note']=True
        imgs=topic.find_all(class_='img-wrapper')
        for img in imgs:
            img_tag=img.find('img')
            img_url_list.append(img_tag['src'])
        user['imgs']=img_url_list
        save_to_mongo(user)


def log_file():
    output_path = 'C:/backup/'
    output_file='output_'
    output = os.path.join(output_path, output_file+f"{datetime.datetime.now():%Y%m%d-%H%M%S}")
    with open(output,'wt',encoding="utf8") as f:
        f.write(str(driver.page_source))

def save_list_to_mongo(data_list):
    collection.insert_many(data_list)

def save_to_mongo(data):
    duplicate=is_duplicate(data)
    if not duplicate:
        collection.insert_one(data) 

def is_duplicate(data):
    one=collection.find_one({"url":data['url']}) 
    existing=False
    if one is None:
        existing=False
    else:
        existing=True
    return existing

def drop(to):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-"+str(to)+");")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(8)
    loaded=check_loading()
    if not loaded:
        time.sleep(10)
        drop(400)

def action():
    drop(600)
    driver.execute_script("var root=document.getElementById('topic-items').childNodes[0];var i=root.childNodes.length-20;while (i>0) {root.removeChild(root.firstChild);i--;}")

def check_loading():
    html=driver.page_source
    bs=BeautifulSoup(html,'lxml')
    topics=bs.select('.topic-item')
    loaded=False
    if len(topics)>20:
        loaded=True
    return loaded

def run():
    time.sleep(5)
#     scroll_times(905)
#     log_file()
    loop=1000
    while loop>0:
        analyze_topic()
        action()
        loop=loop-1
    end=datetime.datetime.now()
    span=(end-start)
    print('total seconds:'+str(span.seconds))


run()