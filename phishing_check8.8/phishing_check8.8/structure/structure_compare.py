# encoding:utf8

'''
对网页dom树进行结构比对，判断相似性
author：邹新一
time：2015.1.12
'''

from __future__ import division
#import traceback


class StructureCompare():

    def __init__(self, num_compare_k=0.03, num_compare_b=0.05,
                 area_compare_k=0.03, area_compare_b=0.001,
                 ):
        self.num_compare_k = num_compare_k  # 结点数量比对求阈值，反比例函数的 k
        self.num_compare_b = num_compare_b  # 结点数量比对求阈值，反比例函数的 b
        self.num_compare_rate = 0.2  # 结点数量比对，遍历结点占总结点数的最小比率
        self.area_compare_k = area_compare_k  # 结点面积比对求阈值，反比例函数的 k
        self.area_compare_b = area_compare_b  # 结点面积比对求阈值，反比例函数的 b
        self.area_compare_rate = 0.2  # 结点面积比对，遍历结点占总结点数的最小比率

        self.main_block_list = []  # 储存分块后主网页的结点
        self.mirror_block_list = []  # 储存分块后目标网页的结点
        self.similar_node_list = []  # 主网页和目标网页间相似结点列表
        self.main_block_len = 0  # 主网页结点数量
        self.mirror_block_len = 0  # 目标网页结点数量
        self.main_block_bottom = 0  # 主网页最底部结点编号
        self.mirror_block_bottom = 0  # 目标网页最底部结点编号
        self.traversal_node_num = 0  # 当为递增遍历mirror结点列表时，记录遍历的结点个数
        self.traversal_node_area = 0  # 当为递增遍历mirror结点列表时，记录遍历的结点面积
        self.similar_node_area = 0  # 相似结点中目标网页的的结点面积
        self.all_node_area = 0  # 目标网页的结点总面积

    def once_compare(self, main_block_list, mirror_block_list):
        '''主函数'''
        self.main_block_list = main_block_list
        self.mirror_block_list = mirror_block_list
        self.similar_node_list = []
        self.traversal_node_num = 0
        self.traversal_node_area = 0
        self.similar_node_area = 0
        self.all_node_area = 0
        for mirror_block in self.mirror_block_list:
            self.all_node_area += int(mirror_block[3]) * int(mirror_block[4])
        self.main_block_len = len(self.main_block_list)
        self.mirror_block_len = len(self.mirror_block_list)

        '''添加比对函数'''
        self.find_bottom_node()
        self.similar_node_select()
        compare_result = self.similar_node_compare()
        return compare_result
        #compare_result = self.begin_end_compare()

    def similar_node_compare(self):
        '''根据找到的相似结点，判断两个网页是否结构相似,用反比例函数确定比对阈值'''
        similar_node_num = len(self.similar_node_list)
        traversal_div_all_num = self.traversal_node_num / self.mirror_block_len
        similar_div_traversal_num = similar_node_num / self.traversal_node_num
        try:
            traversal_div_all_area = self.traversal_node_area / \
                self.all_node_area
        except ZeroDivisionError:
            return 0
        similar_div_traversal_area = self.similar_node_area / \
            self.traversal_node_area
        if traversal_div_all_num < self.num_compare_rate or \
                traversal_div_all_area < self.area_compare_rate:
            return 0
        num_compare_value = self.num_compare_k / \
            traversal_div_all_num + self.num_compare_b
        num_compare_result = similar_div_traversal_num - num_compare_value
        area_compare_value = self.area_compare_k / \
            traversal_div_all_area + self.area_compare_b
        area_compare_result = similar_div_traversal_area - area_compare_value
        result = num_compare_result + area_compare_result
        if result >= 0:
            return 1
        else:
            return 0

    def similar_node_judge(self, first_node, second_node, mistake=10):
        '''比较两个结点高度和宽度是否相似，相似则加入相似结点列表中，后序会根据位移再筛选'''
        if abs(int(first_node[3]) - int(second_node[3])) <= mistake \
                and abs(int(first_node[4]) - int(second_node[4])) <= mistake:
            return 1
        else:
            return 0

    def similar_shift_select(self, top_shift_mistake=5, left_shift_mistake=5, top_mistake=5, bottom_mistake=5):
        '''选择相似结点列表中，具有相同位移关系最多的那些结点
        考虑顶部、左、底部位移，即当网页整体位移时，同样判断成功。
        当在网页中间插入一些内容后，会导致下面结点的顶部位移相差较大，故考虑用底部位移判断。
        模拟从上往下、从下往上找相似结点'''
        top_shift_dic = {}  # ｛顶部位移数值 ：具有该位移的结点个数｝
        left_shift_dic = {}
        max_top_shift = 1  # 最多的顶部位移相同的结点个数
        max_left_shift = 1
        certain_top_shift = 0  # 最多结点相同的顶部位移
        certain_left_shift = 0
        for similar_node in self.similar_node_list:
            '''找到在相似结点列表中，出现最多的左位移和顶部位移'''
            top_shift = similar_node[2]
            left_shift = similar_node[3]
            #bottom_shift = similar_node[4]
            if top_shift in top_shift_dic:  # 将该顶部位移加入字典，若已有则加1
                top_shift_dic[top_shift] = top_shift_dic[top_shift] + 1
                if top_shift_dic[top_shift] > max_top_shift:
                    max_top_shift = top_shift_dic[top_shift]
                    certain_top_shift = top_shift
            else:
                top_shift_dic[top_shift] = 1

            if left_shift in left_shift_dic:  # 将该左位移加入字典，若已有则加1
                left_shift_dic[left_shift] = left_shift_dic[left_shift] + 1
                if left_shift_dic[left_shift] > max_left_shift:
                    max_left_shift = left_shift_dic[left_shift]
                    certain_left_shift = left_shift
            else:
                left_shift_dic[left_shift] = 1

        sure_similar_node_list = []  # 储存最终确定的相似结点列表，即具有相同位移最多的结点
        for similar_node in self.similar_node_list:
            '''根据出现最多的左位移、顶部位移和底部位移，筛选相似结点列表'''
            if ((abs(similar_node[2] - certain_top_shift) <= top_shift_mistake)
                    or (abs(similar_node[4] - similar_node[5]) <= top_mistake)
                    or (abs(similar_node[6] - similar_node[7]) <= bottom_mistake)) \
                    and abs(similar_node[3] - certain_left_shift) <= left_shift_mistake:
                sure_similar_node_list.append(similar_node[:2])
                #mirror_node = self.mirror_block_list[similar_node[0]]
                #self.similar_node_area += int(mirror_node[3]) * int(mirror_node[4])
        self.similar_node_list = sure_similar_node_list

    def similar_node_select(self):
        '''相似结点选择，递进遍历方式，从main_block_list和mirror_block_list中找出相似结点
            当连续匹配失败时，需匹配位置递增'''
        mirror_block_site = 0  # 遍历mirror_block_list中结点位置
        main_block_site = 0  # 每次遍历main_block_list中结点位置
        # 记录当前已经匹配的main_block_list中结点位置，在这之后继续遍历main_block_list
        record_site = 0
        failure_num = 0  # 连续失败次数
        mirror_bottom_node = self.mirror_block_list[self.mirror_block_bottom]
        main_bottom_node = self.main_block_list[self.main_block_bottom]
        mirror_bottom = int(mirror_bottom_node[1]) + int(mirror_bottom_node[3])
        main_bottom = int(main_bottom_node[1]) + int(main_bottom_node[3])
        while mirror_block_site < self.mirror_block_len:
            once_compare_result = 0
            mirror_node = self.mirror_block_list[mirror_block_site]
            self.traversal_node_num += 1
            self.traversal_node_area += int(
                mirror_node[3]) * int(mirror_node[4])
            while main_block_site != self.main_block_len:
                main_node = self.main_block_list[main_block_site]
                # 顶坐标之差，用于判断整体偏移
                top_shift = int(mirror_node[1]) - int(main_node[1])
                left_shift = int(mirror_node[2]) - int(main_node[2])  # 左坐标之差
                mirror_bottom_shift = mirror_bottom - \
                    int(mirror_node[1]) + \
                    int(mirror_node[3])  # 相对mirror分块结果底部的偏移
                main_bottom_shift = main_bottom - \
                    int(main_node[1]) + int(main_node[3])
                once_compare_result = self.similar_node_judge(
                    mirror_node, main_node)
                # 匹配成功，记录当前main_block_site中的位置，将连续失败次数置0
                if once_compare_result == 1:
                    self.similar_node_list.append([mirror_block_site, main_block_site, top_shift, left_shift,
                                                   int(mirror_node[1]), int(main_node[1]), mirror_bottom_shift, main_bottom_shift])
                    main_block_site += 1
                    record_site = main_block_site
                    failure_num = 0
                    break
                else:
                    main_block_site += 1
            # 若失败，则返回main_block_list记录位置，mirror_block_site加上递增值
            if once_compare_result == 0:
                main_block_site = record_site
                # 以failure_num的平方递增
                mirror_block_site += (1 + failure_num ** 2)
                failure_num += 1
            # 若main_block_list已匹配完则退出
            elif main_block_site == self.main_block_len:
                break
            else:
                mirror_block_site += 1
        self.similar_shift_select()

    def find_bottom_node(self):
        '''找到主站、镜像网站分块结果中在位置上最底部结点编号'''
        main_block_len = self.main_block_len
        mirror_block_len = self.mirror_block_len
        main_bottom = 0
        mirror_bottom = 0
        while main_block_len:
            main_block = self.main_block_list[main_block_len - 1]
            bottom = int(main_block[1]) + int(main_block[3])
            if bottom >= main_bottom:
                main_bottom = bottom
                self.main_block_bottom = main_block_len - 1
            main_block_len -= 1

        while mirror_block_len:
            mirror_block = self.mirror_block_list[mirror_block_len - 1]
            bottom = int(mirror_block[1]) + int(mirror_block[3])
            if bottom >= mirror_bottom:
                mirror_bottom = bottom
                self.mirror_block_bottom = mirror_block_len - 1
            mirror_block_len -= 1

    def begin_end_compare(self, judge_factor=3):
        '''对分块结果的头部和尾部进行比较，判断相似的阈值为judge_factor，默认为3
            尾部为视觉上的微博，即分块的HTML中最底部的结点'''
        begin_site = 0
        whole_top_shift = 0
        whole_left_shift = 0
        win_num = 0
        #compare_win_list = []

        while 1:  # 从头匹配
            main_block = self.main_block_list[begin_site]
            mirror_block = self.mirror_block_list[begin_site]
            main_block_top = int(main_block[1])
            main_block_left = int(main_block[2])
            mirror_block_top = int(mirror_block[1])
            mirror_block_left = int(mirror_block[2])
            if main_block[3] == mirror_block[3] and main_block[4] == mirror_block[4] \
                    and (whole_top_shift == main_block_top - mirror_block_top or whole_top_shift == 0) \
                    and (whole_left_shift == main_block_left - mirror_block_left or whole_left_shift == 0):
                if whole_top_shift == 0:
                    whole_top_shift = main_block_top - mirror_block_top
                if whole_left_shift == 0:
                    whole_left_shift = main_block_left - mirror_block_left
                win_num += 1
                #compare_win_list.append([main_block, mirror_block])
                begin_site += 1
                if begin_site == self.main_block_len or begin_site == self.mirror_block_len:
                    break
            else:
                break

        main_block_bottom = self.main_block_bottom
        mirror_block_bottom = self.mirror_block_bottom
        whole_top_shift = 0
        whole_left_shift = 0
        while 1:  # 从尾匹配
            if begin_site == main_block_bottom + 1 or begin_site == mirror_block_bottom + 1:
                break
            main_block = self.main_block_list[main_block_bottom]
            mirror_block = self.mirror_block_list[mirror_block_bottom]
            main_block_top = int(main_block[1])
            main_block_left = int(main_block[2])
            mirror_block_top = int(mirror_block[1])
            mirror_block_left = int(mirror_block[2])
            if main_block[3] == mirror_block[3] and main_block[4] == mirror_block[4] \
                    and (whole_top_shift == main_block_top - mirror_block_top or whole_top_shift == 0) \
                    and (whole_left_shift == main_block_left - mirror_block_left or whole_left_shift == 0):
                if whole_top_shift == 0:
                    whole_top_shift = main_block_top - mirror_block_top
                if whole_left_shift == 0:
                    whole_left_shift = main_block_left - mirror_block_left
                win_num += 1
                #compare_win_list.append([main_block, mirror_block])
                main_block_bottom -= 1
                mirror_block_bottom -= 1
            else:
                break

        if win_num >= judge_factor:
            return 1
        else:
            return 0

