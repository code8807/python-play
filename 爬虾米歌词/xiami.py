#encoding: utf-8
import requests
import re
import csv
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import path

name = '张韶涵'
url = 'https://api.xiami.com/web'
params = {
        'v': '2.0', 'app_key': '1', 'key':name, 'page': "1",'limit':'20','_ksTS':'1516719729973_76','callback':'jsonp77','r':'search/songs'
    }
headers = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Cookie':'gid=151671922885255; join_from=1zufSNtP6D010%2FjCCA; _xiamitoken=ebaf498f975b638642a0156325236398; _unsign_token=3fff31156dc46cf76727ca88be913afa; user_from=1; cna=mkcID/qThR0CAbSsenlrxaKj; UM_distinctid=1612382e74a9-0a552bda82686-4c322e7d-144000-1612382e74b644; isg=AuTkU9SmYjA04Jb84nIIYwkTtOEW1c90K89Prv4FcK9yqYRzJo3YdxoLGzpP; login_method=mobilelogin; member_auth=gTudSIlOuW1l16PET4E0JSxKs%2BXQEzCDxo1Uibd7tlYkLY0KMobwxquSQQ1O0CeUrlEmwwUdBYDxx1Xi%2FHUPHD0RytZUsuXV; user=336687769%22%E7%88%B1%E8%8B%8F%E8%8B%8F%E7%9C%9F%E5%A4%AA%E5%A5%BD%E5%95%A6%22images%2Fdefault%2Favatar_j.jpg%220%22177%22%3Ca+href%3D%27http%3A%2F%2Fwww.xiami.com%2Fwebsitehelp%23help9_3%27+%3ELv3%3C%2Fa%3E%220%220%222632%22f8f25bc661%221516719386',
    'Host':'api.xiami.com',
    'Referer':'https://h.xiami.com/index.html?f=&from=',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1'
}
downloadheaders = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    'Cookie':'gid=151671922885255; join_from=1zufSNtP6D010%2FjCCA; _xiamitoken=ebaf498f975b638642a0156325236398; _unsign_token=3fff31156dc46cf76727ca88be913afa; user_from=1; cna=mkcID/qThR0CAbSsenlrxaKj; UM_distinctid=1612382e74a9-0a552bda82686-4c322e7d-144000-1612382e74b644; isg=AuTkU9SmYjA04Jb84nIIYwkTtOEW1c90K89Prv4FcK9yqYRzJo3YdxoLGzpP; login_method=mobilelogin; member_auth=gTudSIlOuW1l16PET4E0JSxKs%2BXQEzCDxo1Uibd7tlYkLY0KMobwxquSQQ1O0CeUrlEmwwUdBYDxx1Xi%2FHUPHD0RytZUsuXV; user=336687769%22%E7%88%B1%E8%8B%8F%E8%8B%8F%E7%9C%9F%E5%A4%AA%E5%A5%BD%E5%95%A6%22images%2Fdefault%2Favatar_j.jpg%220%22177%22%3Ca+href%3D%27http%3A%2F%2Fwww.xiami.com%2Fwebsitehelp%23help9_3%27+%3ELv3%3C%2Fa%3E%220%220%222632%22f8f25bc661%221516719386',
    'Host':'img.xiami.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1'
}
lrcurls=[];

#获取每页URL列表
def creeperxm(page):
    pageparam = {'key':name,'page':str(page)}
    params.update(pageparam)
    response = requests.get(url,params=params,headers=headers)
    content = response.content.decode('unicode_escape')
    #字符切片，使其变成json字符串
    return content[8:-1]

#JSON处理
def getsong(content,n):
    songjson = json.loads(content)
    return (songjson['data']['songs'][n]['lyric']);

#下载歌词文件并解析
def getlrc(lrcurl):
    f = requests.get(lrcurl,headers=downloadheaders)
    lrc = (f.content)
    patten = re.compile(r'[\u4e00-\u9fa5]',re.S)
    lrc = re.sub(patten,'',lrc)
    lrc = lrc.replace('\n','').replace('.','').replace(' ','').replace('作词','').replace('作曲','').replace('编曲','').replace(name,'').replace('v','').replace('y','');
    return lrc

#CSV
def ci_frep(list):
    with open('d://'+name.decode('utf-8')+'.csv', 'wb') as csvfile:
        fieldnames = ['lrc']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for word in list:
            writer.writerow({'lrc': word})

#词云制作
def draw_wordcloud():
    #读入一个txt文件
    comment_text = open('d://'+name.decode('utf-8')+'.csv','r').read()
    #结巴分词，不使用分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    d = path.dirname(__file__) # 当前文件文件夹所在目录
    color_mask = np.array(Image.open("d://timg.jpg"))# 读取背景图片
    cloud = WordCloud(
        #设置字体，不设置就会出现乱码
        font_path="d://simhei.ttf",
        #设置背景色
        background_color='white',
        #词云形状
        mask=color_mask,
        #允许最大词汇
        max_words=2000,
        #最大号字体
        max_font_size=200,
        random_state=50
    )
    word_cloud = cloud.generate(cut_text) # 产生词云
    word_cloud.to_file('d://'+name.decode('utf-8')+'.jpg') #保存图片
    plt.imshow(word_cloud)#  显示词云图片
    plt.axis('off')
    plt.show()



if __name__ == '__main__':
    for i in range(0,3):
        content = creeperxm(i)
        for n in range (1,20):
            lrcurl = getsong(content, n)
            lrc = getlrc(lrcurl)
            lrcurls.append(lrc)
    ci_frep(lrcurls)
    draw_wordcloud()
    print('success')