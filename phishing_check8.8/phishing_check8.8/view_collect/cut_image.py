# -*- encoding: utf-8 -*- #注意此处为小写
'''
Function :Logo 比对，边缘检测划分子图;子图特征提取;特征组合方法;使用距离分布直方图
Created on 2014年12月11日
@author: momo
'''
import cv2.cv as cv
import cv2
from PIL import Image  # ~~~~~~~
import numpy as np
import math


# canny 边缘检测
def Canny(imgname):
    img = cv2.imread(imgname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 读取灰度图
    image = cv2.erode(gray, None, iterations=4)  # 图像的4次腐蚀
    image = cv2.dilate(image, None, iterations=4)  # 图像的4次膨胀。开运算
    # canny边界检测, 30和150是检测阈值，opencv必须手工输入阈值，如需自动匹配阈值，请参考cvCanny介绍
    PCannyImg = cv2.Canny(image, 50, 150)
    # cv2.findContours()函数来查找检测物体的轮廓
    # 提取边界，参数 cv2.RETR_EXTERNAL为提取最外层边界
    # 返回两个值，一个是轮廓本身，还有一个是每条轮廓对应的属性
    contour, hierarchy = cv2.findContours(
        PCannyImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mylist = []
    i = 0
    for iterm in contour:
        bound_rect = cv2.boundingRect(iterm)  # 边界的矩形属性
        # print "bound_rect",bound_rect
# if bound_rect[2]*bound_rect[3]>500 and bound_rect[2]*bound_rect[3]<
# img.shape[0]*img.shape[1]*2/3:  #计算轮廓内连通区域的面积 and
# bound_rect[2]*bound_rect[3]<
        # 计算轮廓内连通区域的面积 and bound_rect[2]*bound_rect[3]<
        if bound_rect[2] * bound_rect[3] > 200 and bound_rect[2] * bound_rect[3] < img.shape[0] * img.shape[1] * 2 / 3:
            pt1 = (bound_rect[0], bound_rect[1])
            pt2 = (
                bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
#             print "pt1,pt2",pt2
#             raw_input("pt2")
# cv2.rectangle(img,pt1,pt2,cv.CV_RGB(255,0,0),2)       #参数含义(绘制目标图像，起始点坐标，长宽值，绘制线颜色，线粗细)
#             cv2.imshow('Contours', img)
#             cv2.waitKey(0)
            mylist.append([])
            mylist[-1] = [(pt1 + pt2), bound_rect, iterm]
            i = i + 1
    return mylist


def pilcut(imgname, listname):  # 切割子图
    # print "pilcut imgname is -------------",imgname
    im = Image.open(imgname)
    i = 0
    for item in listname:
        # print "item is",item[0],item[1]
        xim = im.crop(item[0])  # 根据元组坐标信息切割子图,速度未知
        # print "xim is",xim
        xim.save('D:/img/image' + str(i) + '.jpg')  # ~~~~here
        i = i + 1


'''
@new function：计算与四个顶点的夹角，同时返回区域位置信息
'''


def vision_center(Img, top, left, height, width):
    # print "Img",Img
    try:
        img = cv2.imread(Img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 读取灰度图
    except:
        return 0
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # 获得图像的二值矩阵
    (Center_x, Center_y) = img_center(binary, 0, 0)  # 整幅图的重心
    S_x = Center_x + int(left)
    S_y = Center_y + int(top)
    angle1 = img_angle(S_x, S_y)  # 子图重心相对整幅图像左上顶点的夹角
    angle2 = img_angle(S_y, width - S_x)  # 相对于右上顶点的夹角
    angle3 = img_angle(width - S_x, height - S_y)  # 想对于右下点顶的夹角
    angle4 = img_angle(height - S_y, S_x)  # 相对于左下顶点的夹角
    # 返回<00011110>这种位置描述
    return Locate_binary((angle1, angle2, angle3, angle4))


'''
@function:判断图像从该夹角属于哪个区域
'''


def Locate_binary(angle):
    locate = ''
    for item in angle:
        value = item / 22.5
        if value < 1:
            locate = locate + '00'
        elif value < 2:
            locate = locate + '01'
        elif value < 3:
            locate = locate + '10'
        else:
            locate = locate + '11'
    return locate
# print Locate_binary((15,25,57,80))


'''
EMD中对logo及增信图标的纹理特征获取，对这里进行修改得到！！！
'''


# 按照论文五，获得子图像的视觉特征，先按照EMD计算图像之间的距离，首先参考论文中每种属性相似性的度量方法，再按照EMD原理，实现最终的距离度量
def get_features(Img):

    img = cv2.imread(Img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 读取灰度图
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    (Center_x, Center_y) = img_center(binary, 0, 0)  # 整幅图的重心
    leng_diagonal = math.sqrt(
        gray.shape[0] * gray.shape[0] + gray.shape[1] * gray.shape[1])
    # print "Center_x",Center_x
    List = Canny(Img)  # 返回轮廓信息，(轮廓矩形框信息，边界点集合)
#     List = check_merge(Img)
#     for i in List:
#         print "i",i
#     raw_input("i")
    feature = []
    # print "Img",Img
    # print "LIst from canny is",List
    for iterm in List:

        '''
        [
        (1, 33, 386, 34), (1, 33, 385, 1), array([  [  [  1,  33]  ],

       [ [385,  33] ]   ])
        ]
        '''
        cv2.rectangle(
            gray, iterm[0][:2], iterm[0][2:], cv.CV_RGB(255, 0, 0), 2)
        # print "iterm[]",iterm[1],iterm[0][1],iterm[0][3]
        # 截取子图像矩阵 #~~here
        SubImg = gray[iterm[0][1]:iterm[0][3], iterm[0][0]:iterm[0][2]]
        SubBin = binary[
            iterm[0][1]:iterm[0][3], iterm[0][0]:iterm[0][2]]  # 截取二值子图像矩阵
        Sub_x, Sub_y = img_center(SubBin, iterm[0][0], iterm[0][1])  # 子图像重心坐标
        # print "Sub_x,Sub_y is",Sub_x,Sub_y
        Distance = math.sqrt((Sub_x - Center_x) * (Sub_x - Center_x) +
                             (Sub_y - Center_y) * (Sub_y - Center_y))  # 分块重心与整幅图像重心间的距离
        # print "Distance is",Distance,Distance/leng_diagonal
        # 与重心间距离相对对角线的比例
        angle = img_angle(Sub_y, Sub_x)  # 子图重心相对整幅图像顶点的夹角
        # print "tan is",angle
        Sub_entory = Entory(SubImg)  # 计算分块子图的信息熵
        Sub_eccentricity = img_eccentricity(SubBin)  # 计算分块的偏心率
       # print "iterm[2] is",iterm
        Sub_circularity = Subimg_circularity(Sub_x, Sub_y, iterm[2])  # 分块的圆形性
        Sub_hu = img_hu(SubBin)  # 分块的Hu矩
        feature.append([])
        feature[-1] = (iterm[1], (Sub_x, Sub_y), Distance, angle, Distance /
                       leng_diagonal, Sub_entory, Sub_eccentricity, Sub_circularity, Sub_hu)
    return feature


def img_angle(cx, cy):
    # print "cx,cy in angle is",cx,cy
    angle = math.atan2(cy, cx) * 180 / math.pi
    # print "angle is",angle
    return angle


def img_center(binary, point_x, point_y):  # 计算图像的重心
    # 找到分块的重心
    M = cv2.moments(binary)
    # print "m[10],m[01],m[00]",M['m10'],M['m00'],M['m01']
    if M['m00'] != 0.0:
        cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
    else:
        cx, cy = (0, 0)
    # print "cx,cy",point_x+cx,point_y+cy
    return point_x + cx, point_y + cy


def img_hu(binary):  # Hu不变矩
    M = cv2.moments(binary)
    Hu = cv2.HuMoments(M)
    # print "Sub Hu is",Hu
    Hu_list = []
    for item in Hu:

        Hu_list.append([])
        Hu_list[-1] = item[0]
    return Hu_list


def img_eccentricity(binary):  # 计算图像的偏心率
    # 找到分块的重心
    M = cv2.moments(binary)
    if (M['m20'] + M['m02']) * (M['m20'] + M['m02']) != 0:
        e = ((M['m20'] - M['m02']) * (M['m20'] - M['m02']) + 4 * M['m11'] *
             M['m11']) / ((M['m20'] + M['m02']) * (M['m20'] + M['m02']))  # 论文5中公式错误
    else:
        e = 0
    # print "sub 图像偏心率是",e
    return e
'''
@function:计算子图的圆形性好像与整幅大图的圆形性不太一致，故此处修改为Subimg_circularity
'''


def Subimg_circularity(center_x, center_y, contour):  # ~~here
    Sub_dis = 0
    Sum = 0
    for iterm in contour:
        #         print "iterm in contour is",iterm
        #         for i in iterm:
        #             print "i in iterm is",i
        #
        # print "iterm is",len(contour)
        # print "iterm 1 is",iterm[0:1,0]
        # print "iterm 2 is",iterm[0:1,1]
        # print "center x,y is",center_x,center_y
        S_distance = (center_x - iterm[0:1, 0]) * (center_x - iterm[0:1, 0]) + (
            center_y - iterm[0:1, 1]) * (center_y - iterm[0:1, 1])
#         print "S_distance is",S_distance
#         raw_input("iterm cir")
        distance = math.sqrt(S_distance)
        Sub_dis = Sub_dis + distance
        Sum = Sum + S_distance
    if len(contour) == 0:
        return 0
    ave_dis = Sub_dis / len(contour)
    SD = math.sqrt(Sum / len(contour))
    if SD == 0:
        return 0
    circularity = ave_dis / SD
    # print "img_circularity",circularity
    return circularity


def Entory(gray):  # 实现灰度图像的信息熵,是否需要计算二值化的信息熵？？？
    #     print "Entory width,heigth",gray.shape
    mat = np.zeros(256, np.float16)
    for i in range(gray.shape[0]):  # 统计每个像素的个数
        for j in range(gray.shape[1]):
            num = gray[i][j]
            mat[num] = mat[num] + 1
        j = j + 1
    i = i + 1
    for i in range(255):
        #         print mat[i],gray.size
        mat[i] = mat[i] / (gray.size)
    H1 = 0
    for i in range(255):
        if mat[i] != 0:
            H1 = H1 + (-mat[i] * math.log(mat[i]) / math.log(2))
    # print "Sub_entory is",H1
    return H1


'''
@function:获取图像的dct信息
'''


# get_hash()
# Img_similarity()
# vision_feature('D:/web_source/bpbar/pic/A01_05.gif')
# Similarity(get_features('D:/img/shunhe.jpg'),get_features('D:/img/juli.jpg'))
# print Img_similarity(Similarity(get_features('D:/img/b.jpg'),get_features('D:/img/a.jpg')))
# img_circularity('D:/img/image1.jpg')
# img_hu('D:/img/image1.jpg')
# img_eccentricity('D:/img/image1.jpg')
# Entory('D:/img/image1.jpg') #求图像的信息熵
# block_entory('D:/img/image1.jpg')
# img_center('D:/img/image1.jpg') #求图像的重心 OK
# print "pwd:",os.getcwd()
# pilcut('D:/cut/ICBC-logo_icbc.jpg',Canny('D:/cut/ICBC-logo_icbc.jpg'))
# pilcut('D:/img/juli.jpg',Canny('D:/img/juli.jpg'))
# pilcut('D:/img/xinsheng.jpg',Canny('D:/img/xinsheng.jpg')) #对图像先腐蚀后膨胀消除笔画间孔隙。OK
# pilcut('D:/img/juli.jpg',OpenClose('D:/img/juli.jpg')) #对图像进行开闭运算，不采用
