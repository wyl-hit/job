# encoding:utf8
import sys
import os
import time
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QUrl, QObject, pyqtSlot, QSize
from PyQt4.QtGui import QImage, QPainter
#import traceback

from web_save_path import WebSavePath
from vtree_parse import VTree


_CURRENT_PATH = sys.path[0]
_CURRENT_URL = ''  # current crawler url
# current crawler url type: protected, gray, counterfeit
_CURRENT_URL_TYPE = ''
_CURRENT_TIME_PATH = ''  # current url time stamp saved path
_CRAWLER_NUM = 0  # current crawler num
# save crawler url, use to interrupt restart
_LIVE_LOG_PATH = '/tmp/qt_crawler_live'
_LOCAL_TIME = ''

try:
    if not os.path.exists(_LIVE_LOG_PATH):
        os.mkdir(_LIVE_LOG_PATH)
except Exception, e:
    print '%s\n' % e

reload(sys)
sys.setdefaultencoding("utf-8")


class PythonJavascript(QObject):

    '''
    call javascript analysis render result, and save it
    '''

    def __init__(self, browser, mongo_operate, update_running_state, mysql_handle):
        super(PythonJavascript, self).__init__()
        self.update_running_state = update_running_state

        global _CURRENT_PATH
        global _LIVE_LOG_PATH
        self.current_path = _CURRENT_PATH
        self.live_log_path = _LIVE_LOG_PATH
        self.mongo_operate = mongo_operate
        self.vtree = VTree(mongo_operate)
        self.br = browser
        self.mysql_handle = mysql_handle
        # self.ofile = open('m_print','wb')

    @pyqtSlot('QString')
    def m_print(self, name):
        pass
        # self.ofile.write('m_print: '+name+'\n')

    @pyqtSlot('int', 'QString', 'int', 'int', 'int', 'int', 'QWebElement', result='int')
    def add_node(self, parent=0, tag='html', top=0, left=0, height=0, width=0, node=None):
        return self.vtree.add_node(parent, str(tag), top, left, height, width, str(node.toPlainText()))

    @pyqtSlot()
    def save(self):
        self.vtree.node_list[0][-1].pop(0)
        # 保存VTree类的对象，用于下一步筛选，此处直接筛选
        self.vtree.select_node()  # 结点筛选
        self.vtree.dump(
            _CURRENT_URL, _CURRENT_URL_TYPE, _CURRENT_TIME_PATH, self.current_path)
        # self.ofile.close()
        self.vtree = VTree(self.mongo_operate)
        with open(self.live_log_path + '/' + str(os.getpid()) + '.txt', 'a+') as f:
            f.write(_CURRENT_URL + '\n')
        global _CRAWLER_NUM
        _CRAWLER_NUM += 1
        self.update_running_state(_CRAWLER_NUM)
        self.br.border_webpage()

        '''if _CURRENT_URL_TYPE != 'gray':
            web_save = self.mongo_operate.url_get_websave(_CURRENT_URL, _CURRENT_URL_TYPE, 'get')
            feature_objectid = web_save.id
            self.mysql_handle.insert_web_feature(_CURRENT_URL, feature_objectid)'''
        self.br.load_url()

    def set_vtree_text(self, text):
        self.vtree.set_page_text(text)


