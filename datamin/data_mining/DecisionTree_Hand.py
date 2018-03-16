#-*- coding:utf-8 -*-

# 定义节点的属性

from sklearn import metrics
from sklearn.model_selection import KFold
from PIL import Image, ImageDraw
from sklearn import cross_validation
import random
from random import choice


class decisionnode:

    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col   # col是待检验的判断条件所对应的列索引值
        self.value = value  # valus就是判断条件
        self.results = results  # 叶子节点保存最后判断结果的变量
        self.tb = tb  # 条件value成立指向的分支
        self.fb = fb  # 条件value不成立指向的分支

tree = ''


class DecisionTree():

    def __init__(self):
        self.FeatureSet = []
        self.Label = []
        self.threshold = 0.0
        self.property = []

    def performance(self, labelArr, predictArr):  # 类标签为int类型
        # labelArr[i] is actual value,predictArr[i] is predict value
        TP = 0.
        TN = 0.
        FP = 0.
        FN = 0.
        for i in range(len(labelArr)):
            if labelArr[i] == "+" and predictArr[i] == "+":
                TP += 1.
            if labelArr[i] == "+" and predictArr[i] == "-":
                FN += 1.
            if labelArr[i] == "-" and predictArr[i] == "+":
                FP += 1.
            if labelArr[i] == "-" and predictArr[i] == "-":
                TN += 1.
        # 召回率（recall）Sensitivity = TP/P  and P = TP + FN
        SN = TP / (TP + FN + 0.001)
        # Specificity = TN/N  and N = TN + FP
        # MCC = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
        return SN

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

    def handle_data(self):
        column_count = len(self.FeatureSet[0]) - 1
        size_num = len(self.FeatureSet)
        for i in range(0, size_num / 10):
            number = random.randint(0, size_num - 1)
            shame_number = random.randint(0, column_count - 1)
            self.FeatureSet[number][shame_number] = None

    # 返回rows里各种可能结果和结果的出现的次数
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

    # misclassification
    def misclassification(self, rows):
        from math import log
        log2 = lambda x: log(x) / log(2)
        results = self.uniquecounts(rows)  # {'None': 3, 'Basic': 1}
        # 开始计算熵的值
        ent = 0.0
        max_mis = 0.0
        for r in results.keys():
            p = float(results[r]) / len(rows)
            if max_mis < p:
                max_mis = p
        return 1 - max_mis

    # 基尼不纯度
    def giniimpurity_2(self, rows):
        total = len(rows)
        counts = self.uniquecounts(rows)
        imp = 0
        for k1 in counts.keys():
            p1 = float(counts[k1]) / total
            imp += p1 * p1
        return 1 - imp

    # 预减枝
    def pre_pruning(self, mingain):
        self.threshold = mingain

    # 后减枝
    def post_pruning(self, tree, mingain):
        # 如果分支不是叶节点，则对其进行剪枝
        if tree.tb.results is None:
            self.post_pruning(tree.tb, mingain)
        if tree.fb.results is None:
            self.post_pruning(tree.fb, mingain)
        # 如果两个子分支都是叶节点，判断是否能够合并
        if tree.tb.results is not None and tree.fb.results is not None:
            # 构造合并后的数据集
            tb, fb = [], []
            for v, c in tree.tb.results.items():
                tb += [[v]] * c
            # print tb
            for v, c in tree.fb.results.items():
                fb += [[v]] * c
            # 检查熵的减少量
            delta = self.entropy(tb + fb) - \
                (self.entropy(tb) + self.entropy(fb) / 2)
            if delta < mingain:
                # 合并分支
                tree.tb, tree.fb = None, None
                tree.results = self.uniquecounts(tb + fb)

    # 根据第column列的值是否等于value，或者大于等于value来对输入rows数据，结果分为两组
    def divideset(self, rows, column, value):
        # 定义一个函数，判断当前数据行属于第一组还是第二组
        split_function = None
        if isinstance(value, int) or isinstance(value, float):
            split_function = lambda row: row[column] >= value
        else:
            split_function = lambda row: row[column] == value
        # 将数据集拆分成含有该属性和不含有该属性的两个集合
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
                # 针对每个属性(value)进行划分数据集
                if col not in self.property:
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
        if best_gain > self.threshold:
            try:
                tmp = float(rows[0][best_criteria[0]])
            except ValueError:
                self.property.append(best_criteria[0])
            trueBranch = self.buildtree(best_sets[0])  # 递归调用
            falseBranch = self.buildtree(best_sets[1])
            return decisionnode(col=best_criteria[0], value=best_criteria[1],
                                tb=trueBranch, fb=falseBranch)
        else:
            return decisionnode(results=self.uniquecounts(rows))

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

    def predict(self, X_test, tree):
        pre_label = []
        for i in X_test:
            pre_label.append(d.classify(i, tree).keys()[0])
        return pre_label

    def getwidth(self, tree):
        if tree.tb is None and tree.fb is None:
            return 1
        return self.getwidth(tree.tb) + self.getwidth(tree.fb)

    def getdepth(self, tree):
        if tree.tb is None and tree.fb is None:
            return 0
        return max(self.getdepth(tree.tb), self.getdepth(tree.fb)) + 1

    '''
    drawtree为待绘制的树确定了一个合理的尺寸，并设置好了画布（canvas），然后将画布和根节点传给了drawnode函数
    '''

    def drawtree(self, tree, jpeg='treepre.jpg'):
        w = self.getwidth(tree) * 100
        h = self.getdepth(tree) * 100 + 120

        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        self.drawnode(draw, tree, w / 2, 20)
        img.save(jpeg, 'JPEG')

    def drawnode(self, draw, tree, x, y):
        if tree.results == None:
            # 得到每个分支的宽度
            w1 = self.getwidth(tree.fb) * 100
            w2 = self.getwidth(tree.tb) * 100

            # 确定此节点所需要占据的空间,最左边left，最右边right
            left = x - (w1 + w2) / 2
            right = x + (w1 + w2) / 2

            # 绘制判断条件字符串
            draw.text((x - 20, y - 10), str(tree.col) +
                      ':' + str(tree.value), (0, 0, 0))

            # 绘制到分支的连线，从当前节点画到其左右子节点
            draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
            draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))

            # 绘制分支的节点
            self.drawnode(draw, tree.fb, left + w1 / 2, y + 100)
            self.drawnode(draw, tree.tb, right - w2 / 2, y + 100)
        else:
            txt = '\n'.join(['%s:%d' % v for v in tree.results.items()])
            draw.text((x - 20, y), txt, (0, 0, 0))

    # 处理缺失值
    # print mdclassify(tree,['google','France',None,None])
    # '''
    # {'None': 0.125, 'Premium': 2.25, 'Basic': 0.125}
    def mdclassify(self, tree, data):
        if tree.results is not None:
            return tree.results
        else:
            if data[tree.col] is None:
                tr, fr = self.mdclassify(
                    tree.tb, data), self.mdclassify(tree.fb, data)
                tcount = sum(tr.values())  # 该分支的样本总数
                fcount = sum(fr.values())
                tw = float(tcount) / (tcount + fcount)  # 流入该分支的样本占父节点样本的比重
                fw = float(fcount) / (tcount + fcount)
                result = {}
                for k, v in tr.items():
                    result[k] = v * tw
                for k, v in fr.items():
                    if k not in result:
                        result[k] = 0
                    result[k] += v * fw
                return result
            else:
                branch = None
                if isinstance(data[tree.col], int) or isinstance(data[tree.col], float):
                    if data[tree.col] < tree.value:
                        branch = tree.fb
                    else:
                        branch = tree.tb
                else:
                    if data[tree.col] != tree.value:
                        branch = tree.fb
                    else:
                        branch = tree.tb
                return self.mdclassify(branch, data)

    def KFold_method(self):
        kf = KFold(n_splits=10)
        for train_index, test_index in kf.split(self.FeatureSet):
            X_train = []
            X_test = []
            y_train = []
            y_test = []
            for trainid in train_index.tolist():
                X_train.append(self.FeatureSet[trainid])
                y_train.append(self.Label[trainid])

            for testid in test_index.tolist():
                X_test.append(self.FeatureSet[testid])
                y_test.append(self.Label[testid])

            tree = self.buildtree(X_train)
            #self.post_pruning(tree, 0.3)
            pre_labels = self.predict(X_test, tree)

            # Modeal Evaluation
            ACC = metrics.accuracy_score(y_test, pre_labels)
        #    MCC = metrics.matthews_corrcoef(y_test, pre_labels)
            SN = self.performance(y_test, pre_labels)
        #    print SP, SN
            print ACC, SN

    def Bootstrap_method(self):
        rs = cross_validation.ShuffleSplit(
            len(self.FeatureSet), 10, 0.25, random_state=0)
        for train_index, test_index in rs:
            X_train = []
            X_test = []
            y_train = []
            y_test = []
            for trainid in train_index.tolist():
                X_train.append(self.FeatureSet[trainid])
                y_train.append(self.Label[trainid])

            for testid in test_index.tolist():
                X_test.append(self.FeatureSet[testid])
                y_test.append(self.Label[testid])

            tree = self.buildtree(X_train)
            #self.post_pruning(tree, 0.3)
            pre_labels = self.predict(X_test, tree)
            # Modeal Evaluation
            ACC = metrics.accuracy_score(y_test, pre_labels)
            MCC = metrics.matthews_corrcoef(y_test, pre_labels)
            SN = self.performance(y_test, pre_labels)
            print ACC, SN


if __name__ == '__main__':
    d = DecisionTree()
    d.load_data("crx.data")
    # d.pre_pruning(0.001)
    # d.handle_data()
    #tree = d.buildtree(d.FeatureSet)

    #d.post_pruning(tree, 0.3)
    # d.KFold_method()

    d.Bootstrap_method()
    #d.drawtree(tree)
   # print d.mdclassify(tree, ['b', None, 1.54, 'u', 'g', 'q', 'v', 0.125,
   #                           't', None, 0, 't', 'g', 00260, 0])

    # print d.classify(['b', 59.67, 1.54, 'u', 'g', 'q', 'v', 0.125, 't', 'f',
    #       0, 't', 'g', 00260, 0], tree).keys()[0]
