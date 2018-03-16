#-*- encoding: utf-8 -*- #注意此处为小写
'''
Created on 2015年3月9日
@author: momo
'''
from __future__ import division 
import pickle,pprint
from collections import namedtuple
from emd import emd
from cut_image import Similarity,Img_similarity


'''
@function:获取图像的位置信息，纹理特征，dct特征
'''
def get_features(filename):
    pkl_file = open(filename, 'rb') 
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
'''
@function:选择标准：对图片面积大小(长宽至少一个不小于80只要不小于logo大小的统计值即可，比例)、超过图像范围、没有纹理特征的
'''
def check_rect(data):
    D = []
    for i in data:
        if i[4] >100 and i[5]>100 and i[3] < 1903 and len(i[8]) !=0 and i[10][1] != 0.0: #是否需要添加dct!=0 and array[1] != 0.0(对称图像)
            D.append([])
            D[-1] = [i[9],i[8],i[10]]
    return D
'''
@function:纹理距离，待图像分类后补充
'''
def textural_dis(initial,target):
    print "initial",len(initial),len(target)
    Mat= Similarity(initial,target)
    #raw_input("textural")
#     print "两图的相似性矩阵Mat为：",Mat
    similarity = Img_similarity(Mat)
    print "匈牙利相似性为similarity",similarity
    return 1-similarity

'''
@function:dct距离,利用dct系数中相同个数
'''
def dct_dis(d1,d2):
    count = 0
    length = len(d1)
    for i in range(length):
            if d1[i] != d2[i]:
                count = count + 1
    return count/length #相似性为不同元素的比例
'''
@function:位置距离,二进制异或运算，不同为1计算1的个数
'''
def locate_dis(a,b):
    count = 0
    for n in range(8):
        if a[n] != b[n]:
            count = count+1
    return count/8
       
'''
@function:两个元素间的距离公式[种类，二进制位置，纹理]
'''
def Distance(f1,f2):
	    
	    print "f1[2]---",f1
	    print "f2[2]-----",f2
	    if f1[0] == f2[0]:
		ratio = locate_dis(f1[1],f2[1])
		print "ratio is---",ratio
		if  f1[0] ==0: #logo或增信图标,计算纹理相似性
		   # print "class is",f1[0]
		    Dis_tex = textural_dis(f1[2],f2[2])
		    print "Dis_tex is",Dis_tex
		    element = 0.5*ratio + 0.5*Dis_tex 
		    print "0 class element is,",element
		    raw_input("0 distance")
		else :#计算dct相似性 
		    Dis_dct = dct_dis(f1[2],f2[2])
		    #print "Dis_dct is",Dis_dct
		    #raw_input("1 distance")
		    element = 0.5*ratio+0.5*Dis_dct
		    #print "1 class element is,",element
		
	    else:
		element = 1.0
	    return element

def main():
	    features1 =check_rect(get_features('emd_mxye.pkl'))
	    weight1 =[1/len(features1) for i in range(len(features1))]  #features1中每个元素的权重
	    features2 = check_rect(get_features('emd_nhwd.pkl'))
	    weight2 = [1/len(features2) for i in range(len(features2))]
	    print "result"
	    R= emd((features1,weight1),(features2,weight2),Distance)
    	    print "Result is",R
if __name__=="__main__":
    main()