class Browser(QWebView):

    '''
    simulation browser, render URL, parse it dom tree and text and webpage
    '''

    def __init__(self, task_id, get_protected_iter, get_gray_iter,
                 get_counterfeit_iter, get_monitor_iter, mongo_operate,
                 update_running_state, update_finish_state, mysql_handle,
                 run_start_time):
        super(Browser, self).__init__()
        self.task_id = task_id
        self.mongo_operate = mongo_operate
        self.update_running_state = update_running_state
        self.update_finish_state = update_finish_state
        self.get_protected_iter = get_protected_iter
        self.get_gray_iter = get_gray_iter
        self.get_counterfeit_iter = get_counterfeit_iter
        self.get_monitor_iter = get_monitor_iter
        self.mysql_handle = mysql_handle
        self.run_start_time = run_start_time

        global _CURRENT_PATH
        global _LIVE_LOG_PATH
        self.current_path = _CURRENT_PATH
        self.live_log_path = _LIVE_LOG_PATH

        self.web_save_path = WebSavePath()
        self.main_page = self.page()  # QWebPage
        self.main_page.javaScriptAlert = self._alert
        self.main_frame = self.main_page.mainFrame()  # QWebFrame
        # 将本地QT对象QWbebView的信号loadfinished与javascript相连
        # 网页加载完毕后执行load_finished函数
        self.main_frame.loadFinished.connect(
            self.load_finished)
        self.pjs = PythonJavascript(
            self, mongo_operate, update_running_state, mysql_handle)
        # 为保证每次刷新加载页面是都调用addtoJavascriptWindowObject方法
        # 需要与信号javaScriptWindowObjectCleared相连
        self.main_frame.javaScriptWindowObjectCleared.connect(
            self.addpjs)  # 绑定python对象注册
        with open(self.current_path + "/script.js", "r") as f:
            self.script = f.read()

        self.qt_live_path = '/tmp/' + str(task_id) + '_qt_callback.txt'
        self.check_qt_alive = open(self.qt_live_path, 'w')
        self.engine_pid = os.getpid()

        self.load_url()

    def _alert(self, frame, message):
        pass

    def over_handle(self):
        '''
        run over, write to log in tmp
        '''
        with open(self.live_log_path + '/' + str(os.getpid()) + '.txt', 'a+') as f:
            f.write('over')
        sys.stdout.write('parse over!\n')

    def load_url(self):
        '''
        parse once url, first load it
        '''
        global _CURRENT_URL_TYPE
        try:
            url = self.get_protected_iter.next()
            _CURRENT_URL_TYPE = 'protected'
        except StopIteration:
            try:
                url = self.get_gray_iter.next()
                _CURRENT_URL_TYPE = 'gray'
            except StopIteration:
                try:
                    url = self.get_counterfeit_iter.next()
                    _CURRENT_URL_TYPE = 'counterfeit'
                except StopIteration:
                    try:
                        url = self.get_monitor_iter.next()
                        _CURRENT_URL_TYPE = 'monitor'
                    except StopIteration:
                        self.over_handle()
                        global _CRAWLER_NUM
                        run_time = int(time.time() - self.run_start_time)
                        self.update_finish_state(_CRAWLER_NUM, run_time)
                        os.remove(self.qt_live_path)
                        os._exit(0)
        # 将实时运行状态写入防卡死检测文件
        self.check_qt_alive.seek(0)  # 清空文件
        self.check_qt_alive.truncate(0)
        self.check_qt_alive.write(url + ' ' + str(_CRAWLER_NUM) + ' ' + str(self.engine_pid))
        self.check_qt_alive.flush()
        local_html, local_time = self.web_save_path.get_html_path_abs(
            url, _CURRENT_URL_TYPE)
        global _LOCAL_TIME
        _LOCAL_TIME = local_time
        if local_html is None or local_time is None:
            sys.stdout.write(
                'url not be saved: %s, task_id: %d\n' % (url, self.task_id))
            self.load_url()
        else:
            global _CURRENT_URL
            global _CURRENT_TIME_PATH
            _CURRENT_URL = url
            _CURRENT_TIME_PATH = local_time
            #print 'load:', _CURRENT_URL
            self.load(QUrl(local_html))

    def border_webpage(self):
        '''
        get web page border and webpage
        ** this method inaccurate, page will change longer **
        ** give up use **
        '''
        size = self.main_page.mainFrame().contentsSize()
        global _CURRENT_URL
        global _CURRENT_URL_TYPE
        nwe_border_list = [size.width(), size.height()]
        self.mongo_operate.add_web_border(
            _CURRENT_URL, _CURRENT_URL_TYPE, nwe_border_list)
        # print u"页面宽：%d,页面高：%d" % (size.width(), size.height())
        self.main_page.setViewportSize(
            QSize(size.width() + 16, size.height()))
        img = QImage(size, QImage.Format_ARGB32)
        painter = QPainter(img)
        self.main_page.mainFrame().render(painter)
        painter.end()
        global _CURRENT_TIME_PATH
        img_path = _CURRENT_TIME_PATH + '/webpage.jpeg'
        if not img.save(img_path):
            sys.stderr.write('%s  error to save img: %s,  path: %s\n' %
                             (time.ctime(), _CURRENT_URL,
                              _CURRENT_TIME_PATH))

    def load_finished(self, finished):
        '''
        load_url over, save it text and ...
        '''
        #global _CURRENT_URL
        # print 'finished:', finished, _CURRENT_URL
        self.pjs.set_vtree_text(str(self.main_frame.toPlainText()))
        self.main_frame.evaluateJavaScript(self.script)

    def addpjs(self):
        self.main_frame.addToJavaScriptWindowObject(
            "python", self.pjs)  # 向Javascript注册Python对象

if __name__ == '__main__':
    url_list = [['111_vtree', 'http://www.taobao.com/']]
    pb = PageBlock(url_list)
    pb.stop()
