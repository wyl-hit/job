#-*- coding:utf-8 -*-

# 定义节点的属性


class decisionnode:

    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col   # col是待检验的判断条件所对应的列索引值
        self.value = value  # value对应于为了使结果为True，当前列必须匹配的值
        self.results = results  # 保存的是针对当前分支的结果，它是一个字典
        self.tb = tb  # desision node,对应于结果为true时，树上相对于当前节点的子树上的节点
        self.fb = fb  # desision node,对应于结果为true时，树上相对于当前节点的子树上的节点


class DecisionTree():

    def __init__(self):
        self.FeatureSet = []
        self.Label = []

    def load_data(self, fileName):
        with open(fileName, 'r')as f:
            data = f.read().split("\r\n")
        dataSet = []
        for one in data:
            one = one.replace(' ', ",").replace(",,", ",")
            tmp_data = one.split(",")
            dataSet.append(tmp_data)
        self.FeatureSet = []
        self.Label = []
        for i in dataSet:
            self.FeatureSet.append(i)
            self.Label.append(i[-1])

    # 基尼不纯度
    def uniquecounts(self, rows):
        results = {}
        for row in rows:
            # 计数结果在最后一列
            r = row[len(row) - 1]
            if r not in results:
                results[r] = 0
            results[r] += 1
        return results  # 返回一个字典

    # 熵
    def entropy(self, rows):
        from math import log
        log2 = lambda x: log(x) / log(2)
        results = self.uniquecounts(rows)  # {'None': 3, 'Basic': 1}
        # 开始计算熵的值
        ent = 0.0
        for r in results.keys():
            p = float(results[r]) / len(rows)
            ent = ent - p * log2(p)
        return ent

    # 随机放置的数据项出现于错误分类中的概率

    def giniimpurity(self, rows):
        total = len(rows)
        counts = self.uniquecounts(rows)
        imp = 0
        for k1 in counts:
            p1 = float(counts[k1]) / total
            for k2 in counts:  # 这个循环是否可以用（1-p1）替换？
                if k1 == k2:
                    continue
                p2 = float(counts[k2]) / total
                imp += p1 * p2
        return imp

    # 改进giniimpurity
    def giniimpurity_2(self, rows):
        total = len(rows)
        counts = self.uniquecounts(rows)
        imp = 0
        for k1 in counts.keys():
            p1 = float(counts[k1]) / total
            imp += p1 * (1 - p1)
        return imp

    # 在某一列上对数据集进行拆分。可应用于数值型或因子型变量
    def divideset(self, rows, column, value):
        # 定义一个函数，判断当前数据行属于第一组还是第二组
        split_function = None
        if isinstance(value, int) or isinstance(value, float):
            split_function = lambda row: row[column] >= value
        else:
            split_function = lambda row: row[column] == value
        # 将数据集拆分成两个集合，并返回
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        return(set1, set2)

    # 以递归方式构造树

    def buildtree(self, rows, scoref=entropy):
        if len(rows) == 0:
            return decisionnode()
        current_score = scoref(self, rows)
        # 定义一些变量以记录最佳拆分条件
        best_gain = 0.0
        best_criteria = None
        best_sets = None
        # 去掉最后一个类别标签
        column_count = len(rows[0]) - 1
        for col in range(0, column_count):
            # 在当前列中生成一个由不同值构成的序列
            column_values = {}
            for row in rows:
                column_values[row[col]] = 1  # 初始化 {"a":1}
            # 根据这一列中的每个值，尝试对数据集进行拆分
            for value in column_values.keys():
                (set1, set2) = self.divideset(rows, col, value)
                # 信息增益
                p = float(len(set1)) / len(rows)
                gain = current_score - p * \
                    scoref(self, set1) - (1 - p) * scoref(self, set2)
                if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                    best_gain = gain
                    best_criteria = (col, value)
                    best_sets = (set1, set2)

        # 创建子分支
        if best_gain > 0:
            trueBranch = self.buildtree(best_sets[0])  # 递归调用
            falseBranch = self.buildtree(best_sets[1])
            return decisionnode(col=best_criteria[0], value=best_criteria[1],
                                tb=trueBranch, fb=falseBranch)
        else:
            return decisionnode(results=self.uniquecounts(rows))

    # 决策树的显示

    def printtree(self, tree, indent=''):
        # 是否是叶节点
        if tree.results is not None:
            print str(tree.results)
        else:
            # 打印判断条件
            # print str(tree.col) + ":" + str(tree.value) + "? "
            # 打印分支
            print indent + "T->",
            self.printtree(tree.tb, indent + " ")
            print indent + "F->",
            self.printtree(tree.fb, indent + " ")

    # 对新的观测数据进行分类

    def classify(self, observation, tree):
        if tree.results is not None:
            return tree.results
        else:
            v = observation[tree.col]
            branch = None
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            else:
                if v == tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            return self.classify(observation, branch)


if __name__ == '__main__':
    '''
    my_data = [['slashdot', 'USA', 'yes', 18, 'None'],
               ['google', 'France', 'yes', 23, 'Premium'],
               ['digg', 'USA', 'yes', 24, 'Basic'],
               ['kiwitobes', 'France', 'yes', 23, 'Basic'],
               ['google', 'UK', 'no', 21, 'Premium'],
               ['(direct)', 'New Zealand', 'no', 12, 'None'],
               ['(direct)', 'UK', 'no', 21, 'Basic'],
               ['google', 'USA', 'no', 24, 'Premium'],
               ['slashdot', 'France', 'yes', 19, 'None'],
               ['digg', 'USA', 'no', 18, 'None'],
               ['google', 'UK', 'no', 18, 'None'],
               ['kiwitobes', 'UK', 'no', 19, 'None'],
               ['digg', 'New Zealand', 'yes', 12, 'Basic'],
               ['slashdot', 'UK', 'no', 21, 'None'],
               ['google', 'UK', 'yes', 18, 'Basic'],
               ['kiwitobes', 'France', 'yes', 19, 'Basic']]
    '''

    # giniimpurity(my_data)

    # giniimpurity_2(my_data)
    d = DecisionTree()
    d.load_data("crx.data")

    tree = d.buildtree(d.FeatureSet)

    d.printtree(tree=tree)

    print d.classify(['b',59.67,1.54,'u','g','q','v',0.125,'t','f',0,'t','g',00260,0], tree)
