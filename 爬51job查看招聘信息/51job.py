import requests
from bs4 import BeautifulSoup
import re
import csv
careers = []

url = 'http://m.51job.com/search/joblist.php'
params = {
        'jobarea': '020000', 'keyword': '大数据', 'keywordtype': '2', 'pageno': "1"
    }

#职业类
class CareerInfo:
    name=''
    time=''
    area=''
    wage=''
    recNum=''
    exp=''
    detail=''

#获取每页URL列表
def creeper51(page):
    careers = []
    pageparam = {'pageno':str(page)}
    params.update(pageparam)
    response = requests.get(url,params=params)
    content = response.content
    bs = BeautifulSoup(content,"lxml")
    list = bs.find_all("a",href=re.compile('http://m.51job.com/search/jobdetail.php\?jobid'))
    for a in list:
        r = re.compile(r'http://m.51job.com/search/jobdetail.php\?jobid=\d*&amp;jobtype=0')
        if (r.findall(str(a)) != []):
            careers.append(r.findall(str(a))[0])
    return careers

def getPageNum():
    response = requests.get(url, params=params)
    content = response.content
    bs = BeautifulSoup(content, "lxml")
    # 获得页码
    resultHtml = bs.find("p", class_='result')
    pattern = re.compile(r'[1-9]\d*')
    resultHtml = pattern.findall(str(resultHtml))[0]
    return int(resultHtml) / 30

#解析每页信息
def getInfo(list):
        for perurl in list:
            response = requests.get(perurl)
            bs = BeautifulSoup(response.content.decode("utf-8"), "lxml")
            pattern = re.compile(r'<div class="jt">.*?<p>(.*?)</p>.*?<span>(.*?)</span>.*?<em>(.*?)</em>', re.S)
            info = pattern.findall(str(bs))
            c = CareerInfo()
            c.name = info[0][0]
            c.time = info[0][1]
            c.area = info[0][2]
            c.wage = bs.find('p', class_='jp').text
            c.recNum = '' if bs.find('span', class_='s_n')==None else bs.find('span', class_='s_n').text
            c.exp = bs.find('p',class_='c_444').text
            c.detail = bs.find('article').text.strip()
            careers.append(c)
        return careers

#生成CSV
def createCsv(list):
    with open('d://names.csv','w+',encoding='utf-8',  newline='') as csvfile:
        fieldnames = ['工作名称', '创建时间', '工作地区', '工资', '招聘人数', '工作经验', '职业描述']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in careers:
            writer.writerow(
            {'工作名称': c.name, '创建时间': c.time, '工作地区': c.area, '工资': c.wage,
             '招聘人数': c.recNum, '工作经验': c.exp, '职业描述': c.detail})

if __name__ == '__main__':
    sum_page = int(getPageNum());

    for i in range(1,sum_page):
        list1 = creeper51(i)
        list2 = getInfo(list1)
        createCsv(list2)

    print ("success")