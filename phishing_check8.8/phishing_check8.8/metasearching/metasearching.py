# encoding:utf8
import os
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import sys
import mechanize
import cookielib
from clawer import *
import engine
import time
import ConfigParser
import codecs
import warnings
warnings.filterwarnings("ignore")


class UnicodeStreamFilter:

    def __init__(self, target):
        self.target = target
        self.encoding = 'utf-8'
        self.errors = 'replace'
        self.encode_to = self.target.encoding

    def write(self, s):
        if type(s) == str:
            s = s.decode("utf-8")
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)
        self.target.write(s)

if sys.stdout.encoding == 'cp936':
    sys.stdout = UnicodeStreamFilter(sys.stdout)


def Debug(*argv):
    for a in argv:
        print a,
    print ''


class RunInfo():

    def __init__(self, keyworld, page=0, num=0):
        self.keyworld = keyworld
        self.page = page
        self.num = num

    def __str__(self):
        return '[%s,%s,%s]' % (self.keyworld, self.page, self.num)

# 元搜索主函数


class Metasearching():

    '''
    # 变量总结：br: 浏览器； cj: cookies; error_list: 错误列表
    #           breakpoint：断点； engine_list：搜索引擎列表
    #           keys_list：关键字列表；keys_list：引擎集合；key_iter：遍历引擎集合
    #           result_list：检索结果；engine: ; E:
    #           
    # 初始化函数
    '''

    def __init__(self, keys_list, mongo_operate, objectID, linkinfo_file,
                 numinfo_file, work_path, update_running_state, breakpoint=False):
        self.keys_list = keys_list
        self.mongo_operate = mongo_operate
        self.objectID = objectID
        self.linkinfo_file = linkinfo_file
        self.numinfo_file = numinfo_file
        self.work_path = work_path
        self.update_running_state = update_running_state
        self.begin_time = time.time()
        self.link_runinfo = ConfigParser.ConfigParser()
        self.num_runinfo = ConfigParser.ConfigParser()
        self.set_br()
        self.set_sql()
        # 设置配置文件
        self.set_conf_file()
        self.breakpoint = breakpoint

        self.bind()

    # 设置浏览器
    def set_br(self):
        br = mechanize.Browser()
        # cookiejar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        self.error_list = []
        # options
        br.set_handle_equiv(True)
        try:
            br.set_handle_gzip(True)
        except:
            pass
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(
            mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                         ('Accept-Language', 'zh-Hans-CN,zh-Hans;q=0.5')]
        self.br = br

    # 设置数据库
    def set_sql(self):
        pass

    # 设置输出数量和引擎的配置文件
    def set_conf_file(self):

        self.link_runinfo.read(self.linkinfo_file)
        self.num_runinfo.read(self.numinfo_file)

    # 此处用到了Clawer
    # 添加搜索引擎
    def bind(self):
        self.engine_list = []
        for mo in dir(engine):
            # 这是什么函数
            E = getattr(engine, mo)
            #Debug('bind type(C) =',type(C))
            if str(type(E)) == "<type 'classobj'>" and E.__name__ != 'Base':
                e = E()
                # print e.__class__.__name__
                if e.ready:
                    self.engine_list.append(
                        Clawer(self.br, e, self.link_runinfo, self.breakpoint))
                    if e.__class__.__name__ not in self.link_runinfo.sections():
                        self.link_runinfo.add_section(e.__class__.__name__)
                    if e.__class__.__name__ not in self.num_runinfo.sections():
                        self.num_runinfo.add_section(e.__class__.__name__)

    # 开始检索-获取关键字
    def start_search(self):
        #self.keys_list = []
        # print 'start - key'
        # for key in self.keys_list:
            # print key

        # print 'end - key'
        self.search()

    # 检索
    def search(self):
        key_iter = []

        search_kword_num = 0
        search_url_num = 0
        for key in self.keys_list:
                    # 输出HTML文件

            search_kword_num = search_kword_num + 1
            if os.path.isdir(self.work_path + '/result'):
                pass
            else:
                os.mkdir(self.work_path + '/result')

            if self.breakpoint:
                filename = self.work_path + \
                    '/result/%s-%s.html' % ((sys.argv[1]
                                             ).decode('utf8'), key.decode('utf8'))
            else:
                filename = self.work_path + \
                    '/result/%s.html' % (key.decode('utf8'))

            # 写文件
            with codecs.open(filename, 'wb', "utf-8") as f:
                f.write(unicode(
                    '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body>'))
                self.br.set_cookiejar(cookielib.LWPCookieJar())

                for engine in self.engine_list:
                    engine_name = engine.engine.__class__.__name__

                    if self.breakpoint and self.num_runinfo.has_option(engine_name, key):
                        ri = RunInfo(
                            key, num=int(self.num_runinfo.get(engine_name, key)))
                    else:
                        ri = RunInfo(key)
                    key_iter.append([engine_name, engine.search(key), ri])

                while key_iter != []:
                    for k_iter in key_iter:
                        self.exist_list = []

                        try:
                            k_iter[2].page += 1
                            # next函数相当重要
                            result_list = next(k_iter[1])

                        except StopIteration:
                            # print 'remove ',k_iter[0]
                            key_iter.remove(k_iter)
                            for k_iter in key_iter:
                                print "      ", k_iter[0]
                            continue

                        except Exception, e:
                            # print k_iter[0],'error'
                            # print e
                            self.error_list.append([e, k_iter[0], k_iter[2]])
                            key_iter.remove(k_iter)
                            continue

                        if result_list:
                            # print "============================"
                            # print "key:",key,'engine:',k_iter[0]
                            # print "***************************"
                            f.write(
                                ('<p>============================</p>\n<p>key:%s  engine:%s</p>\n<p>****************************</p>\n' % (key, k_iter[0])).decode('utf8'))
                            for result in result_list:
                                k_iter[2].num += 1
                                result['engine'] = k_iter[0]
                                result['num'] = k_iter[2].num
                                result['key'] = key
                                result['time_now'] = time.strftime(
                                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                                # print
                                # result['num'],result['title']#,result['url']
                                self.exist_list.append(result['url'])
                                f.write(unicode('<p>%s %s <a href="%s" target="_blank">%s</a></p>\n' % (
                                    result['time_now'], result['num'], result['url'], result['title'])))
                            self.num_runinfo.set(k_iter[0], key, k_iter[2].num)
                            # 什么是nif，什么是rif
                            with open(self.numinfo_file, 'wb') as nif:
                                self.num_runinfo.write(nif)
                            with open(self.linkinfo_file, 'wb') as rif:
                                self.link_runinfo.write(rif)
                            # print "============================"
                            f.write('<p>============================</p>\n')

                            # 更新URL长度
                            search_url_num = search_url_num + \
                                len(self.exist_list)
                            '''
                            存储mongo数据库
                            '''
                            # print '///////////////////////'
                            # print  self.exist_list
                            # print '//////////////////////////'
                            try:
                                self.mongo_operate.add_gray_list(
                                    self.exist_list, self.objectID)
                            except Exception, e:
                                sys.stderr.write(
                                    '%s\n' % MongoError(e, 'meta_run add gray'))
                                sys.stderr.write(
                                    ' task_id: %s\n' % self.task_id)
                            # print
                            # '---------------------seccess###################################'

                            self.update_running_state(
                                search_url_num, search_kword_num)

                f.write('</body></html>')


if __name__ == '__main__':
    print len(sys.argv)
    # 获取参数
    if len(sys.argv) > 1:
        m = Metasearching(True)
    else:
        numinfo_file = './runinfo/link_info.ini'
        runinfo_file = './runinfo/num_info.ini'
        with open(numinfo_file, 'wb') as f:
            pass
        with open(runinfo_file, 'wb') as f:
            pass
        m = Metasearching()
        # 开始检索
    m.start_search()
    # 打印错误
    for error in m.error_list:
        print "~~~~~~~~~~~~~~~~~~~~~~~"
        print error[0]
        print error[1]
        print error[2]
        # 结束打印
    print 'over!'
