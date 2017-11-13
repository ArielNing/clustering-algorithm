#coding=utf-8
from numpy import *
import sys
# 读取数据
def loadDataSet(fileName):
    data = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        data.append(fltLine)
    return data

# 计算距离，欧几里得距离
def distEclud(a, b):
    a=mat(a)
    b=mat(b)
    return sqrt(sum(power(a - b, 2)))

# 随机生成第一个聚类中心
def randFirstCent(dataSet):
    m=shape(dataSet)[0]
    r=random.randint(0,m-1)
    return dataSet[r],r

# 最大最小距离算法
def MaxMinDist(dataSet,theta,dist=distEclud,firstCent=randFirstCent):
    maxDist=0  # C1与C2的距离
    m=shape(dataSet)[0] # 样本数目
    minDists=zeros((m,1)) # 每次迭代中每个样本与聚类中心的最小距离
    cents=[] # 聚类中心
    centsNum=[] # 聚类中心点索引
    clusterAssment=zeros((m,1)) # 划分
    cent1,index=firstCent(dataSet) # 随机选取第一个聚类中心
    cents.append(cent1)
    centsNum.append(index)
    k=1 # 聚类中心数 迭代次数
    for i in range(m):
        minDists[i]=dist(dataSet[i],cent1)
        clusterAssment[i]=1
        if(maxDist<minDists[i]):
            maxDist=float(minDists[i])
            index=i
    cents.append(dataSet[index])
    centsNum.append(index)
    clusterAssment[index]=2
    minDists[index]=0
    k=k+1
    hasNext=True # 存在新的聚类中心
    while hasNext:
        hasNext=False
        for i in range(m):
            if minDists[i]!=0:
                d=dist(dataSet[i],cents[k-1]) # 计算与新的聚类中心的距离
                if minDists[i]>d:
                    minDists[i]=d
                    clusterAssment[i]=k
        max=0 # 寻找m个最小距离中的最大距离
        for i in range(m):
            if (max<minDists[i]) and (minDists[i]!=0)and i not in centsNum :
                max=minDists[i]
                index=i
        if max>(maxDist*theta): # 判断
            hasNext=True
            k=k+1
            cents.append(dataSet[index])
            centsNum.append(index)
            clusterAssment[index]=k
            minDists[index]=0
    return cents,clusterAssment

def main(file):
    data = loadDataSet(file)
    centers, clusterAssing = MaxMinDist(data, 0.5)
    print(centers)
    print(clusterAssing)

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("error usage")
    else:
        main(sys.argv[1])











