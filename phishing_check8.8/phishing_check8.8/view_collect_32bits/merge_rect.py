# -*- encoding: utf-8 -*- #注意此处为小写
'''
Created on 2015年1月29日
@author: momo
@function:整幅图像中查找进行logo定位
'''
from __future__ import division
import cv2.cv as cv
import cv2
from PIL import Image  # ~~~~~~~
import numpy as np
import math
import matplotlib


'''
 @attention: 合并边界矩形
'''


def check_merge(pathfile):
    node_list = Canny(pathfile)
    rect_list = rect_set(node_list, pathfile)  # 得到边界矩形集合
    img = cv2.imread(pathfile)
    for item in rect_list:
        pt1 = (item['rect'][0], item['rect'][1])
        pt2 = (item['rect'][2], item['rect'][3])
        height = item['rect'][3] - item['rect'][1]
        width = item['rect'][2] - item['rect'][0]
        # print "pt1,height,width",pt1,height,width
# if height/width>0.15 and height/width< 1.5 and height*width>25*25 and
# height*width< img.shape[0]*img.shape[1]*2/3:  #计算轮廓内连通区域的面积 and
# bound_rect[2]*bound_rect[3]<
        # 参数含义(绘制目标图像，起始点坐标，长宽值，绘制线颜色，线粗细)
        cv2.rectangle(img, pt1, pt2, cv.CV_RGB(255, 0, 0), 3)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
    # print "rect_list",rect_list
    raw_input("rect_list")
    return rect_list


# rect_set()
# check_merge('D:/web/wamp/www/category/92.223.191.8-images-task/pic/sig-eng.jpeg')
# rect_set(Canny('D:/cut/BBVA Bancomer-fondo.jpg'))
# check_merge('D:/cut/10086-loginbg.jpg')

# print Canny('D:/cut/thumb_1396407230_41155500.jpg') #与背景融合，不能分隔开
# print Canny('D:/cut/dhico.png') #与背景融合，不能分隔开
# print Canny('D:/cut/tengxun-foot_bg.jpg') #膨胀、腐蚀参数设置为6效果不好
# print Canny('D:/cut/pinghengche-tmp1396252045_s.jpg') #膨胀、腐蚀参数设置为6效果不好
# print Canny('D:/cut/pingan-logo.jpg') #嵌入到背景中，不能检测出来logo
# print Canny('D:/cut/america -irs.PNG') #膨胀、腐蚀参数为6时效果不好
# print Canny('D:/cut/index_b_bg01.jpg') #logo嵌入到背景图中，不能检测出
# print Canny('D:/cut/trades.png') #最左部的logo检测出来，但是别的图标相距太近，划分到一个矩形框中
# print Canny('D:/cut/sparkasse-wpc1ce0755_06.png') #最上部的边框覆盖了logo区域
# print Canny('D:/cut/outlook-o.PNG') #最大矩形框，覆盖了logo矩形框，设定具体规则。
# print Canny('D:/cut/ICBC-logo_icbc.jpg') # logo被分隔开
# print Canny('D:/cut/google-drive-icons.png') # logo被分隔开与下层文字分隔开
# print Canny('D:/cut/google-bgimage.jpg') # logo被分隔开
# print Canny('D:/cut/bbqn2_201406124.jpg') # 标记嵌入在背景中，小图太多，无法分离
# print Canny('D:/cut/apple-login1.png') # My/apple ID(logo)被分隔开
# print Canny('D:/cut/apple-2.png') #logo貌似能检测出来，但是上部的导航栏也组成了子图，可用于黑名单
# print Canny('D:/cut/AOL-y.PNG')#logo嵌入在背景图中，且左上角的logo太小，不能检测出来。登录框中的logo能检测，但是不确定能否分离出来！
# print Canny('D:/cut/1086-1-logo.jpg') #不知何种原因，腐蚀、膨胀系数越大，越检测不出来图像。
# print Canny('D:/cut/A01_02.jpg') #由于logo是嵌入背景中的白色图像，当腐蚀、膨胀系数大于3时，logo不能检测出来
