#-*-coding:utf-8-*-
'''
Created on 2015年8月24日

@author: yx
要求3个参数，网址 保存名 字符串数组
'''
import sys
import os
import os.path
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from PyQt4 import QtNetwork
reload(sys)
import json
from json import *
from urlparse import urlparse
sys.setdefaultencoding('utf-8')
current_path = sys.path[0]


class Pagescreen(QWidget):

    def __init__(self, task):
        super(Pagescreen, self).__init__()
        self.url = task['model_url']
        self.shot_name = task['shot_name']
        #self.destDir = "/opt/lampp/htdocs/"

        self.parts = urlparse(self.url)
        self.host = self.parts.netloc
        self.savename = current_path + '/' + self.host + '.png'

        self.webpage = None
        self.input = task['post_url']
        fd = QFile(current_path + "/js/red.js")
        if fd.open(QIODevice.ReadOnly | QFile.Text):
            self.red = QTextStream(fd).readAll()
            fd.close()
        else:
            self.red = ''
        fd = QFile(current_path + "/js/jquery-2.1.1.js")
        if fd.open(QIODevice.ReadOnly | QFile.Text):
            self.jquery = QTextStream(fd).readAll()
            fd.close()
        else:
            self.jquery = ''
        self.shot()

    def shot(self):  # 载入网页
        print os.getpid()
        print self.url
        web = QWebView(self)
        request = QtNetwork.QNetworkRequest()
        request.setUrl(QUrl(self.url))
        request.setRawHeader(
            'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0')
        # web.load(QUrl(self.url))
        request.setRawHeader("Connection", "keep-alive")
        # request.setRawHeader(
        #"Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        #request.setHeader(request, "application/octet-stream")
        web.load(request)
        self.webpage = web.page()
        self.connect(web, SIGNAL("loadFinished(bool)"), self.save)  # 事件连接

    def input_str(self):
        for line in self.input:
            search_str = line.strip()
            code = u'redblock("' + search_str + '");'
            self.webpage.mainFrame().evaluateJavaScript(code)

    def save(self, finished):
        print 'in save'
        if finished:
            self.webpage.mainFrame().evaluateJavaScript(self.jquery)
            self.webpage.mainFrame().evaluateJavaScript(self.red)
            self.input_str()
            size = self.webpage.mainFrame().contentsSize()
            self.webpage.setViewportSize(QSize(size.width(), size.height()))
            img = QImage(size, QImage.Format_ARGB32)

            painter = QPainter(img)  # 绘图
            self.webpage.mainFrame().render(painter)

            painter.end()
            img.save(self.savename)
            #destPath = self.destDir + self.host + '.png'
            # shutil.copy(self.savename,destPath)
        else:
            print "载入错误，有可能网址错误！输入网址为 " + self.url
        self.close()


