# encoding:utf8
#import hashlib
# import sys
import chardet
import os
import time
import re
from urllib import splittype, splithost, splitport
from lxml import etree
from os.path import join as pjoin
from getkeyword import extract_html
from urlparse import urlparse
from cookielib import CookieJar
from twisted.internet import reactor
# Gzip压缩、及重定向跳转
from twisted.web.client import Agent, CookieAgent, HTTPConnectionPool, \
    ContentDecoderAgent, GzipDecoder, RedirectAgent
from twisted.web.http_headers import Headers
from twisted.internet.ssl import ClientContextFactory

_PATH = os.path.abspath('..')  # _PATH 当前工作路径的上一级目录 phishing/ #phishing/ 级目录
# sys.path.append('../server_base')
from web_save_path import WebSavePath


class WebClientContextFactory(ClientContextFactory):

    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)


class Client():

    def __init__(self):
        self.pool = HTTPConnectionPool(reactor, persistent=True)
        self.pool.maxPersistentPerHost = 5  # 默认一个IP最大保持两个链接
        self.pool.cachedConnectionTimeout = 50  # 默认240秒
        contextFactory = WebClientContextFactory()
        raw_agent = Agent(reactor, contextFactory, pool=self.pool)
        agent = RedirectAgent(
            ContentDecoderAgent(raw_agent, [('gzip', GzipDecoder)]))
        self.cookieJar = CookieJar()
        self.agent = CookieAgent(agent, self.cookieJar)
        self.headers = {'User-agent': ['Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'],
                        'Accept-Language': ['zh-Hans-CN,zh-Hans;q=0.5'],
                        'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'],
                        'Accept-Encoding': ['gb2313,utf-8;q=0.7,*;q=0.7'],
                        'Cache-Control': ['max-age=0']}

    def getpage(self, url, headers={}):
        headers.update(self.headers)
        return self.agent.request('GET', url, Headers(headers), None)

_CSSIMGURLRE = r'url\((.*?)\)'


def format_filename(url):
    fn = url.split('/')[-1]
    fn = fn.replace('"', '')
    fn = fn.split('?')[0]
    return fn

#_FC 输入为 路径，url列表。输出为 [[url,path,路径文件名]]
_FC = lambda path, url_list: [
    [url, path, format_filename(url[0])] for url in url_list]


def save_to_file(content, path, filename):
    # content 内容 path 目录 filename 文件名
    path = os.path.join(_PATH, path)
    if not(os.path.isdir(path) or os.path.isfile(path)):
        os.makedirs(path)
    if content is not None:
        try:
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(content)
        except:
            pass


class ExtractUrl():

    def __init__(self, page_url):
        self.page_url = page_url
        self.link = ''

    def set_response(self, body):
        self.html = body
        char = chardet.detect(body)['encoding']
        self.page = etree.HTML(body.decode(char, 'ignore'))

    def get_url(self):
        url = self.page.xpath('/html/body/div/div/div/div/div/b/text()')
        return url


