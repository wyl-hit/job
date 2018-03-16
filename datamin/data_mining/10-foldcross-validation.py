#-*- coding:utf-8 -*-
import os
import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split  # 这里是引用了交叉验证
from sklearn.preprocessing import LabelEncoder
from sklearn import cross_validation
from sklearn import metrics
le = LabelEncoder()


def loadDataSet(fileName):
    with open(fileName, 'r')as f:
        data = f.read().split("\r\n")
    dataSet = []
    for one in data:
        one = one.replace(' ', ",").replace(",,", ",")
        tmp_data = one.split(",")
        dataSet.append(tmp_data)

    FeatureSet = []
    Label = []
    print dataSet
    for i in dataSet:
        le.fit(i)
        FeatureSet.append(le.transform(i[:-1]))
        Label.append(i[-1])
    return FeatureSet, Label


def loadSubDataSet(fileName):
    with open(fileName, 'r')as f:
        data = f.read().split("\n")
    dataSet = []
    for one in data:
        one = one.replace(' ', ",").replace(",,", ",")
        tmp_data = one.split(",")
        dataSet.append(tmp_data)
    FeatureSet = []
    Label = []
    for i in dataSet:
        le.fit(i)
        FeatureSet.append(le.transform(i[:-1]))
        Label.append(i[-1])
    return FeatureSet, Label


def splitDataSet(fileName, split_size, outdir):
    if not os.path.exists(outdir):  # if not outdir,makrdir
        os.makedirs(outdir)
    fr = open(fileName, 'r')  # open fileName to read
    num_line = 0
    onefile = fr.readlines()
    num_line = len(onefile)
    arr = np.arange(num_line)  # get a seq and set len=numLine
    np.random.shuffle(arr)  # generate a random seq from arr
    list_all = arr.tolist()
    each_size = (num_line + 1) / split_size  # size of each split sets
    split_all = []
    each_split = []
    count_num = 0
    count_split = 0  # count_num 统计每次遍历的当前个数
    # count_split 统计切分次数
    for i in range(len(list_all)):  # 遍历整个数字序列
        each_split.append(onefile[int(list_all[i])].strip())
        count_num += 1
        if count_num == each_size:
            count_split += 1
            array_ = np.array(each_split)
            np.savetxt(outdir + "/split_" + str(count_split) + '.txt',
                       array_, fmt="%s", delimiter='\r\n')  # 输出每一份数据
            split_all.append(each_split)  # 将每一份数据加入到一个list中
            each_split = []
            count_num = 0
    return split_all


def underSample(datafile):  # 只针对一个数据集的下采样
    dataMat, labelMat = loadSubDataSet(datafile)  # 加载数据
    pos_num = 0
    pos_indexs = []
    neg_indexs = []
    for i in range(len(labelMat)):  # 统计正负样本的下标
        if labelMat[i] == "+":
            pos_num += 1
            pos_indexs.append(i)
            continue
        neg_indexs.append(i)
    np.random.shuffle(neg_indexs)
    neg_indexs = neg_indexs[0:pos_num]

    outfile = []
    with open(datafile, 'r') as fr:
        outfile = fr.readlines()
    #outfile = content.split("\n")

    '''    
        for i in range(pos_num):
        pos_line = onefile[pos_indexs[i]]
        outfile.append(pos_line)
        neg_line = onefile[neg_indexs[i]]
        outfile.append(neg_line)
    '''

    return outfile  # 输出单个数据集采样结果


def generateDataset(datadir, outdir):  # 从切分的数据集中，对其中九份抽样汇成一个,\
    # 剩余一个做为测试集,将最后的结果按照训练集和测试集输出到outdir中
    if not os.path.exists(outdir):  # if not outdir,makrdir
        os.makedirs(outdir)
    listfile = os.listdir(datadir)
    train_all = []
    test_all = []
    cross_now = 0
    for eachfile1 in listfile:  # eachfile1 test
        train_sets = []
        test_sets = []
        cross_now += 1  # 记录当前的交叉次数
        for eachfile2 in listfile:
            if eachfile2 != eachfile1:  # 对其余九份欠抽样构成训练集
                one_sample = underSample(datadir + '/' + eachfile2)
                for i in range(len(one_sample)):
                    train_sets.append(one_sample[i])
        # 将训练集和测试集文件单独保存起来
        with open(outdir + "/test_" + str(cross_now) + ".datasets", 'w') as fw_test:
            with open(datadir + '/' + eachfile1, 'r') as fr_testsets:
                for each_testline in fr_testsets:
                    test_sets.append(each_testline)
            for oneline_test in test_sets:
                fw_test.write(oneline_test)  # 输出测试集
            test_all.append(test_sets)  # 保存训练集
        with open(outdir + "/train_" + str(cross_now) + ".datasets", 'w') as fw_train:
            for oneline_train in train_sets:
                oneline_train = oneline_train
                fw_train.write(oneline_train)  # 输出训练集
            train_all.append(train_sets)  # 保存训练集
    return train_all, test_all