def url_check(url):
    import re
    return re.match('https?://', url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
   # print sys.argv
    # print len(sys.argv)

    #task = json.loads()
    task = {}
    #task['model_url'] = 'http://forum.memehk.com/forum.php?mod=forumdisplay&fid=62'
    #task['post_url'] = ['forum.php?mod=viewthread&tid=12185&extra=page%3D1', 'forum.php?mod=viewthread&tid=12185&extra=page%3D1', 'forum.php?mod=viewthread&tid=12185&extra=page%3D1', 'forum.php?mod=viewthread&tid=12184&extra=page%3D1', 'forum.php?mod=viewthread&tid=12184&extra=page%3D1', 'forum.php?mod=viewthread&tid=12184&extra=page%3D1', 'forum.php?mod=viewthread&tid=12183&extra=page%3D1', 'forum.php?mod=viewthread&tid=12183&extra=page%3D1', 'forum.php?mod=viewthread&tid=12183&extra=page%3D1', 'forum.php?mod=viewthread&tid=12182&extra=page%3D1', 'forum.php?mod=viewthread&tid=12182&extra=page%3D1', 'forum.php?mod=viewthread&tid=12182&extra=page%3D1', 'forum.php?mod=viewthread&tid=12181&extra=page%3D1', 'forum.php?mod=viewthread&tid=12181&extra=page%3D1', 'forum.php?mod=viewthread&tid=12181&extra=page%3D1', 'forum.php?mod=viewthread&tid=12180&extra=page%3D1', 'forum.php?mod=viewthread&tid=12180&extra=page%3D1', 'forum.php?mod=viewthread&tid=12180&extra=page%3D1', 'forum.php?mod=viewthread&tid=12179&extra=page%3D1', 'forum.php?mod=viewthread&tid=12179&extra=page%3D1', 'forum.php?mod=viewthread&tid=12179&extra=page%3D1', 'forum.php?mod=viewthread&tid=12178&extra=page%3D1', 'forum.php?mod=viewthread&tid=12178&extra=page%3D1', 'forum.php?mod=viewthread&tid=12178&extra=page%3D1', 'forum.php?mod=viewthread&tid=12177&extra=page%3D1', 'forum.php?mod=viewthread&tid=12177&extra=page%3D1', 'forum.php?mod=viewthread&tid=12177&extra=page%3D1', 'forum.php?mod=viewthread&tid=12176&extra=page%3D1', 'forum.php?mod=viewthread&tid=12176&extra=page%3D1', 'forum.php?mod=viewthread&tid=12176&extra=page%3D1', 'forum.php?mod=viewthread&tid=12175&extra=page%3D1', 'forum.php?mod=viewthread&tid=12175&extra=page%3D1', 'forum.php?mod=viewthread&tid=12175&extra=page%3D1', 'forum.php?mod=viewthread&tid=12174&extra=page%3D1', 'forum.php?mod=viewthread&tid=12174&extra=page%3D1', 'forum.php?mod=viewthread&tid=12174&extra=page%3D1', 'forum.php?mod=viewthread&tid=12173&extra=page%3D1', 'forum.php?mod=viewthread&tid=12173&extra=page%3D1', 'forum.php?mod=viewthread&tid=12173&extra=page%3D1', 'forum.php?mod=viewthread&tid=12172&extra=page%3D1', 'forum.php?mod=viewthread&tid=12172&extra=page%3D1', 'forum.php?mod=viewthread&tid=12172&extra=page%3D1', 'forum.php?mod=viewthread&tid=12171&extra=page%3D1', 'forum.php?mod=viewthread&tid=12171&extra=page%3D1', 'forum.php?mod=viewthread&tid=12171&extra=page%3D1', 'forum.php?mod=viewthread&tid=12170&extra=page%3D1', 'forum.php?mod=viewthread&tid=12170&extra=page%3D1', 'forum.php?mod=viewthread&tid=12170&extra=page%3D1', 'forum.php?mod=viewthread&tid=12169&extra=page%3D1', 'forum.php?mod=viewthread&tid=12169&extra=page%3D1', 'forum.php?mod=viewthread&tid=12169&extra=page%3D1', 'forum.php?mod=viewthread&tid=12168&extra=page%3D1', 'forum.php?mod=viewthread&tid=12168&extra=page%3D1', 'forum.php?mod=viewthread&tid=12168&extra=page%3D1', 'forum.php?mod=viewthread&tid=12167&extra=page%3D1', 'forum.php?mod=viewthread&tid=12167&extra=page%3D1', 'forum.php?mod=viewthread&tid=12167&extra=page%3D1', 'forum.php?mod=viewthread&tid=12166&extra=page%3D1', 'forum.php?mod=viewthread&tid=12166&extra=page%3D1', 'forum.php?mod=viewthread&tid=12166&extra=page%3D1']
    #task['model_url'] = 'http://forum.memehk.com/forum.php?mod=forumdisplay&fid=62'
    # task['post_url'] = ['forum.php?mod=viewthread&tid=187399&extra=page%3D1', 'forum.php?mod=viewthread&tid=187399&extra=page%3D1', 'forum.php?mod=viewthread&tid=187399&extra=page%3D1',
    #'forum.php?mod=viewthread&tid=187391&extra=page%3D1', 'forum.php?mod=viewthread&tid=187391&extra=page%3D1', 'forum.php?mod=viewthread&tid=187391&extra=page%3D1']
    #task['shot_name'] = '1'
    ps = Pagescreen(task)
    # ps.shot()
    sys.exit(app.exec_())  # 启动事件循环
