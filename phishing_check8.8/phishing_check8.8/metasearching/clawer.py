# encoding:utf8

from lxml import etree
from time import sleep
from random import random
from mechanize import Link
import sys


class Clawer():

    '''
    clawer英文原意是，爪、钳
    br:浏览器；engine:引擎；conf:配置文件；breakpoint ; ready: ;
    next_url: 下一条URL; engine_name : 搜索引擎名字; key: 关键字;
    '''

    def __init__(self, browser, engine, conf, breakpoint=False):
        self.br = browser
        self.engine = engine
        self.ready = True
        self.next_url = ''
        self.conf = conf
        self.engine_name = self.engine.__class__.__name__
        self.key = ''
        # print "breakpoint", breakpoint
        self.breakpoint = breakpoint

    '''
    加载运行信息文件
    '''

    def load_runinfo(self):
        try:
            with open(self.runinfo_dir) as f:
                pass
        except Exception:
            pass

    '''
    
    '''

    def new_search(self):
        self.br.open(self.engine.host)
        self.engine.fill_form(self.br, self.key)
        self.br.submit()

    def continue_search(self):
        # print 'continue_search'
        self.br.open(self.engine.host)
        sleep(self.engine.sleep_time)
        link = self.conf.get(self.engine_name, self.key)
        exec_str = 'link = %s' % link
        exec(exec_str)
        self.br.follow_link(link)

    def search(self, key):
        '''
        #一次返回一页记录
        '''
        self.key = key
        max_num = self.engine.max_num
        sleep_time = self.engine.sleep_time

        if self.breakpoint and self.conf.has_option(self.engine_name, key):
            self.continue_search()
        else:
            self.new_search()

        page_num = 0
        waite = 0
        html = etree.HTML(self.br.response().read().decode('utf8'))

        self.get_next()

        while(1):
            if waite == 0:
                waite = self.engine.waite
                yield self.engine.parse(html)
                sleep(sleep_time)
                # print self.engine_name,page_num,self.is_enable()
                page_num += 1
                if page_num == max_num or not self.is_enable():
                    self.enable()
                    sys.stdout.write(
                        '%s %s search over, key: %s\n' % (time.ctime(), self.engine_name, key))
                    raise StopIteration()
                else:
                    self.next_page()
                    self.get_next()
                    html = etree.HTML(self.br.response().read().decode('utf8'))

            else:
                yield []
                sleep(sleep_time)
                waite -= 1

    def get_next(self):
        try:
            self.engine.next(self, self.br)
            self.conf.set(self.engine_name, self.key, self.next_url)
            # print self.engine_name,"next url=",self.next_url
        except Exception, e:
            self.disable()

    def disable(self):
        self.ready = False

    def enable(self):
        self.ready = True

    def is_enable(self):
        return self.ready

    def next_page(self):
        self.br.follow_link(self.next_url)

if __name__ == '__main__':
    print 'a'
