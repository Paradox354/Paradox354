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