if __name__ == '__main__':
    '''
    #汇总，检测误报率
    start = 1
    num = 610
    all = 610
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = str(i+start) + '.txt'
        #print goal1
        for j in range(all):
            if start <= j+1 <= i+start:
                continue
            goal2 = str(j+1) + '.txt'
            #print goal2
            structure_compare.structure_compare(goal1,goal2)
    structure_compare.end_save()
    print 'luntan over!'
    '''
    # 论坛，检测误报率
    start = 42
    num = 47
    all = 610
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = str(i + start) + '.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = str(j + 1) + '.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'luntan over!'

    # 新闻，检测误报率
    start = 89
    num = 20
    all = 610
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = str(i + start) + '.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = str(j + 1) + '.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'xinen over!'

    # 已知镜像网站，误报率
    start = 1
    num = 610
    all = 610
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = str(i + start) + '.txt'
        structure_compare.structure_compare(goal1, 'mirror_1_0.txt')
        structure_compare.structure_compare(goal1, 'mirror_2_0.txt')
    structure_compare.end_save()
    print 'mirror lou bao over!'

    # 观海论坛各版块，测试漏报率
    start = 1
    num = 39
    all = 39
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = 'ghtt_' + str(i + start) + '.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = 'ghtt_' + str(j + 1) + '.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'ghtt_lt over!'

    # 观海贴吧帖子
    start = 1
    num = 90
    all = 90
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = 'ghtt_tb_' + str(i + start) + '_vtree.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = 'ghtt_tb_' + str(j + 1) + '_vtree.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'ghtt_tb over!'

    # 已知镜像网站，漏报率
    start = 1
    num = 6
    all = 6
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = 'mirror_1_' + str(i + start) + '.txt'
        structure_compare.structure_compare(goal1, 'mirror_1_0.txt')
    structure_compare.structure_compare('mirror_2_1.txt', 'mirror_2_0.txt')
    structure_compare.end_save()
    print 'mirror 1 over!'

    # 搜狐新闻各版块
    start = 1
    num = 7
    all = 7
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = 'sohu_new_' + str(i + start) + '.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = 'sohu_new_' + str(j + 1) + '.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'sohu_news over!'

    # 新浪新闻各版块
    start = 1
    num = 33
    all = 33
    structure_compare = Structure_Compare()
    for i in range(num):
        goal1 = 'sina_new_1_' + str(i + start) + '.txt'
        # print goal1
        for j in range(all):
            if start <= j + 1 <= i + start:
                continue
            goal2 = 'sina_new_1_' + str(j + 1) + '.txt'
            # print goal2
            structure_compare.structure_compare(goal1, goal2)
            # print
            # '--------------------------------------------------------------------------------'
    structure_compare.end_save()
    print 'sohu_news over!'
