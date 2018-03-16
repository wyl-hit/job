# encoding:utf8
'''
    程序简介：
         首先删除所有外围结点，和面积为0的结点
         然后设定一个阈值，对面积大于阈值的结点，若包含其所有子结点（区域面积和文字均包含），则删除此结点；
             对面积小于阈值的结点，若包含其所有子结点，则删除其所有子结点。即使结点在两头向中间靠拢。
        接着对网页结构的某一模块中以列表的形式一行一行显示的结点进行合并，并删除网页中存在的滚动条
        选择筛选后的DOM树中非空且没有子结点的结点进行输出

    author: xinyi
'''


class SNode():

    def __init__(self, node_list, plan_text):
        self.selected_node_list = []
        self.current_node_list = node_list
        self.plan_text = plan_text
        self.node_sum = len(self.current_node_list)
        self.most_right_boundary = 0
        self.most_left_boundary = 0
        self.select_area = 70000
        self.min_area = 12000
        self.line_max_area = 30000  # 进行列表合并 combine_message_line
        self.line_combine_mistake = 5

    def delete_node(self, real_parents_site, real_current_site, order_type=0, combine_site=-1):
        '''在此结点的父结点中删除此结点，然后将此结点的子结点指向此结点的父结点，
           并在此结点的父结点的孩子列表中添加此结点的子结点，然后将此结点所在位置变为None
           real_parents_site ：待删除结点的父结点编号
           real_current_site ：待删除结点编号
           order_type：删除结点时的遍历类型，0：正序遍历，1：倒序遍历
           combine_site：合并时母结点的编号，在结点合并后删除已合并结点时使用'''
        if order_type == 0:  # 当为正序删除时，计算结点在列表为正序时的位置
            if real_current_site == 0:
                return None
            current_site = real_current_site
            parents_site = real_parents_site
        elif order_type == 1:  # 当为倒序删除时
            current_site = self.node_sum - real_current_site - 1
            parents_site = self.node_sum - real_parents_site - 1
        current_node = self.current_node_list[current_site]
        self.current_node_list[parents_site][8].remove(real_current_site)
        for cnode_num in current_node[8]:
            if order_type == 0:
                child_site = cnode_num  # 当为正序删除时，计算结点的孩子结点在列表此时的位置
            elif order_type == 1:  # 当为倒序删除时
                child_site = self.node_sum - cnode_num - 1
            if combine_site == -1:
                self.current_node_list[child_site][0] = current_node[0]
                self.current_node_list[parents_site][8].append(cnode_num)
            else:
                self.current_node_list[child_site][0] = combine_site
                # self.current_node_list[combine_site][8].append(cnode_num)
        # self.current_node_list[current_site][0] = -2
        # 将此结点的父结点编号变为-2，表明此结点以被删除
        self.current_node_list[current_site] = None

    def node_combine(self, combine_node_list, current_site):
        ''''将combine_node_list中的结点合并到current_site结点中'''
        current_node = self.current_node_list[current_site]
        top = current_node[2]
        left = current_node[3]
        bottom = current_node[2] + current_node[4]
        right = current_node[3] + current_node[5]
        new_plan_text = self.plan_text[
            current_node[6]:current_node[6] + current_node[7]]
        child_list = current_node[8]
        for node_site in combine_node_list:
            node = self.current_node_list[node_site]
            if node[2] < top:
                top = node[2]
            if node[3] < left:
                left = node[3]
            if node[2] + node[4] > bottom:
                bottom = node[2] + node[4]
            if node[3] + node[5] > right:
                right = node[3] + node[5]
            new_plan_text = new_plan_text + \
                self.plan_text[node[6]:node[6] + node[7]]
            child_list = child_list + node[8]
            self.delete_node(node[0], node_site, 0, current_site)
        current_node = [current_node[0], 'combine', top, left, bottom - top,
                        right - left, len(self.plan_text), len(new_plan_text), child_list]
        self.current_node_list[current_site] = current_node
        self.plan_text = self.plan_text + new_plan_text

    def delete_first_node(self):
        '''清空第一个结点，但保留其子结点列表'''
        first_node = self.current_node_list[0]
        self.most_left_boundary = first_node[3]
        self.most_right_boundary = first_node[3] + first_node[5]
        for temp in [1, 2, 3, 4, 5, 6, 7]:
            self.current_node_list[0][temp] = 0
        self.current_node_list[0][0] = -1

    def delete_whole_node(self, least_gap=3):
        '''从前往后删除面积小于最小面积阈值的结点、分割栏结点'''
        '''（弃用）从前往后删除最外围的结点，即顶部和左边均小于等于0'''
        min_area = self.min_area
        current_site = 0
        for node in self.current_node_list:
            if node is None or node[0] == -1:
                current_site += 1
                continue
            #self.current_node_list[current_site][7] = 0
            # if (node[0] == 0 and node[2] <= 0 and node[3] <= 0) or ((node[4]
            # * node[5] <= 0)):
            if node[4] <= least_gap or node[5] <= least_gap:
                self.delete_node(node[0], current_site, 0)
            elif node[4] * node[5] <= min_area:
                combine_sign = 0
                combine_node_list = []
                combine_node_list.append(current_site)
                brother_node_list = self.current_node_list[node[0]][8]
                current_next_site = brother_node_list.index(current_site) + 1
                brother_node_list = brother_node_list[current_next_site:]
                for brother_node_site in brother_node_list:
                    brother_node = self.current_node_list[brother_node_site]
                    if brother_node[4] * brother_node[5] <= min_area:
                        combine_node_list.append(brother_node_site)
                    else:
                        self.node_combine(combine_node_list, brother_node_site)
                        combine_sign = 1
                        break
                if combine_sign == 0:
                    for min_node in combine_node_list:
                        self.delete_node(node[0], min_node, 0)
            current_site += 1

    def contain_son_nodes(self, current_node, order_type, contain_son_mistake=5):
        '''判断输入的结点current_node是否完全包含其子结点（包含所占区域与文本），完全包含返回1
                        如果所有子结点面积均小于最小结点面积，则返回2，否则返回0'''
        if current_node[0] == -1 or len(current_node[8]) == 0:
            return 0
        contain_num = 0  # 包含的结点数量
        f_text_start = current_node[6]
        f_text_end = f_text_start + current_node[7]
        f_text = self.plan_text[f_text_start:f_text_end]  # 该结点所包含的文字
        for cnode_num in current_node[8]:  # 循环对其子结点判断，得到包含的子结点数目
            if order_type == 0:  # 当为正序检测时
                child_node = self.current_node_list[cnode_num]
            elif order_type == 1:  # 当为倒序检测时
                child_site = self.node_sum - cnode_num - 1
                child_node = self.current_node_list[child_site]
            if current_node[2] <= child_node[2] + contain_son_mistake and current_node[3] <= child_node[3] + contain_son_mistake\
                    and current_node[2] + current_node[4] >= child_node[2] + child_node[4] - contain_son_mistake\
                    and current_node[3] + current_node[5] >= child_node[3] + child_node[5] - contain_son_mistake:  # 计算区域面积是否包含
                c_text_start = child_node[6]
                c_text_end = c_text_start + child_node[7]
                c_text = self.plan_text[c_text_start:c_text_end]  # 子节点包含的文字
                if f_text.find(c_text) == -1:  # 判断文字是否包含
                    break
                contain_num += 1
        if contain_num == len(current_node[8]):  # 如果包含所有子结点的所占区域及文字，返回1
            return 1
        return 0

    def contain_del_max(self):
        '''对结点列表正序遍历，删除面积比阈值大、完全包含其所有子结点的结点（完全包含即包含区域面积和文字）'''
        current_site = 0  # 记录当前结点位置
        contain_son_nodes_sign = 0  # 完全包含标识，是为“1”，否为“0”
        for node in self.current_node_list:
            if node is None or node[0] == -1:
                current_site += 1
                continue
            area = node[4] * node[5]
            if area < self.select_area:  # 小于阈值跳过
                current_site += 1
                continue
            contain_son_nodes_sign = self.contain_son_nodes(
                node, 0)  # 判断是否完全包含
            if contain_son_nodes_sign == 1:  # 表明该结点包含所有子结点
                self.delete_node(node[0], current_site, 0)  # 删除该结点
            current_site += 1

    def contain_del_min_once(self):
        '''对结点列表倒序遍历，当前结点小于阈值，并完全包含其所有子结点时（包含所占区域与文本），删除其所有子结点 '''
        self.current_node_list.reverse()  # 列表倒序
        current_site = 0  # 记录当前结点的位置
        contain_son_nodes_sign = 0
        response = 0  # 用于判断本次循环遍历，是否进行了删除子结点操作
        for node in self.current_node_list:
            if node is None or node[0] == -1:
                current_site += 1
                continue
            area = node[4] * node[5]
            if area > self.select_area:  # 大于阈值跳过
                current_site += 1
                continue
            contain_son_nodes_sign = self.contain_son_nodes(node, 1)
            if contain_son_nodes_sign == 1:  # 如果包含所有子结点的所占区域及文字，则进一步判断是否删除
                for cnode_num in node[8]:
                    real_parents_site = self.node_sum - current_site - 1
                    self.delete_node(real_parents_site, cnode_num, 1)
                    response = 1
            current_site += 1
        self.current_node_list.reverse()
        return response

    def contain_del_min(self):
        '''循环执行contain_del_min_once，保留面积比阈值小、完全包含其所有子结点的结点，该结点小于阈值，但在该结点所在分支中最大'''
        response = 1
        while(response):
            response = self.contain_del_min_once()

    def combine_message_line(self, line_combine_mistake=2):
        '''对某一模块中以列表的形式（行或列）显示的结点进行合并，合并为一个结点'''
        line_max_area = self.line_max_area
        current_site = 0
        message_line_list = []
        for node in self.current_node_list:
            # 当行结点大于阈值时，则不合并
            if node is None or node[0] == -1 or (node[4] * node[5] > line_max_area):
                current_site += 1
                continue
            assist_check_node = node
            brother_node_list = self.current_node_list[node[0]][8]
            current_next_site = brother_node_list.index(current_site) + 1
            brother_node_list = brother_node_list[current_next_site:]
            judge_win = 0
            for brother_node_site in brother_node_list:
                brother_node = self.current_node_list[brother_node_site]
                if assist_check_node[1] != brother_node[1]:
                    # 选取结点名称相同的结点
                    continue
                # print brother_node_site, current_site, assist_check_node,
                # brother_node
                if (judge_win == 0 or judge_win == 1) \
                    and abs(assist_check_node[3] - brother_node[3]) <= line_combine_mistake \
                    and abs(assist_check_node[4] - brother_node[4]) <= line_combine_mistake \
                    and abs(assist_check_node[5] - brother_node[5]) <= line_combine_mistake \
                    and ((abs(assist_check_node[2] - (brother_node[2] + brother_node[4])) <= line_combine_mistake)
                         or ((abs(assist_check_node[2] + assist_check_node[4] - brother_node[2])) <= line_combine_mistake)):
                    # 选择左边、面积相同，且上下相邻的结点，否则继续判断
                    judge_win = 1
                    message_line_list.append(brother_node_site)
                    assist_check_node = brother_node
                elif (judge_win == 0 or judge_win == 2) \
                    and abs(assist_check_node[2] - brother_node[2]) <= line_combine_mistake \
                    and abs(assist_check_node[4] - brother_node[4]) <= line_combine_mistake \
                    and abs(assist_check_node[5] - brother_node[5]) <= line_combine_mistake \
                    and (abs(assist_check_node[3] - (brother_node[3] + brother_node[5])) <= line_combine_mistake
                         or abs(assist_check_node[3] + assist_check_node[5] - brother_node[3]) <= line_combine_mistake):
                    # 选择顶部、面积相同，且左右相邻的结点，否则退出循环
                    judge_win = 2
                    message_line_list.append(brother_node_site)
                    assist_check_node = brother_node
                else:
                    break
                # print brother_node_site, current_site, assist_check_node,
                # brother_node
            if len(message_line_list) >= 1:
                self.node_combine(message_line_list, current_site)
                message_line_list = []
            current_site += 1

    def delete_roll_bar(self, line_combine_mistake=2):
        '''删除滚动条，因为DIV,UL等均可做成滚动条，所以针对所有类型标签判断
                            依次遍历结点列表，提取当前标签之后和其父结点、结点名称、顶部、面积均相同，并且左右相邻的结点，
                            如果有结点在网页边界之外的话，则判定这一系列结点构成滚动条，此时仅留下第一个结点
        '''
        current_site = 0
        roll_bar_list = []
        for node in self.current_node_list:
            if node is None or node[0] == -1:
                current_site += 1
                continue
            assist_check_node = node
            brother_node_list = self.current_node_list[node[0]][8]
            current_next_site = brother_node_list.index(current_site) + 1
            brother_node_list = brother_node_list[current_next_site:]
            for brother_node_site in brother_node_list:
                brother_node = self.current_node_list[brother_node_site]
                if assist_check_node[1] != brother_node[1]:
                    # 选取结点名称相同的结点
                    continue
                if abs(assist_check_node[2] - brother_node[2]) <= line_combine_mistake \
                    and abs(assist_check_node[4] - brother_node[4]) <= line_combine_mistake \
                    and abs(assist_check_node[5] - brother_node[5]) <= line_combine_mistake \
                    and (abs(assist_check_node[3] - (brother_node[3] + brother_node[5])) <= line_combine_mistake
                         or abs(assist_check_node[3] + assist_check_node[5] - brother_node[3]) <= line_combine_mistake):
                    # 选取顶部、面积相同，并左右相邻的结点,暂且判定为滚动条结点
                    roll_bar_list.append(brother_node_site)
                    assist_check_node = brother_node
                else:
                    break
            if len(roll_bar_list) >= 1:
                roll_last_node = self.current_node_list[roll_bar_list[-1]]
                if roll_last_node[3] <= self.most_left_boundary\
                        or roll_last_node[3] + roll_last_node[5] >= self.most_right_boundary:  # 如果这一系列结点中最后一个在边界之外的话，则判定为滚动条
                    if node[3] <= self.most_left_boundary\
                            or node[3] + node[5] >= self.most_right_boundary:  # 如果该结点在边界之外的话，则找一个在边界内的结点显示
                        roll_bar_list.append(current_site)
                        for roll_node_site in roll_bar_list:
                            roll_node = self.current_node_list[roll_node_site]
                            if roll_node[3] > self.most_left_boundary\
                                    and roll_node[3] + roll_node[5] < self.most_right_boundary:  # 找一个在边界内的结点显示
                                roll_bar_list.remove(roll_node_site)
                                break
                    for roll_node_site in roll_bar_list:  # 删除除显示结点之外的所有结点
                        self.delete_node(node[0], roll_node_site, 0)
            roll_bar_list = []
            current_site += 1

    def return_result(self):
        '''选择筛选后的DOM树中非空且没有子结点的结点'''
        for node in self.current_node_list:
            if node is not None and len(node[8]) == 0:
                self.selected_node_list.append(node)
        return self.selected_node_list
