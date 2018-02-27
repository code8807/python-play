import csv
import matplotlib.pyplot as plt

districtsName = ['baoshan','changning','jingan','pudong','songjiang','xuhui']
districtAvg=[]

def count(name):
    csvFile = open("d:/%s.csv"%name, "r",encoding='UTF-8')
    dict_reader = csv.DictReader(csvFile)
    temp = []
    for row in dict_reader:
        if (row['单位'].strip() =='元/平'):
            temp.append(row['价格'])
    #去重
    temp = list(set(temp))
    sum = 0
    for price in temp:
        sum = sum+int(price)
    districtAvg.append(sum/int(len(temp)))
def coldia():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(districtsName,districtAvg)
    plt.grid('true')
    plt.title('Shanghai price map ')
    plt.show()

if __name__=='__main__':
    for district in districtsName:
        count(district)
    coldia()