def performance(labelArr, predictArr):  # 类标签为int类型
    # labelArr[i] is actual value,predictArr[i] is predict value
    TP = 0.
    TN = 0.
    FP = 0.
    FN = 0.
    for i in range(len(labelArr)):
        if labelArr[i] == "+\n" and predictArr[i] == "+\n":
            TP += 1.
        if labelArr[i] == "+\n" and predictArr[i] == "-\n":
            FN += 1.
        if labelArr[i] == "-\n" and predictArr[i] == "+\n":
            FP += 1.
        if labelArr[i] == "-\n" and predictArr[i] == "-\n":
            TN += 1.
    SN = TP / (TP + FN)  # Sensitivity = TP/P  and P = TP + FN
    SP = TN / (FP + TN)  # Specificity = TN/N  and N = TN + FP
    #MCC = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
    return SN, SP


def classifier(clf, train_X, train_y, test_X, test_y):  # X:训练特征，y:训练标号
    # train with randomForest
    clf = clf.fit(train_X, train_y)
    #==========================================================================
    # test randomForestClassifier with testsets
    print " test begin."
    predict_ = clf.predict(test_X)  # return type is float64
    proba = clf.predict_proba(test_X)  # return type is float64
    score_ = clf.score(test_X, test_y)
    print " test end."
    #==========================================================================
    # Modeal Evaluation
    ACC = metrics.accuracy_score(test_y, predict_)
    MCC = metrics.matthews_corrcoef(test_y, predict_)
    SN, SP = performance(test_y, predict_)
    print 22222222
    print SP, ACC
    
    #AUC = roc_auc_score(test_labelMat, proba)
    return ACC, SN, SP


def mean_fun(onelist):
    count = 0
    for i in onelist:
        count += i
    return float(count / len(onelist))


def crossValidation(clf, clfname, curdir, train_all, test_all):
    global le
    os.chdir(curdir)
    # 构造出纯数据型样本集
    cur_path = curdir
    ACCs = []
    SNs = []
    SPs = []
    for i in range(len(train_all)):
        os.chdir(cur_path)
        train_data = train_all[i]
        train_X = []
        train_y = []
        test_data = test_all[i]
        test_X = []
        test_y = []
        for eachline_train in train_data:
            # ['b,27.83,4,y,p,i,h,5.75,t,t,02,t,g,00075,0,-\n']
            one_train = eachline_train.split(',')
            one_train_format = []
            le.fit(one_train)
            one_train_format = le.transform(one_train[:-1])
            
            train_X.append(one_train_format)
            train_y.append(one_train[-1])     
        for eachline_test in test_data:
            one_test = eachline_test.split(',')
            one_test_format = []
            le.fit(one_test)
            one_test_format = le.transform(one_test[:-1])
            test_X.append(one_test_format)
            test_y.append(one_test[-1])
        #======================================================================
        # classifier start here
        if not os.path.exists(clfname):  # 使用的分类器
            os.mkdir(clfname)
        out_path = clfname + "/" + clfname + "_00" + str(i)  # 计算结果文件夹
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        os.chdir(out_path)
        ACC, SN, SP = classifier(clf, train_X, train_y, test_X, test_y)
        ACCs.append(ACC)
        SNs.append(SN)
        SPs.append(SP)
        #======================================================================
    ACC_mean = mean_fun(ACCs)
    SN_mean = mean_fun(SNs)
    SP_mean = mean_fun(SPs)
    #==========================================================================
    return ACC_mean, SN_mean, SP_mean


if __name__ == '__main__':
    datasets = "crx.data"
    os.chdir("./")  # 你的数据存放目录
    datadir = "./split10_1"  # 切分后的文件输出目录
    splitDataSet(datasets, 10, datadir)  # 将数据集datasets切为十个保存到datadir目录中
    #==========================================================================
    outdir = "sample_data1"  # 抽样的数据集存放目录

    train_all, test_all = generateDataset(datadir, outdir)  # 抽样后返回训练集和测试集

    #==========================================================================
    # 分类器部分
    clf = tree.DecisionTreeClassifier()
    # ==========================================================================
    clfname = "DecisionTree"
    curdir = "./"  # 工作目录
    # clf:分类器,clfname:分类器名称,curdir:当前路径,train_all:训练集,test_all:测试集
    ACC_mean, SN_mean, SP_mean = crossValidation(
        clf, clfname, curdir, train_all, test_all)
    print ACC_mean, SN_mean, SP_mean  # 将ACC均值，SP均值，SN均值都输出到控制台
