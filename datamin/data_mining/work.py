#-*- coding:utf-8 -*-
'''
from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np
from sklearn.cross_validation import train_test_split  # 这里是引用了交叉验证
from sklearn.preprocessing import LabelEncoder

lb = LabelEncoder()
with open("lenses.data", "r") as f:
    dataSet = f.read().split("\r\n")
le = LabelEncoder()
FeatureSet = []
Label = []
for i in dataSet:
    i.replace(" ", ",")
    FeatureSet.append(i[: -1])
    Label.append(i[-1])
X_train, X_test, y_train, y_test = train_test_split(
    FeatureSet, Label, random_state = 1)  # 将数据随机分成训练集和测试集
print X_train
# print X_test
print y_train
# print y_test
# print iris
clf=tree.DecisionTreeClassifier()
clf=clf.fit(X_train, y_train)
from sklearn.externals.six import StringIO
with open("isBuy.dot", 'w') as f:
    f=tree.export_graphviz(clf, out_file = f)
import os
os.unlink('isBuy.dot')
#
from sklearn.externals.six import StringIO
import pydot  # 注意要安装pydot2这个python插件。否则会报错。
dot_data=StringIO()
tree.export_graphviz(clf, out_file = dot_data)
graph=pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("isBuy.pdf")  # 将决策树以pdf格式输出

pre_labels=clf.predict(X_test)
print pre_labels
'''
from sklearn.datasets import load_iris
from sklearn import tree
with open("lenses.data",'r')as f:
    data = f.read().split("\r\n")
dataSet = []
for one in data:
    one = one.replace(' ', ",").replace(",,",",")
    tmp_data = one.split(",")
    dataSet.append(tmp_data)
print dataSet

from sklearn.cross_validation import train_test_split  # 这里是引用了交叉验证

FeatureSet = []
Label = []
for i in dataSet:
    FeatureSet.append(i[:-1])
    Label.append(i[-1])
X_train, X_test, y_train, y_test = train_test_split(
    FeatureSet, Label, random_state=1)  # 将数据随机分成训练集和测试集
# print iris
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
from sklearn.externals.six import StringIO
with open("isBuy.dot", 'w') as f:
    f = tree.export_graphviz(clf, out_file=f)
import os
os.unlink('isBuy.dot')
#
from sklearn.externals.six import StringIO
import pydot  # 注意要安装pydot2这个python插件。否则会报错。
dot_data = StringIO()
tree.export_graphviz(clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
#graph.write_pdf("isBuy.pdf")  # 将决策树以pdf格式输出

pre_labels = clf.predict(X_test)
print pre_labels
