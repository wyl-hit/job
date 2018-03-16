# encoding:utf8
from select_node import SNode


class VTree():

    '''
    dom tree filtrate and save
    '''

    def __init__(self, mongo_operate):
        self.mongo_operate = mongo_operate
        self.node_list = []
        self.node_num = -1
        self.selected_node_list = []
        self.snode = None

    def set_page_text(self, text):
        self.plan_text = text

    def add_node(self, parent=0, tag='html', top=0, left=0, height=0, width=0, node_plan_text=None):
        self.node_list.append([])
        text_start = self.plan_text.find(node_plan_text)
        if text_start == -1:
            text_start = len(self.plan_text)
            self.plan_text += node_plan_text
        self.node_list[-1] = [parent, tag, top, left, height,
                              width, text_start, len(node_plan_text), []]
        self.node_num += 1
        self.node_list[parent][-1].append(self.node_num)
        #print self.node_list
        return self.node_num

    def select_node(self):
        '''
        dom tree filtrate
        '''
        self.snode = SNode(self.node_list, self.plan_text)  # 创建选择函数类的对象
        self.snode.delete_first_node()  # 清空第一个结点，但保留其子结点列表
        self.snode.delete_whole_node()  # 删除最外围的结点，和面积等于0的结点
        self.snode.contain_del_max()  # 删除面积比阈值大、完全包含其所有子结点的结点
        self.snode.contain_del_min()  # 若当前结点小于阈值，并完全包含其所有子结点时，删除其所有子结点
        self.snode.combine_message_line()  # 对网页结构的某一模块中以列表的形式一行一行显示的结点进行合并
        self.snode.delete_roll_bar()  # 删除滚动条
        # 选择筛选后的DOM树中非空且没有子结点的结点
        self.selected_node_list = self.snode.return_result()
        self.plan_text = self.snode.plan_text

    def get_output_name(self, url):
        tree_name = url.replace('.com', '~').replace('www.', '!').replace('https://', '{')\
            .replace('http://', '+').replace('/', '^').replace('.', '_').replace('?', '[').replace('#', ']')
        return tree_name

    def dump(self, current_url, current_url_type, current_time_path, current_path):
        '''
        dom tree save
        '''
        # save selected node in mongo
        new_node_list = []
        for node in self.selected_node_list:
            new_node_list.append(node[2:])
        self.mongo_operate.add_web_tree(current_url, current_url_type, new_node_list)
        # save in web path
        with open(current_time_path + '/block.html', 'wb') as f:
            f.write(
                '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>\n')
            k = 0
            for node in self.selected_node_list:
                #f.write('<p style="position: absolute; top: %spx; left: %spx; height: %spx; width: %spx; border: solid 2px red;">%s</p>\n' % (node[2],node[3],node[4],node[5],str(k)+''+self.plan_text[node[6]:node[6] + node[7]]))
                f.write('<p style="position: absolute; top: %spx; left: %spx; height: %spx; width: %spx; border: solid 2px red;">%s</p>\n' % (node[2], node[3], node[4], node[5], str(
                    k) + ' ' + str(node[0]) + ' ' + str(node[2]) + ' ' + str(node[3]) + ' ' + str(node[4]) + ' ' + str(node[5])))  # +' '+self.plan_text[node[6]:node[6] + node[7]]))
                k += 1
            f.write('</body></html>\n')

        # save in current run path , output
        filename = self.get_output_name(current_url)[:200]
        with open(current_path + '/output/' + filename + '.html', 'wb') as f:
            f.write(
                '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head><body>\n')
            k = 0
            for node in self.selected_node_list:
                #f.write('<p style="position: absolute; top: %spx; left: %spx; height: %spx; width: %spx; border: solid 2px red;">%s</p>\n' % (node[2],node[3],node[4],node[5],str(k)+''+self.plan_text[node[6]:node[6] + node[7]]))
                f.write('<p style="position: absolute; top: %spx; left: %spx; height: %spx; width: %spx; border: solid 2px red;">%s</p>\n' % (node[2], node[3], node[4], node[5], str(
                    k) + ' ' + str(node[0]) + ' ' + str(node[2]) + ' ' + str(node[3]) + ' ' + str(node[4]) + ' ' + str(node[5])))  # +' '+self.plan_text[node[6]:node[6] + node[7]]))
                k += 1
            f.write('</body></html>\n')

        with open(current_path + '/output/' + filename + 'block.txt', 'w') as f2:
            k = 0
            for node in self.selected_node_list:
                f2.write('|#|' + str(k) + '-' + str(node[2]) + '-' + str(
                    node[3]) + '-' + str(node[4]) + '-' + str(node[5]) + '\n')
                k += 1

if __name__ == '__main__':
    print 'run over!'
