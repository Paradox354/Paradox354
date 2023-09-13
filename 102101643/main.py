import re
import time
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import jieba
import pandas as pd
import wordcloud
import threading
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.69"}
#此函数返回同一关键字不同页面的url

def video(a: int):
    b = (a-1) * 30
    # 观察发现b站搜索关键字’日本核污染水排海‘网站翻页的url具有page+1&&o+30的规律
    return f'https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%9F%93%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page={a}&o={b}'
#此函数获取综合排名前300的视频链接
def get_video_url(k: int):
    driver = webdriver.Edge()  #利用edge浏览器驱动
    for i in range(k):
        url = video(i+1) #获取关键字’日本核污染水排海‘网站翻页的url
        driver.get(url)  #前面已从库函数中调用selenium 利用edge浏览器驱动进入b站搜索关键字’日本核污染水排海‘网站
        time.sleep(20) # 等待页面加载完成后，获取视频链接
        # print(driver)
        #利用xpath捕获视频链接标签 捕获所有div标签里具有class="bili-video-card__wrap __scale-wrap类&&target="_blank"属性的标签
        video_elements = driver.find_elements(By.XPATH, '//div[@class="bili-video-card__wrap __scale-wrap"]/a[@target="_blank"]')
        for element in video_elements:
            link = element.get_attribute('href')  #利用selenium中的get_attribute捕获element中href属性的值
            # print(link)  #用于测试是否捕获正确
            # 将链接保存到文件，也可保存到列表 文件按utf-8编码 防止出现乱码
            with open("url.txt", "a+", encoding="utf-8") as fp:
                fp.write(link + '\n')  #方便后续按行读取
    driver.quit()  #退出浏览器
def process_url(url): #处理url :提取url中的实际有效的标志不同的视频的元素
    a=re.findall('https://www.bilibili.com/(.*)',url)  #利用正则表达式提取
    return 'https://www.ibilibili.com/'+a[0]
def dan_mu_url(url):
    #print(url)
    video_api=requests.get(url,headers=headers).text  #请求b站视频api接口并返回 里面有弹幕网页地址
    video_api=etree.HTML(video_api)  #解析对象 为了后续xpath的使用方便
    dan_mu_div=video_api.xpath('//*[@id="dtl"]/div') #先捕获具体弹幕地址的div标签
    c = {}
    for i in dan_mu_div:
        disc=i.xpath(".//text()")[1]
        url=i.xpath('./input/@value')[0]  #捕获弹幕api的url
        c[disc] = url
    t=dan_mu(c['弹幕地址:'])
    # print(t)
    with open('弹幕.txt','a+',encoding='utf-8')as fp:
        #fp.write(str(c)+'\n')
        for i in t:
            fp.write(i+'\n')
def dan_mu(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # response = response.text
    word = re.findall('">(.*?)</d>',response.text)
    return word
def read_url(url_file):
    with open(url_file,'r',encoding='utf-8')as fp:
        url = fp.readlines()  #按行读取url
        for i in url:
            dan_mu_url(process_url(i))
def jie():
    f = open('弹幕.txt',encoding='utf-8')
    text = f.read()
    cut_word=jieba.lcut(text)  #利用jieba进行分词
    cut_word=' '.join(cut_word)  #将列表转换成字符串
    #词云图配置
    wt=wordcloud.WordCloud(width=500,height=500,background_color='white',font_path='msyh.ttc',stopwords = {"的", "是", "吧","啊","了","!"})
    wt.generate(cut_word)  #加载词云图
    wt.to_file(f'词云.png')  #输出词云图
def collect():
    with open('弹幕.txt','r',encoding='utf-8') as fp:
        data = fp.read()
        contents = data.split('\n')  #去除换行符‘\n’
        #统计不同弹幕出现的次数
        content_count = {}
        for content in contents:
            if content not in content_count:
                content_count[content] = 1
            else:
                content_count[content] += 1
        sorted_content = sorted(content_count.items(), key=lambda d: d[1], reverse=True)  #按出现次数从大到小排序，并转换成列表
        #print(sorted_content)
        df = pd.DataFrame(sorted_content, columns=('弹幕', '次数')) #用panda库转换
        # 写入Excel文件
        df.to_excel('弹幕统计数据.xlsx', index=False)
if __name__=='__main__':
    #进入函数前格式化文件
    with open("url.txt", "a+", encoding="utf-8") as fp:
        fp.seek(0)
        fp.truncate()
    start_time = time.time()
    get_video_url(8)
    end_time = time.time()
    print(f'get_video_url(8) 执行时间：{end_time-start_time}秒')
    with open("弹幕.txt", "a+", encoding="utf-8") as fp:
        fp.seek(0)
        fp.truncate()
    start_time = time.time()
    read_url('url.txt')
    end_time = time.time()
    print(f"read_url('url.txt') 执行时间：{end_time - start_time}秒")
    with open("弹幕统计数据.xlsx", "a+", encoding="utf-8") as fp:
        fp.seek(0)
        fp.truncate()
    thread1 = threading.Thread(name='t1',target=jie)
    thread2 = threading.Thread(name='t2', target=collect)
    thread1.start()
    thread2.start()
