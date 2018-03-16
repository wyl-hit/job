#-*- coding:utf-8 -*-
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split  # 这里是引用了交叉验证
from sklearn.preprocessing import LabelEncoder
from sklearn import cross_validation

with open("crx.data", 'r')as f:
    data = f.read().split("\r\n")
dataSet = []
for one in data:
    one = one.replace(' ', ",").replace(",,", ",")
    tmp_data = one.split(",")
    dataSet.append(tmp_data)


le = LabelEncoder()
FeatureSet = []
Label = []
for i in dataSet:
    print i
    le.fit(i)
    FeatureSet.append(le.transform(i[:-1]))
    Label.append(i[-1])

X_train, X_test, y_train, y_test = train_test_split(
    FeatureSet, Label, random_state=1)  # 将数据随机分成训练集和测试集
# print iris

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
pre_labels = clf.predict(X_test)
print pre_labels


a = ['b,27.83,4,y,p,i,h,5.75,t,t,02,t,g,00075,0,-']
le.fit(a)
print le.transform(a[:-1])
