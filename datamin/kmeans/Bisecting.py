#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from numpy import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import matplotlib.pyplot as pl
# general function to parse tab-delimited floats
from mpl_toolkits.mplot3d import Axes3D


def loadDataSet(fileName):
    # assume last column is target value
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\r\n')
        # map all elements to float()
        curLine = curLine[0].split(',')
        fltLine = map(float, curLine[1:])
        #fltLine = map(float, curLine)
        dataMat.append(list(fltLine))
    return dataMat


def getDistance(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k):
    n = shape(dataSet)[1]
    # create centroid mat
    centroids = mat(zeros((k, n)))
    # create random cluster centers, within bounds of each dimension
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
    return centroids


def kMeans(dataSet, k, disMens=getDistance, createCent=randCent):
    ''' 
    :param dataSet: 数据集，要求有矩阵形式 
    :param k: 指定聚类的个数 
    :param disMens: 求解距离的方式，除欧式距离还可以定义其他距离计算方式 
    :param createCent: 生成随机质心方式 
    :return:随机质心，簇索引和误差距离矩阵 
    '''
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))  # 要为每个样本建立一个簇索引和相对的误差，所以需要m行的矩阵，m就是样本数
    centRoids = createCent(dataSet, k)  # 生成随机质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # 遍历所有样本
            minDist = inf
            minIndex = -1  # 初始化最小值
            for j in range(k):  # 遍历所有质心
                disJI = disMens(centRoids[j, :], dataSet[i, :])
                if disJI < minDist:
                    minDist = disJI
                    minIndex = j  # 找出距离当前样本最近的那个质心
            if clusterAssment[i, 0] != minIndex:  # 更新当前样本点所属于的质心
                clusterChanged = True  # 如果当前样本点不属于当前与之距离最小的质心，则说明簇分配结果仍需要改变
                clusterAssment[i, :] = minIndex, minDist**2
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            # nonzero 返回的是矩阵中所有非零元素的坐标，坐标的行数与列数个存在一个数组或矩阵当中
            # 矩阵支持检查元素的操作，所有可以写成matrix == int这种形式，返回的一个布尔型矩阵，代表矩阵相应位置有无此元素
            # 这里指寻找当前质心下所聚类的样本
            # 更新当前的质心为所有样本的平均值，axis = 0代表对列求平均值
            centRoids[cent, :] = mean(ptsInClust, axis=0)
    sseSplit = sum(clusterAssment[:, 1])
    sseNotSplit = sum(clusterAssment[nonzero(
        clusterAssment[:, 0].A != i)[0], 1])
    print "sseSplit", sseSplit
    return centRoids, clusterAssment

'''
def plotKmens(dataMat, centroids):
    color = ['ro', 'bo', 'go', 'yo', 'ko', 'co']
    pl.plot(centroids[:, 0], centroids[:, 1], 'r*')
    for k,v in dataMat.items():
        for mat in v:
            pl.plot(mat[:, 0], mat[:, 1], color[k])
    pl.show()
'''


def plotKmens(dataMat, centroids):
    ''''' 
    本函数用于绘制kMeans的二维聚类图 
    :param dataSet: 数据集 
    :param k: 聚类的个数 
    :return:无 
    '''
    color = ['ro', 'bo', 'go', 'yo', 'ko', 'co']
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(centroids)
    cX = []
    cY = []
    cZ = []
    dX = []
    dY = []
    dZ = []
    (ci, cj) = shape(centroids)
    #(di, dj) = shape(dataMat)
    for i in range(ci):
        cX.append(centroids[i, 0])
        cY.append(centroids[i, 1])
        cZ.append(centroids[i, 2])
    '''    
    for i in range(di):
        dX.append(dataMat[i, 0])
        dY.append(dataMat[i, 1])
        dZ.append(dataMat[i, 2])
    '''
    for k, v in dataMat.items():
        dX = []
        dY = []
        dZ = []
        for mat in v:
            dX.append(float(mat[:, 0]))
            dY.append(float(mat[:, 1]))
            dZ.append(float(mat[:, 2]))
            #ax.plot(mat[:, 0], mat[:, 1], mat[:, 2], color[k])

        ax.plot(dX, dY, dZ, color[k])
    ax.plot(cX, cY, cZ, 'r*')

    pl.show()


def biKmeans(dataSet, k, distMeas=getDistance):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]  # create a list with one centroid
    for j in range(m):  # calc initial Error
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            # get the data points currently in cluster i
            ptsInCurrCluster = dataSet[
                nonzero(clusterAssment[:, 0].A == i)[0], :]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            # compare the SSE to the currrent minimum
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(
                clusterAssment[:, 0].A != i)[0], 1])
            # print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(
            centList)  # change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)
                     [0], 0] = bestCentToSplit
        # print 'the bestCentToSplit is: ', bestCentToSplit
        # print 'the len of bestClustAss is: ', len(bestClustAss)
        # replace a centroid with two best centroids
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]
        centList.append(bestNewCents[1, :].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[
            0], :] = bestClustAss  # reassign new clusters, and SSE
    print sum(clusterAssment[:, 1])
    return mat(centList), clusterAssment


def handle_color(dataSet, clustAssing):
    m = shape(dataSet)[0]
    new_data = {}
    for j in range(m):
        if new_data.has_key(int(clustAssing[j][:, 0])):
            new_data[int(clustAssing[j][:, 0])].append(datMat[j])
        else:
            new_data[int(clustAssing[j][:, 0])] = []
    return new_data


if __name__ == '__main__':
    datMat = mat(loadDataSet('222'))
    myCentroids, clustAssing = kMeans(datMat, 4)
    new_data = handle_color(datMat, clustAssing)
    plotKmens(new_data, myCentroids)
    # print '*********'
    #centList, myNewAssments = biKmeans(datMat, 4)
    #new_data = handle_color(datMat, myNewAssments)
    #plotKmens(new_data, centList)
