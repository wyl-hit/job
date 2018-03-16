# encoding:utf8
# 实现了对css文件的解析,单个文件解析css文件，然后将所有url下载下来

import os
import sys
import time
import re
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.protocol import Protocol
from twisted.web.client import readBody
#import traceback

from get_web_source import Client, HtmlStruct, save_to_file

_TOTAL = 0  # all send source num
_FINISHED = False
_WAITURL = 0  # wait to save url num


class BeginningPrinter(Protocol):

    def __init__(self, finished):
        self.finished = finished
        self.display = None

    def dataReceived(self, bytes):
        if self.display:
            self.display += bytes
        else:
            self.display = bytes

    def connectionLost(self, reason):
        self.finished.callback(self.display)

clinet = Client()


def decorate(f):  # 定义修饰器
    def call(*args, **kwargs):
        global _TOTAL
        # print _TOTAL
        pid = os.getpid()
        _TOTAL -= 1
        args[0].file_callback.seek(0)  # 清空文件
        args[0].file_callback.truncate(0)
        args[0].file_callback.write(
            str(pid) + '-' + str(_TOTAL) + '-' + str(time.time()))
        args[0].file_callback.flush()
        return f(*args, **kwargs)
    return call


def get_page(url, s=None):  # 封装 getpage函数
    global _TOTAL
    _TOTAL += 1
    if s is None:
        d = clinet.getpage(url)
    else:
        d = clinet.getpage(url, s)
    return d


