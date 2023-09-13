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
