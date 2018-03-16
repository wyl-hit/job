#-*- coding:utf-8 -*-
import sys
import time
from PyQt4 import QtGui, QtCore, QtWebKit
import multiprocessing


class PageShot(QtGui.QWidget):

    '''
    使用PyQt4的QtWebKit对整个网页截图
    url: wait to shot url
    save_path: save abs path
    img_type: save name = img_type + '.jpeg'
    '''

    def __init__(self, url, save_path, img_type, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.url = url
        self.save_path = save_path
        self.img_type = img_type

    def shot(self):
        webView = QtWebKit.QWebView(self)
        webView.load(QtCore.QUrl(self.url))
        self.webPage = webView.page()
        self.connect(
            webView, QtCore.SIGNAL("loadFinished(bool)"), self.savePage)

    def savePage(self, finished):
        if finished:
            size = self.webPage.mainFrame().contentsSize()
            #print u"页面宽：%d,页面高：%d" % (size.width(), size.height())
            self.webPage.setViewportSize(
                QtCore.QSize(size.width() + 16, size.height()))
            img = QtGui.QImage(size, QtGui.QImage.Format_ARGB32)
            painter = QtGui.QPainter(img)
            self.webPage.mainFrame().render(painter)
            painter.end()
            fileName = self.save_path + '/' + self.img_type + '.jpeg'
            if not img.save(fileName):
                sys.stderr.write('%s  PageShot error to save img: %s\n' %
                                 (time.ctime(), self.url))
            with open(self.save_path + '/shot_over_sign', 'w') as fp:
                fp.write('1')
        else:
            sys.stderr.write('%s  PageShot error to load html: %s\n' %
                             (time.ctime(), self.url))
        self.close()


class CallPageShot(multiprocessing.Process):

    '''
    call PageShot in new process
    '''

    def __init__(self, url, save_path, img_type):
        super(CallPageShot, self).__init__()
        self.url = url
        self.save_path = save_path
        self.img_type = img_type

    def run(self):
        app = QtGui.QApplication(sys.argv)
        # shotter = PageShotter("http://www.adssfwewfdsfdsf.com")
        shotter = PageShot(self.url, self.save_path, self.img_type)
        shotter.shot()
        sys.exit(app.exec_())

if __name__ == "__main__":
    url = '/home/zxy/phishing_check/web_info/gray_web/www.shxxytz66.com/d568be9d/ade5877c/2591943b/394d6ee5/2015-07-17 15:18/main.html'
    save_path = '/home/zxy/phishing_check/web_info/gray_web/www.shxxytz66.com/d568be9d/ade5877c/2591943b/394d6ee5/2015-07-17 15:18'
    a = CallPageShot(url, save_path, img_type='webpage')
    a.start()
