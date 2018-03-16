#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from numpy import *
from sklearn.cluster import KMeans
import numpy as np
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def loadDataSet(fileName):
    # assume last column is target value
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\r\n')
        # map all elements to float()
        curLine = curLine[0].split(',')
        fltLine = map(float, curLine)
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


def plotKmens(dataSet, k, clusterMeans):
    ''''' 
    本函数用于绘制kMeans的二维聚类图 
    :param dataSet: 数据集 
    :param k: 聚类的个数 
    :return:无 
    '''
    centPoids, assment = clusterMeans(dataSet, k)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataSet[:, 0], dataSet[:, 1], c='blue')
    ax.scatter(centRoids[:, 0], centRoids[:, 1], c='red', marker='+', s=70)
    plt.show()


class Km:

    def __init__(self):
        pass

    def load_data(self, fileName):
        mat_array = []

        if os.path.exists(fileName):
            with open(fileName, 'r') as f:
                content = f.read().split('\n')
                for one_data in content:
                    tmp_data = one_data.split(',')
                    tmp_data = map(float, tmp_data)
                    mat_array.append(tmp_data)
                return mat_array
        else:
            return [[]]

    def cluster(self, mat_array, n_clusters, disMens=getDistance, createCent=randCent):
        kmeans = KMeans(n_clusters, random_state=5).fit(mat_array)
        return kmeans.cluster_centers_, kmeans.labels_, kmeans.inertia_


if __name__ == '__main__':
    k = Km()
    mat_array = k.load_data("./3D_spatial_network")
    kk = 6
    cluster_centers_,labels_,inertia =   k.cluster(mat_array, 6)
    print inertia