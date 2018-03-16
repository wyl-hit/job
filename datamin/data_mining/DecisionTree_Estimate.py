#-*- coding:utf-8 -*-
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split  # 这里是引用了交叉验证
from sklearn.preprocessing import LabelEncoder
from sklearn import cross_validation
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.metrics import roc_auc_score
import pydot
import numpy as np
from sklearn.ensemble import AdaBoostClassifier


class DecisionTree():

    def __init__(self):
        self.FeatureSet = []
        self.Label = []

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
        SN = TP / (TP + FN + 0.001)  # 召回率（recall）Sensitivity = TP/P  and P = TP + FN
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
        le = LabelEncoder()
        self.FeatureSet = []
        self.Label = []
        for i in dataSet:
            le.fit(i)
            test_targets = le.transform(i[:-1]).tolist()
            self.FeatureSet.append(le.transform(i[:-1]))
            self.Label.append(i[-1])

    def holdout_method(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.FeatureSet, self.Label, random_state=1)  # 将数据随机分成训练集和测试集
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X_train, y_train)
        pre_labels = clf.predict(X_test)
        #clf = AdaBoostClassifier(n_estimators=100)
        #clf = clf.fit(X_train, y_train)
        #pre_labels = clf.predict(X_test)
        #print pre_labels
        # Modeal Evaluation
        ACC = metrics.accuracy_score(y_test, pre_labels)
        MCC = metrics.matthews_corrcoef(y_test, pre_labels)
        SN = self.performance(y_test, pre_labels)
        print SN
        print ACC
        
        #self.draw_tree(clf)

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
            #clf = tree.DecisionTreeClassifier()        
            #clf = clf.fit(X_train, y_train)
            #pre_labels = clf.predict(X_test)
            clf = AdaBoostClassifier(n_estimators=100)
            clf = clf.fit(X_train, y_train)
            pre_labels = clf.predict(X_test)
            # Modeal Evaluation
            ACC = metrics.accuracy_score(y_test, pre_labels)
            MCC = metrics.matthews_corrcoef(y_test, pre_labels)
            SN = self.performance(y_test, pre_labels)
            print ACC, SN
             

    def Bootstrap_method(self):
        rs = cross_validation.ShuffleSplit(
            len(self.FeatureSet), 10, 0.25, random_state=0)
        clf = tree.DecisionTreeClassifier()
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

            #clf = clf.fit(X_train, y_train)
           # pre_labels = clf.predict(X_test)
            clf = AdaBoostClassifier(n_estimators=100)
            clf = clf.fit(X_train, y_train)
            pre_labels = clf.predict(X_test)
            # Modeal Evaluation
            ACC = metrics.accuracy_score(y_test, pre_labels)
            MCC = metrics.matthews_corrcoef(y_test, pre_labels)
            SN = self.performance(y_test, pre_labels)
            print ACC,SN
           

    def AdaBoostClassifier_method(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.FeatureSet, self.Label, random_state=1)
        clf = AdaBoostClassifier(n_estimators=100)
        clf = clf.fit(X_train, y_train)
        pre_labels = clf.predict(X_test)
        print pre_labels
        ACC = metrics.accuracy_score(y_test, pre_labels)
        print ACC

    def draw_tree(self, clf):
        dot_data = StringIO()
        tree.export_graphviz(clf, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph[0].write_pdf("tree.pdf")

if __name__ == '__main__':
    d = DecisionTree()
    d.load_data("crx.data")
    #d.holdout_method()

    #d.KFold_method()
    d.Bootstrap_method()
    #d.AdaBoostClassifier_method()
# http://ogrisel.github.io/scikit-learn.org/sklearn-tutorial/modules/generated/sklearn.tree.DecisionTreeClassifier.html