class WebSave():

    def __init__(self, task_id, protected_urls, get_gray_iter, gray_urls,
                 counterfeit_urls, monitor_urls, url_num,
                 update_running_state, update_finished_state,
                 mongo_operate):
        self.task_id = task_id

        self.protected_urls = protected_urls
        self.get_gray_iter = get_gray_iter
        self.gray_urls = gray_urls
        self.counterfeit_urls = counterfeit_urls
        self.monitor_urls = monitor_urls
        global _WAITURL
        # print 'protected_urls', protected_urls
        # print 'counterfeit_urls', counterfeit_urls
        _WAITURL = url_num
        self.update_running_state = update_running_state
        self.update_finished_state = update_finished_state
        self.mongo_operate = mongo_operate

        # 每次 完成一个网页自加1，>=self.update_num后重置为0
        self.all_request_num = 0   # 已经请求的数量
        self.saved_win_num = 0  # 已经保存的数量
        self.current_request_num = 3  # max meantime request web num
        # save the type of url like :gray,protected...
        self.url_type_list = []
        self.start_run_time = time.time()
        # save struct check log
        self.task_callback_path = '/tmp/' + str(task_id) + '_callback.txt'
        self.file_callback = open(self.task_callback_path, 'w')
        # save already saved url
        self.task_saved_urls_path = '/tmp/' + str(task_id) + '_saved_urls.txt'
        self.file_saved_urls = open(self.task_saved_urls_path, 'w')

    def onePageOver(self, res, url):
        self.downloadFinished()

    @decorate
    def saveResource(self, response, path, filename, url):
        finished = defer.Deferred()
        response.deliverBody(BeginningPrinter(finished))
        finished.addCallbacks(save_to_file, self.parseErr, [path, filename])
        return finished

    def parseBody(self, body, hs):
        print 'in parseBody'
        match = re.search(r"<title>(.*?)</title>", body)
        try:
            title = match.group(1)
        except:
            title = 'None'
        if title.find("Redirect") != -1:
            '''sys.stderr.write(
                '%s  table_name: %s, fields: %s, wheres: %s\n' %
                (time.ctime(), table_name, fields, wheres))'''
            # print 'redirect'
            raise Exception("-1")
        hs.set_response(body)
        flag, url, url_type = hs.store()
        print 'flag', flag, url
        if flag == 0:
            #'发出已存在异常'
            # 抛出 0错误，表示当前网页已经下载且内容没有发生变化
            raise Exception("0")
        else:
            self.file_saved_urls.write(url + ' ' + url_type + '\n')
            self.file_saved_urls.flush()
            self.saved_win_num += 1
            return hs

    def dlResource(self, response, hs):
        for res in response:
            if res[0] and res[1]:
                hs.total_list += res[1]
        if hs.total_list:
            tmp_list = []
            try:
                for pair in hs.total_list:
                     # encode是为了下载含有中文字符的资源
                    tmp_list.append(get_page(pair[0][0].encode('gb2312'),
                                             {'referer': [hs.url]}).addCallbacks(
                        self.saveResource, self.dlErr,
                        callbackArgs=[pair[1][0], pair[2], pair[0][0]],
                        errbackArgs=[pair[0][0]]))
            except:
                sys.stderr.write(
                    '%s  %s\n' % 'WebSave dlResource string index out of range' %
                    (time.ctime(), self.task_id))
                pass

            dl = defer.DeferredList(tmp_list, consumeErrors=True)
            dl.addBoth(self.onePageOver, hs.url)
        else:
            # "once page over"
            self.onePageOver(None, hs.url)

    @decorate
    def dlErr(self, err, path, filename, url):
        print 'dlErr', err, path, filename, url

    @decorate
    def durlErr(self, err, hs, url):
        print err, 'ininin'
        self.downloadFinished()

    def parseErr(self, err):
        # print 'in parseErr'
        self.downloadFinished()

    @decorate
    def cbRequest(self, response, hs, url):
        print 'in cbRequest'
        d = readBody(response)
        d.addCallbacks(self.parseBody, self.parseErr, [hs])
        d.addCallbacks(self.dlCssResource, self.parseErr)  # 添加对css文件资源的处理回调函数
        return d

    def dlCssResource(self, hs):
        # 先下载其中的css文件,===============
        # print 'in dlCssResource'
        try:
            if hs.css_list:
                dl = defer.DeferredList([get_page(pair[0][0],
                                                  {'referer': [hs.url]}).addCallbacks(
                    self.saveCss, self.dlErr, callbackArgs=[
                        pair[0][1], pair[2], hs, pair[0][0]],
                    errbackArgs=[pair[0][0]])
                    for pair in hs.css_list], consumeErrors=True)
                dl.addCallbacks(self.dlResource, self.parseErr, [hs])
            else:
                self.dlResource([], hs)
        except:
            return False
        return hs  # 这里是否需要添加什么，还是可以没有操作？

    @decorate
    def saveCss(self, response, path, filename, hs, url):
        # print 'saveCss'
        finished = defer.Deferred()
        response.deliverBody(BeginningPrinter(finished))
        return finished.addCallbacks(self.parseCss, self.parseErr, [hs, path, filename])

    def parseCss(self, css_body, hs, path, filename):
        list = hs.add_pic(css_body, path, filename)
        return list

    def downloadFinished(self):
        global _TOTAL
        global _WAITURL
        # print 'downloadFinished'
        ulist = []  # ulist  save like [[url,url_type],[],[],]
        self.current_request_num += 1
        self.update_running_state(self.saved_win_num, self.all_request_num)
        if _TOTAL == 0 and _WAITURL == 0:
            run_time = int(time.time() - self.start_run_time)
            # 完成后更新状态
            self.file_saved_urls = open(self.task_saved_urls_path, 'r')
            download_urls = self.file_saved_urls.readlines()
            for line in download_urls:
                line = line[:-1]           # delete '\n'
                ulist.append(line.split(' '))
            self.file_saved_urls.close()
            self.update_finished_state(ulist, run_time, self.all_request_num)
            # 'over 已关闭'
            try:
                reactor.stop()
                self.file_callback.close()
                sys.stdout.write('%s  normal close engine, task_id: %s: \n' %
                                 (time.ctime(), self.task_id))
            except:
                self.file_callback.close()
                sys.stderr.write('%s  again close , task_id: %s: \n' %
                                 (time.ctime(), self.task_id))
            try:
                os.remove(self.task_callback_path)
                os.remove(self.task_saved_urls_path)
            except:
                pass
        else:
            self.download()

    def downloadFinished_err(self, url):
        # update error handle, jump
        pass
        # print "DonwloadFinished_err", url

    def download(self):
        global _WAITURL
        while self.current_request_num > 0:
            try:
                url = self.protected_urls.pop()
                self.url_type_list = [url, 'protected']
            except IndexError:
                try:
                    url = self.counterfeit_urls.pop()
                    self.url_type_list = [url, 'counterfeit']
                except IndexError:
                    try:
                        url = self.monitor_urls.pop()
                        self.url_type_list = [url, 'monitor']
                    except IndexError:
                        try:
                            url = self.gray_urls.pop()
                            self.url_type_list = [url, 'gray']
                        except IndexError:
                            try:
                                url = self.get_gray_iter.next().encode("UTF-8")
                                self.url_type_list = [url, 'gray']
                            except StopIteration:
                                break
            print 'ready download', self.url_type_list
            hs = HtmlStruct(self.url_type_list, self.mongo_operate)
            if hs is False:
                continue
            d = get_page(url)
            self.all_request_num += 1
            # print 'download', url, _WAITURL

            d.addCallbacks(
                self.cbRequest, self.durlErr, callbackArgs=[hs, url], errbackArgs=[hs, url])
            self.current_request_num -= 1
            _WAITURL -= 1


if __name__ == '__main__':
    _DLURL = UrlList(4, '/dev/null', '/dev/null', '172.31.159.248', 'root',
                     '', 'phishing_check', 'test', '172.31.159.248', 27017, 'root', '')
    _DLURL.download()
    reactor.run()
