#-*- encoding: utf-8 -*- #注意此处为小写
'''
Created on 2015年3月9日
@author: momo
'''
from __future__ import division 
import pickle,pprint
from collections import namedtuple
from emd import emd
import math
import numpy as np
'''
@function:获取图像的位置信息，纹理特征，dct特征
'''
def get_features(filename):
    pkl_file = open(filename, 'rb') 
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
'''
@function:选择部分数据用于计算距离，class,name,[dct,[split]],location
'''
def check_rect(data):
    D = []
    for i in data:
        D.append([])
        D[-1] = [i[8],i[7],i[10:],i[9]]  #class,name,[features],location
    return D
'''
@function:纹理距离，待图像分类后补充
'''
def textural_dis(initial,target):
    Mat= Similarity(initial,target)
    #raw_input("textural")
#     print "两图的相似性矩阵Mat为：",Mat
    similarity = Img_similarity(Mat)
    #print "匈牙利相似性为similarity",similarity
    return 1-similarity
def Similarity(Img_initial,Img_target):
    m = len(Img_initial)
    n = len(Img_target)
    Mat = np.empty([m,n],dtype=np.float32)
    A_M = np.empty([m,n],dtype=np.float32)
    for m in range(len(Img_initial)):
        iterm_initial = Img_initial[m][4:]
#         print "iterm_initial",iterm_initial
#         raw_input("iterm_initial")
        for n in range(len(Img_target)):
            Sum = 0
            iterm_target = Img_target[n][4:]   
            for j in range(len(iterm_initial)-1): #除Hu矩外，均计算每维特征之间的相似性，均使用S=1-D(F-F)/Max(F)
#                 print "iterm_initial[j],iterm_target[j],",j,iterm_initial[j],iterm_target[j]
                if iterm_initial[j] > iterm_target[j]:
                    num = iterm_initial[j]
                    Sub_Similarity = 1-math.fabs(iterm_initial[j]-iterm_target[j])/num
#                     print "iterm_initial[j] > iterm_target[j] Sub_similarity ,",Sub_Similarity
#                     raw_input("similarity") 
                elif iterm_target[j] != 0 :
                    num = iterm_target[j]
                    Sub_Similarity = 1-math.fabs(iterm_initial[j]-iterm_target[j])/num
#                     print "iterm_target[j] != 0 Sub_similarity ,",Sub_Similarity
#                     raw_input("similarity")
                else:
                    Sub_Similarity = 0 #如果两个视觉元素均为0，相似性
                #print " Sub_similarity ,",Sub_Similarity
                #raw_input("similarity")
                Sum =Sum +Sub_Similarity 
            Sa =iterm_initial[-1] #Hu矩的相似性http://www.cnblogs.com/skyseraph/archive/2011/07/19/2110183.html 中方法
            Ta = iterm_target[-1]
            dSa = 0
            dS = 0
            dT = 0
            for num in range(7):
                temp = math.fabs(Sa[num]*Ta[num])
                dSa = dSa+temp
                dS =dS+math.pow(Sa[num], 2)
                dT = dT+math.pow(Ta[num], 2)
            if dS*dT == 0:
                Hu_Similarity = 0
            else:
                Hu_Similarity = dSa/(math.sqrt(dS)*math.sqrt(dT))
            Similarity = 0.2*(Sum+Hu_Similarity)

            Mat[m][n] = Similarity
            A_M[m][n] = 1-Similarity
    #print "相似性矩阵为",mat
    return Mat
'''
使用匈牙利算法计算两幅图的相似性
'''
import munkres_sparse
def Img_similarity(mat):
    list = []
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            list.append([])
            list[-1]=(i,j,1-mat[i][j])  
    km = munkres_sparse.munkres(list)
    sum = 0
    for iterm in km:
        i,j = iterm
        sum = sum + mat[i][j]
    if len(km) ==0:
	return 0.0
    similarity = sum/len(km)
    return similarity
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
def distance(f1,f2):
    if f1[0] == f2[0]:
        ratio = locate_dis(f1[3],f2[3])
        if f1[0] ==1 or f1[0]==4: #logo或增信图标,计算纹理相似性
            dis_dct = dct_dis(f1[2][0],f2[2][0])
            dis_tex = textural_dis(f1[2][1],f2[2][1])
            element = 0.5*ratio + 0.25*dis_tex+0.25*dis_dct
        else :#计算dct相似性 
            dis_dct = dct_dis(f1[2],f2[2])
            element = 0.5*ratio+0.5*dis_dct		
    else:
        element = 1.0
    return element
