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

# 计算欧几里得距离
def distEclud(a, b):
    a=mat(a)
    b=mat(b)
    return sqrt(sum(power(a - b, 2)))

# 最短距离
def dist_min(Ci, Cj):
    return min(distEclud(i, j) for i in Ci for j in Cj)
# 最长距离
def dist_max(Ci, Cj):
    return max(distEclud(i, j) for i in Ci for j in Cj)
# 类平均距离
def dist_avg(Ci, Cj):
    return sum(distEclud(i, j) for i in Ci for j in Cj)/(len(Ci)*len(Cj))

#找到距离最小的下标
def findMin(M):
    min = inf
    x = 0; y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i != j and M [i][j] < min:
                min = M[i][j];x = i; y = j
    return (x, y, min)


def HCluster(dataset, dist, k):
    # initialize C and M
    C = [];M = []
    for i in dataset:
        Ci = []
        Ci.append(i)
        C.append(Ci)
    for i in C:
        Mi = []
        for j in C:
            Mi.append(dist(i, j))
        M.append(Mi)
    q = len(dataset)
    # union and update
    while q > k:
        x, y, min = findMin(M)
        C[x].extend(C[y])
        C.remove(C[y])
        M = []
        for i in C:
            Mi = []
            for j in C:
                Mi.append(dist(i, j))
            M.append(Mi)
        q -= 1
    return C

def main(file):
    C = HCluster(loadDataSet(file), dist_min, 4)
    print(C)

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("error usage")
    else:
        main(sys.argv[1])




