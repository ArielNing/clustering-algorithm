#coding=utf-8
from numpy import *
import sys

# 读取数据
def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)
    return mat(dataMat)


# 计算两个向量的距离，用的是欧几里得距离
def distEclud(a, b):
    return sqrt(sum(power(a - b, 2)))


# 随机生成初始的质心
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centers = mat(zeros((k, n)))
    for j in range(n):
        min_j = min(dataSet[:, j])
        range_j = float(max(dataSet[:, j]) - min_j)
        centers[:, j] = min_j + range_j * random.rand(k, 1)
    return centers


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))  # create mat to assign data points
    centers = createCent(dataSet, k)
    hasChanged = True
    while hasChanged:
        hasChanged = False
        for i in range(m):  # for each data point assign it to the closest center
            minDist = inf
            minIndex = -1
            for j in range(k):
                dist_ji = distMeas(centers[j, :], dataSet[i, :])
                if dist_ji < minDist:
                    minDist = dist_ji;
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                hasChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        for cent in range(k):  # recalculate centers
            point_of_clusters = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # get all the point in this cluster
            centers[cent, :] = mean(point_of_clusters, axis=0)  # assign centroid to mean
    return centers, clusterAssment


def main(file):
    dataMat = loadDataSet(file)
    centers, clustAssing = kMeans(dataMat, 4)
    print (centers)
    print(clustAssing[:,0])

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("error usage")
    else:
        main(sys.argv[1])