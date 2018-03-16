# -*- encoding: utf-8 -*- #注意此处为小写
'''
Created on 2015年3月9日
@author: momo
'''
from __future__ import division
from emd import emd
import math
import numpy as np
import munkres_sparse
'''
@function:获取图像的位置信息，纹理特征，dct特征
'''


class ViewEmd():

    def __init__(self, mysql_handle, mongo_operate, task_id, task_start_time, protected_title_dict, counterfeit_title_dict):
        self.mysql_handle = mysql_handle
        self.mongo_operate = mongo_operate
        self.task_id = task_id
        self.task_start_time = task_start_time
        self.protected_title_dict = protected_title_dict
        self.counterfeit_title_dict = counterfeit_title_dict

    '''
    @function:纹理距离，待图像分类后补充
    '''

    def textural_dis(self, initial, target):
        Mat = self.Similarity(initial, target)
        # raw_input("textural")
    #     print "两图的相似性矩阵Mat为：",Mat
        similarity = self.Img_similarity(Mat)
        # print "匈牙利相似性为similarity",similarity
        return 1 - similarity

    def Similarity(self, Img_initial, Img_target):
        m = len(Img_initial)
        n = len(Img_target)
        Mat = np.empty([m, n], dtype=np.float32)
        A_M = np.empty([m, n], dtype=np.float32)
        for m in range(len(Img_initial)):
            iterm_initial = Img_initial[m][4:]
    #         print "iterm_initial",iterm_initial
    #         raw_input("iterm_initial")
            for n in range(len(Img_target)):
                Sum = 0
                iterm_target = Img_target[n][4:]
                # 除Hu矩外，均计算每维特征之间的相似性，均使用S=1-D(F-F)/Max(F)
                for j in range(len(iterm_initial) - 1):
                    # print
                    # "iterm_initial[j],iterm_target[j],",j,iterm_initial[j],iterm_target[j]
                    if iterm_initial[j] > iterm_target[j]:
                        num = iterm_initial[j]
                        Sub_Similarity = 1 - \
                            math.fabs(iterm_initial[j] - iterm_target[j]) / num
    #                     print "iterm_initial[j] > iterm_target[j] Sub_similarity ,",Sub_Similarity
    #                     raw_input("similarity")
                    elif iterm_target[j] != 0:
                        num = iterm_target[j]
                        Sub_Similarity = 1 - \
                            math.fabs(iterm_initial[j] - iterm_target[j]) / num
    #                     print "iterm_target[j] != 0 Sub_similarity ,",Sub_Similarity
    #                     raw_input("similarity")
                    else:
                        Sub_Similarity = 0  # 如果两个视觉元素均为0，相似性
                    # print " Sub_similarity ,",Sub_Similarity
                    # raw_input("similarity")
                    Sum = Sum + Sub_Similarity
                # Hu矩的相似性http://www.cnblogs.com/skyseraph/archive/2011/07/19/2110183.html
                # 中方法
                try:
                    Sa = iterm_initial[-1]
                    Ta = iterm_target[-1]
                except:
                    continue
                dSa = 0
                dS = 0
                dT = 0
                for num in range(7):
                    temp = math.fabs(Sa[num] * Ta[num])
                    dSa = dSa + temp
                    dS = dS + math.pow(Sa[num], 2)
                    dT = dT + math.pow(Ta[num], 2)
                if dS * dT == 0:
                    Hu_Similarity = 0
                else:
                    Hu_Similarity = dSa / (math.sqrt(dS) * math.sqrt(dT))
                Similarity = 0.2 * (Sum + Hu_Similarity)

                Mat[m][n] = Similarity
                A_M[m][n] = 1 - Similarity
        # print "相似性矩阵为",mat
        return Mat
    '''
    使用匈牙利算法计算两幅图的相似性
    '''

    def Img_similarity(self, mat):
        list = []
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                list.append([])
                list[-1] = (i, j, 1 - mat[i][j])
        km = munkres_sparse.munkres(list)
        sum = 0
        for iterm in km:
            i, j = iterm
            sum = sum + mat[i][j]
        if len(km) == 0:
            return 0.0
        similarity = sum / len(km)
        return similarity
    '''
    @function:dct距离,利用dct系数中相同个数
    '''

    def dct_dis(self, d1, d2):
        count = 0
        length = len(d1)
        for i in range(length):
            if d1[i] != d2[i]:
                count = count + 1
        return count / length  # 相似性为不同元素的比例
    '''
    @function:位置距离,二进制异或运算，不同为1计算1的个数
    '''

    def locate_dis(self, a, b):
        count = 0
        for n in range(8):
            if a[n] != b[n]:
                count = count + 1
        return count / 8

    '''
    @function:两个元素的位置距离 called many times
    '''

    def dis_location(self, f1, f2):
        ratio = self.locate_dis(f1[3], f2[3])
        return ratio

    '''
    @function:两个元素视觉距离
    '''
    '''
    [ 1, u'D:/web/wamp/www/white/white_foreign/americanexpress/506tmp.jpeg', 
       [ u'8140a1408150855085502550a512a402a402b4528c9f1c9fb69bf68376837683', 
          [  [   [1, 8, 117, 12], [56, 13], 49.0, 76.93068210371783, 0.23347102124769356, 
               4.8450984097341925, 0.9797060176239845, 0.84955188258642, 
               [0.004270272521263887, 1.7375440332876605e-05, 8.409505124229687e-11, 
               9.608595888288582e-11, 8.636956527926735e-21, 4.0039950073194236e-13, 
              -7.028340855752252e-23] 
             ],
          ] 
        ], 
       u'00110101'
    ]
    '''

    def dis_visual(self, f1, f2):
        if f1[0] == f2[0]:
            if f1[0] == 1 or f1[0] == 4:
                dis_dct = self.dct_dis(f1[2][0], f2[2][0])
                dis_tex = self.textural_dis(f1[2][1], f2[2][1])
                if dis_tex == 0.0:
                    element = dis_dct
                else:
                    element = 0.5 * dis_dct + 0.5 * dis_tex
            else:
                element = self.dct_dis(f1[2], f2[2])
        else:
            element = self.dct_dis(f1[2][0], f2[2][0])
        # print "element",element
        return element

    def emdcalculate(self, gray_url):
        update_num = 0
        find_flags = 0
        location_value = 0.15
        visual_value = 0.2
        features1 = self.mongo_operate.get_web_view(gray_url, 'gray')
        if features1 is False or features1 == []:
            return 0
        if len(features1) > 50:
            features1 = features1[:50]
        weight1 = [1 / len(features1) for i in range(len(features1))]
        for protect_url in self.protected_title_dict.keys():
            features2 = self.mongo_operate.get_web_view(
                protect_url, 'protected')
            if not features2:
                continue

            if len(features2) > 50:
                features2 = features2[:50]
            # features1中每个元素的权重
            weight2 = [1 / len(features2) for i in range(len(features2))]
            emd_goal_location = emd(
                (features1, weight1), (features2, weight2), self.dis_location)
            if math.isnan(emd_goal_location):
                continue
            if emd_goal_location < location_value:
                find_flags = 1
                self.mysql_handle.undate_gray_list_check_result(
                    gray_url, 'view', source_url=protect_url)
                self.mysql_handle.undate_task_result_check_result(
                    self.task_id, self.task_start_time, gray_url, 'view_location')

            emd_goal_visual = emd(
                (features1, weight1), (features2, weight2), self.dis_visual)
            if math.isnan(emd_goal_visual):
                continue
            if emd_goal_visual < visual_value:
                find_flags = 1
                self.mysql_handle.undate_gray_list_check_result(
                    gray_url, 'view', source_url=protect_url)
                self.mysql_handle.undate_task_result_check_result(
                    self.task_id, self.task_start_time, gray_url, 'view_visual')

        for counterfeit_url in self.counterfeit_title_dict.keys():
            features2 = self.mongo_operate.get_web_view(
                counterfeit_url, 'counterfeit')
            if not features2:
                continue
            if len(features2) > 50:
                features2 = features2[:50]
            # features1中每个元素的权重
            weight2 = [1 / len(features2) for i in range(len(features2))]
            emd_goal_location = emd(
                (features1, weight1), (features2, weight2), self.dis_location)
            if math.isnan(emd_goal_location):
                continue
            if emd_goal_location < location_value:
                find_flags = 1
                self.mysql_handle.undate_gray_list_check_result(
                    gray_url, 'view', counterfeit_url=counterfeit_url)
                self.mysql_handle.undate_task_result_check_result(
                    self.task_id, self.task_start_time, gray_url, 'view_location')

            emd_goal_visual = emd(
                (features1, weight1), (features2, weight2), self.dis_visual)
            if math.isnan(emd_goal_visual):
                continue
            if emd_goal_visual < visual_value:
                find_flags = 1
                self.mysql_handle.undate_gray_list_check_result(
                    gray_url, 'view', counterfeit_url=counterfeit_url)
                self.mysql_handle.undate_task_result_check_result(
                    self.task_id, self.task_start_time, gray_url, 'view_visual')
        if update_num >= 5:
            #update_running_state(view_check_num, view_find_num)
            pass
        return find_flags


if __name__ == "__main__":
    e = ViewEmd('', '', '')
    e.emdcalculate('')
