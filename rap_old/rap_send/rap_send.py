# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import beanstalkc
from pybloom import BloomFilter
import urllib2
import chardet
from lxml import etree
import traceback
from server_base.mysql_handle import MysqlOperate
import cStringIO
import gzip
import time
from format_url import FormatUrl
current_path = sys.path[0]
global Bloom
Bloom = BloomFilter(capacity=100000, error_rate=0.0001)
format_url = FormatUrl()
import socket
socket.setdefaulttimeout(40)
_NUM = 4

class Rap_SendShot():

    def __init__(self):
        self.task_mysql_handle = MysqlOperate('comment', '192.168.8.55',
                                              'root', '123456')
        self.bean = ''
        self.outlog = current_path + '/log/engine_stdout.log'
        self.errlog = current_path + '/log/engine_stderr.log'
        self.req_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                           'Accept-Encoding': 'gzip, deflate, sdch',
                           'Connection': 'keep-alive',
                           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                           }
        self.model_url = []
        self.url_name = {}
        # self.init_log_file()
        self.get_model_url()
        self.init_bloom_filter()
        self.init_beanstalkc()
        self.load_model_url()

    def init_log_file(self):
        if not os.path.isfile(self.outlog):
            f = open(self.outlog, 'w')
            f.close()
        if not os.path.isfile(self.errlog):
            f = open(self.errlog, 'w')
            f.close()

    def get_model_url(self):
        '''
        读取模板url
        '''
        table_name = 'site'
        fields = ['*']
        wheres = {}
        result = self.task_mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'all', 0)
        for one_note in result:
            if one_note['site_name'].find('--') != -1:
                self.model_url.append(one_note['post_url'])
                self.url_name[one_note['post_url']] = one_note['site_name']
        # print self.model_url

    def init_bloom_filter(self):
        global Bloom
        table_name = 'posts'
        fields = ['url']
        wheres = {}
        result = self.task_mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'all', 0)
        for one_note in result:
            Bloom.add(one_note['url'])

    def init_beanstalkc(self):
        self.bean = beanstalkc.Connection('192.168.8.55', 11300)
        self.bean.use('test')

    def bloom_filter(self, tmp_urls, ture_urls):
        global Bloom
        exist_url = []
        for ture_url, tmp_url in zip(ture_urls, tmp_urls):
            if ture_url in Bloom:
                if ture_url not in exist_url:
                    exist_url.append(tmp_url)
        return exist_url

    def load_model_url(self):
       # self.model_url = ['http://forum.vanhi.com/forum-38-1.html']
       # self.model_url =['http://www.wailaike.net/group_post?gid=1']
        global _NUM
        while self.model_url and _NUM>0:
            url = self.model_url.pop(0)
            site_name = self.url_name[url]
            tmp_urls = []
            print url
            try:
                req = urllib2.Request(url, headers=self.req_header)
                content = urllib2.urlopen(req).read()

                encoding = chardet.detect(content)['encoding']
                
                if encoding is None:
                    if content[:6] == b'\x1f\x8b\x08\x00\x00\x00':
                        content = gzip.GzipFile(
                            fileobj=cStringIO.StringIO(content)).read()
                        encoding = chardet.detect(content)['encoding']
                        content = content.decode(
                            encoding, 'ignore')
                if encoding != 'utf-8':
                    content = content.decode(encoding, 'ignore')
                
            except Exception, e:
                print e
                if str(e).find('Connection refused') != -1:
                    print 555
                    self.model_url.append(url)
                    continue
                else:
                    _NUM -=1
                    self.model_url.append(url)
                    continue

            htmlSource = etree.HTML(content)
            web_urls = htmlSource.xpath(u'//a/@href')
            ture_urls, web_urls= format_url.match_url(url, web_urls)
            exist_url = self.bloom_filter(web_urls, ture_urls)
            print url, exist_url
            if exist_url:
                self.send_task(url, exist_url, site_name)

    def send_task(self, model_url, post_url, site_name):
        data = {
            'method':   'manual',
            'model_url': model_url,
            'post_url':  post_url,
            'shot_name': unicode(site_name)

        }
        job_body = json.dumps(data)
        self.bean.put(job_body)


if __name__ == '__main__':
    r = Rap_SendShot()
