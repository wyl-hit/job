#!/usr/bin/env python
#-*- encoding: utf-8 -*-
'''
Created on 2014年6月21日

@author: momo
'''

from __future__ import division
import sys
from cut_image import vision_center, get_features
from PIL import Image
import os
import img_hash
from svmutil import *


class ViewPageBlock():

    def __init__(self, path, vtree, current_path, url, mongo_operate, web_type):
        # self.html_size = []
        # self.select_node = []
        self.vtree = []         # 从mongo中获取的视觉块信息
        self.path = path        # 本地存储的网页的绝对路径
        self.img_feature = []   # 存储一个网页的所有分割的图像特征
        self.p_label = []       # 用于 svm 分类，存储所有图像的类型
        self.vtree = vtree
        self.current_path = current_path
        self.url = url
        self.mongo_operate = mongo_operate
        self.web_type = web_type
        self.select()

    def select(self, size=0):
        '''
        获取网页边界大小
        '''
        web_border = self.mongo_operate.get_web_border(self.url, self.web_type)
        self.width = web_border[0]
        self.height = web_border[1]
        self.size = web_border[0] * web_border[1]

    def cut_img(self, node, num):
        '''
        @function:从主图中切取获得子图
        '''
        '''
        node: [0, 0, 0, 1021, 787]
        '''
        img_name = 'webpage.jpeg'
        img_path = self.path + '/' + img_name
        if not os.path.isfile(img_path):
            sys.stderr.write(' %simg_path not exist' % (img_path))
            return None
        im = Image.open(img_path)
        if int(node[3]) == 0 or int(node[4]) == 0 or int(node[3]) * int(node[4]) >= self.height * self.width:
            return
        box = (node[2] + 7, node[1], node[4] + node[2] + 7, node[3] + node[1])
        xim = im.crop((box))
        pic_name = self.path + "/" + str(num) + 'tmp.jpeg'
        xim.save(pic_name)
        return pic_name
    '''
    @function:获得vips图片，使用射线扫描方法获得图像空间位置，及纹理信息
    '''

    def gather_vips_pic(self):
        vips_pic_list = self.select_subimg()
        #[0, 14, 31, 758, '/home/phishing_check/web_info/gray/.../32tmp.jpeg', 2]
        for pic in vips_pic_list:
            dis = pic[4]
            # print "pic in vips_pic_list is",pic
            try:
                if os.path.isfile(dis):
                    # vision_center 返回<00011110>这种图像位置描述
                    location = vision_center(
                        dis, pic[0], pic[1], self.height, self.width)
                else:
                    continue
            except:
                continue
            pic.append([])
            pic[-1] = location
            #[0, 14, 31, 758, 'spoonfulcafeandliving/32tmp.jpeg', 2,'00011110']
            pic.append([])
            img = Image.open(dis)
            dct = img_hash.phash(img)  # 获取图像的dct 量化值
            pic[-1] = str(dct)
            #[0, 14, 31, 758, 'spoonfulcafeandliving/32tmp.jpeg', 2,'00011110','sddddsaa...']
            if int(pic[5]) == 1:  # 如果图像类型为 1 ：logo ，切取子图，获取纹理特征
                # logo阈值来源legal_imginfo_logopic.xlsx
                if pic[1] / pic[2] > 0.09 and pic[1] / pic[2] < 1.12:
                    pic.append([])
                    # get_features 输入logo的图像路径，输出 logo子图的纹理特征
                    pic[-1] = get_features(dis)
                    # [0, 14, 31, 758, 'spoonfulcafeandliving/32tmp.jpeg', 2,'00011110','sddddsaa...',[]]
                else:
                    continue
            elif int(pic[5]) == 4:  # 如果图像类型为 4 ：增信图标 ，切取子图，获取纹理特征
                # 增信图标阈值来源legal_imginfo_zengxin.xlsx
                if pic[1] / pic[2] > 0.25 and pic[1] / pic[2] < 1.2:
                    pic.append([])
                    pic[-1] = get_features(dis)
                else:
                    continue
            else:
                pic.append([])

            self.img_feature.append([])
            self.img_feature[-1] = pic

    def select_subimg(self):
        '''
        @attention: 判断是否选中图片来对网页描述,并写入svm预测文件img.txt中

        '''
        path = self.path + '/vips_imgs.txt'
        file = open(path, 'w')
        List = []
        svm_img_list = []
        for node in self.vtree:
            # 如果图像的大小值<25*25，则跳过，该图像过小，不适和图像描述，筛选出大小合适的图像
            if node[3] * node[4] > 25 * 25:
                file.write('%d %d:%f %d:%f %d:%f %d:%f %d:%f'
                           % (0, 1, node[2] / self.width, 2, node[3] / node[4], 3, node[4] / self.width, 4, node[3] / self.width, 5, node[1] / self.height))
                pic_name = self.cut_img(node, node[0])
                if pic_name is None:
                    continue
                img_svm = node[1:5]
                img_svm.append([])
                img_svm[-1] = pic_name
                #[0, 14, 31, 758, 'spoonfulcafeandliving/32tmp.jpeg']
                List.append([])
                List[-1] = img_svm
                file.write('\n')
        file.close()

        y, x = svm_read_problem(
            self.current_path + '/imginfo_svm.txt')  # 训练的数据
        m = svm_train(y[:], x[:], '-c 2048 -g 0.5')  # 训练出来的参数，预测
       # print path
        y, x = svm_read_problem(self.path + '/vips_imgs.txt')
        if len(y) == 0:
            return svm_img_list
        p_label, p_acc, p_val = svm_predict(y[0:], x[0:], m)      # 获取到图像种类的预测值
        for num in range(len(List)):
            # print "num",num
            # print "List[num]",List[num]
            List[num].append([])
            List[num][-1] = int(p_label[num])
            svm_img_list.append([])
            svm_img_list[-1] = List[num]
        # svm_img_list 格式为 [0, 14, 31, 758, 'spoonfulcafeandliving/32tmp.jpeg',
        # 2]
        return svm_img_list

    def save_feature(self):
        feature_dict = {}
        feature_list = []
        tmps = []
        for pic in self.img_feature:
            # [2,'spoonfulcafeandliving/32tmp.jpeg','sddddsaa...','00011110',,[]]
            tmps = [pic[5], pic[4], pic[7], pic[6], pic[8]]
            feature_list.append([])
            feature_list[-1] = tmps

       # @function:将抽取到的视觉特征信息存入mongo中
        self.mongo_operate.add_web_view(self.url, self.web_type, feature_list)
