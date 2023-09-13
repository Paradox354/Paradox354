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