'''
@function:两个元素的位置距离
'''
def dis_location(f1,f2):
    ratio = locate_dis(f1[3],f2[3])
    return ratio


'''
@function:两个元素视觉距离
'''
def dis_visual(f1,f2):
    print "f1,f2",f1
    print "f2",f2
    if f1[0]==f2[0]:
	if f1[0]==1 or f1[0]==4:
	    dis_dct = dct_dis(f1[2][0],f2[2][0])
            dis_tex = textural_dis(f1[2][1],f2[2][1])
	    if dis_tex == 0.0:
		element = dis_dct
	    else:
		element = 0.5*dis_dct+0.5*dis_tex
	else:
	    element = dct_dis(f1[2],f2[2])
    else:
	element = dct_dis(f1[2][0],f2[2][0])
    print "element",element
    return element
    
def main():
    emd_list=[]
    Min_goal_location =1
    Min_goal_visual = 1
    Min_black_location = 1
    Min_black_visual=1
    file = open('result.txt','wb')
    test_list= get_features('svips_detect_visual.pkl')
    print "len of test_list is",len(test_list)
    raw_input("test")
    black_list = get_features('vips_black_visual.pkl')
    print "length of white",len(black_list)
    raw_input("goal")
    #weight1 = [1/len(features1) for i in range(len(features1))]
    goal_list =get_features('vips_white_visual.pkl')
    for test_url in test_list.keys():
    	Min_goal_location =1
    	Min_goal_lurl =''
    	Min_goal_visual = 1
	Min_goal_vurl = ''
    	Min_black_visual=1
	Min_black_vurl = ''
    	Min_black_location = 1
	Min_black_lurl = ''
	features1=test_list[test_url]
    	if len(features1)>50:
	    continue
	weight1 = [1/len(features1) for i in range(len(features1))]
    	for goal_url in goal_list.keys():
		features2 =goal_list[goal_url]
        	if len(features2)>50:
		    continue
		weight2 =[1/len(features2) for i in range(len(features2))]  #features1中每个元素的权重
        	#emd_dis = emd((features1,weight1),(features2,weight2),distance)
        	emd_goal_location = emd((features1,weight1),(features2,weight2),dis_location)
		if emd_goal_location < Min_goal_location:
			Min_goal_location = emd_goal_location
			Min_goal_lurl = goal_url
        	emd_goal_visual = emd((features1,weight1),(features2,weight2),dis_visual)
		if emd_goal_visual < Min_goal_visual:
			Min_goal_visual = emd_goal_visual
			Min_goal_vurl = goal_url
	for black_url in black_list.keys():
		features2 = black_list[black_url]
		if len(features2)>50:
		    continue
		weight2 = [1/len(features2) for i in range(len(features2))]
        	emd_black_location = emd((features1,weight1),(features2,weight2),dis_location)
		if emd_black_location < Min_black_location:
			Min_black_location = emd_black_location
			Min_black_lurl = black_url
        	emd_black_visual = emd((features1,weight1),(features2,weight2),dis_visual)
		if emd_black_visual < Min_black_visual:
			Min_black_visual = emd_black_visual
			Min_black_vurl = black_url
	file.write(str(test_url)+' '+str(Min_goal_lurl)+' '+str(1-Min_goal_location)+' '+str(Min_goal_vurl)+' '+str(1-Min_goal_visual)+' '+
				     str(Min_black_lurl)+' '+str(1-Min_black_location)+' '+str(Min_black_vurl)+' '+str(1-Min_black_visual)+'\n')
#	print emd_dis_location,emd_dis_visual
#	raw_input("item")
    file.close()
if __name__=="__main__":
    main()