class HtmlStruct():

    def __init__(self, url_type_list, mongo_operate):
        # 例：url="http://www.outofmemory.cn/11/12.htm"
        self.url = url_type_list[0]
        self.url_type = url_type_list[1]
        self.parts = urlparse(self.url)
        self.host = self.parts.netloc
        # u_pro: "http"  u_s1: "www.outofmemory.cn/11/12.htm"
        self.u_pro, u_s1 = splittype(self.url)
        # u_host: "www.outofmemory.cn"   u_path: "/11/12.htm"
        self.u_host, self.u_path = splithost(u_s1)
        if self.u_host is None:
            return None
        self.u_host, port = splitport(self.u_host)
        # 获取到 "http://www.outofmemory.cn"
        self.u_phost = self.u_pro + '://' + self.u_host
        # self.url_md5 = self.get_folder_name_split(url)
        self.gray_create_time = str(
            time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))
        # Web_save_base类获取url保存的路径和MD5值
        self.web_save_path = WebSavePath()
        self.upath, self.identity_list = self.web_save_path.get_file_save_path(
            self.url, self.url_type)
        # self.s_path 格式为 域名路径/md5/时间戳
        self.s_path = self.upath + '/' + self.gray_create_time
        # 初始化 extract_html类，获取title和keyword 写入数据库
        self.parse_web_text = extract_html(mongo_operate)
        self.css_path = 'css'
        self.js_path = 'js'
        self.html_path = 'html'
        self.pic_path = 'pic'
        # 保存数据的根目录  格式为: ...web_save/web_info
        self.r_path = pjoin(_PATH, 'web_info')
        # 域名路径层的文件目录   格式为: 工作路径/web_info/域名路径/md5
        self.upath = pjoin(self.r_path, self.upath)
        self.headers = {}
        self.total_list = []

    def format_css_url(self, path, url):
        url = url.replace('\\', '')
        url = url.replace('"', '')
        url = url.replace("'", '')
        url = url.strip()
        if url.find('http') != 0:
            if url.find('/') == 0 or url.find('./') == 0:
                url = url[url.find('/') + 1:]
                if path.find('./') == 0:
                    return url
                else:
                    path = path[0:path.rfind('/')]
                    url = path + '/' + url
            elif url.find('../') == 0:
                if url.find('www.') != -1:
                    url = url[url.find('www.'):]
                    return url
                else:
                    num = url.count('../')
                    path_list = path.split('/')
                    path_list = path_list[0:len(path_list) - num - 1]
                    if len(path_list) > 0:
                        path = '/'.join(path_list)
                        url = path + '/' + url[num * 3:]
                    else:
                        path = ''
                        url = path + url[num * 3:]
            else:
                index = path.rfind('/')
                path = path[:index]
                url = pjoin(path, url).replace('\\', '/')
        return url

    def set_response(self, body):
        char = chardet.detect(body)['encoding']
        self.char = char
        body = body.decode(char, 'ignore')
        self.html = body
        # 由于网页的编码可能不是utf-8因此需要分析并进行转换
        self.page = etree.HTML(body)
        self.get_urllist()

    def add_pic(self, css_body, path, filename):
        '''使用正则匹配css文件中的url，添加到pic_list中，修改css文件中的路径，如此的话，此次下载的css文件需要修该url中的路径
            完成对list的修改'''
        css_url = []
        css_pic_format = []
        char_css = chardet.detect(css_body)['encoding']
        css_pic = re.findall(
            _CSSIMGURLRE, css_body.decode(char_css, 'ignore').encode('utf8'), re.S)
        for i in css_pic:
            if i and i.find('data:') != 0:
                css_pic_format.append([])
                re_url = self.format_css_url(path, i)
                css_pic_format[-1] = (self.format_url(re_url), i)
        css_url = _FC(
            (pjoin(self.r_path, self.s_path, self.css_path), self.css_path), css_pic_format)
        for url in css_url:
            css_body = css_body.replace(url[0][1], url[2].replace('\\', '/'))

        css_path = pjoin(pjoin(self.r_path, self.s_path), 'css')
        save_to_file(css_body, css_path, filename)
        return css_url

    def get_urllist(self):
        css_list = self.page.xpath('//*/link[@rel="stylesheet"]/@href')
        js_list = self.page.xpath('//*/script/@src')
        pic_list = self.page.xpath('//*/link[@rel="shortcut icon"]/@href')
        pic_list += self.page.xpath('//*/link[@rel="Shortcut Icon"]/@href')
        pic_list += self.page.xpath('//*/link[@rel="icon"]/@href')
        pic_list += re.findall(_CSSIMGURLRE, self.html, re.S)
        pic_list += self.page.xpath('//img/@original')
        pic_list += self.page.xpath('//img/@src')
        pic_list += self.page.xpath('//div/@src')
        pic_list += self.page.xpath('//input/@src')
        pic_list += self.page.xpath('//*/@background')
        html_list = self.page.xpath('//iframe/@src')
        html_list += self.page.xpath('//frame/@src')
        html_list = list(set(html_list))
        pic_list = list(set(pic_list))
        css_list = list(set(css_list))
        js_list = list(set(js_list))
        fc = lambda url_list: [(self.format_url(url).replace(
            '\\', '/'), url) for url in url_list if url and url.find('data:') != 0]
        self.pic_list = fc(pic_list)
        self.css_list = fc(css_list)
        self.html_list = fc(html_list)
        self.css_list = _FC(
            (pjoin(self.r_path, self.s_path, self.css_path), self.css_path), self.css_list)
        self.js_list = fc(js_list)

    def format_url(self, url):
        url = url.replace('\\', '')
        url = url.replace("'", '')
        url = url.replace('"', '')
        url = url.strip()
        if url.find('//') == 0:
            return self.u_pro + ':' + url
        if url.find('www.') == 0:
            return self.u_pro + '://' + url
        if url.find('http') != 0:
            if url.find('./') == 0:
                r_url = url[url.find('/') + 1:]
                path = os.path.join(
                    self.u_path[0:self.u_path.rfind('/')], r_url).replace('\\', '/')
            elif url.find('../') == 0:
                u_path = '/'.join(self.u_path.split('/')[:-2])
                r_url = url[url.find('/') + 1:]
                path = os.path.join(u_path, r_url).replace('\\', '/')
            elif url.find('/') == 0:
                path = url
            else:
                path = os.path.join(
                    self.u_path[0:self.u_path.rfind('/') + 1], url).replace('\\', '/')
            if path:
                if path[0] == '.':
                    path = os.path.join(self.url, path[path.find('/'):])
                if path[0] != '/':
                    return self.u_phost + '/' + path
            return self.u_phost + path
        return url

    def store(self):
        dl_list = []
        dl_list += _FC((pjoin(self.r_path, self.s_path,
                              self.pic_path), self.pic_path), self.pic_list)
        dl_list += _FC((pjoin(self.r_path, self.s_path,
                              self.js_path), self.js_path), self.js_list)
        dl_list += _FC((pjoin(self.r_path, self.s_path,
                              self.html_path), self.html_path), self.html_list)
        self.total_list += dl_list
        dl_list += self.css_list
        self.dl_list = dl_list
        for dl in dl_list:
            if dl[0][1] != ' ':
                self.html = self.html.replace(
                    dl[0][1], pjoin(dl[1][1], dl[2]).replace('\\', '/'))
        self.html = self.html.replace("base href", "cc")
        self.html = self.html.encode('utf-8', 'ignore')
        # print 'call back all url', self.url
        # s_path 格式为: 当前工作目录/web/域名/时间戳/
        s_path = pjoin(self.r_path, self.s_path)

        now_web_info = self.parse_web_text.get_keyword(self.html)
        print 'now_web_info', now_web_info  

        if self.identity_list is not None:
            if self.identity_list[0] == now_web_info[0] or self.identity_list[1] == now_web_info[1]:
                return 0, self.url, self.url_type
        # print 'call back not saved, wait save url', self.url
        save_to_file(self.html, s_path, 'main.html')
        with open(pjoin(s_path, 'url'), 'wb') as f:
            f.write(self.url)
        # 将title和关键字从网页中抽取出存入mongo
        self.parse_web_text.save_info(self.url, s_path, self.url_type)
        return 1, self.url, self.url_type
