#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import chardet
import warnings
warnings.filterwarnings('ignore', '.*', Warning, 'chardet')
from lxml import etree
from os.path import join as pjoin
from web_save_path import WebSavePath
from jeba_call import *
#father_path = os.path.abspath('..')
#sys.path.append(father_path + '/server_base')
'''
模块任务: 保存网页title和关键字到数据库
输入：    网页url,网页内容 html
输出：    将title、keyword 写入数据库
'''


class extract_html():

    def __init__(self, mongo_operate=None):
        self.mongo_operate = mongo_operate
        self.web_save_path = WebSavePath()
        self.title = ''
        self.keyword = ''
        self.Html = ''
        self.url = ''
        self.div_num = 0
        # pass

    def write_mongo(self, goal_url, title, text, url_type):
        self.mongo_operate.add_web_title(goal_url, url_type, title)
        self.mongo_operate.add_web_text(goal_url, url_type, text)

    def get_html_file(self, url, url_type):
        html_path, time_path = self.web_save_path.get_html_path_abs(
            url, url_type)
        if html_path is None or time_path is None:
            return False
        # print html_path
        f = open(html_path, 'r')
        self.Html = f.read()

    def get_keyword(self, Html=None):
        '''
        获取 title keyword, div num
        '''
        if Html is None:
            Html = self.Html
        # Html=file('main.html').read()
        char = chardet.detect(Html)['encoding']
        page = etree.HTML(Html.decode(char, 'ignore'))
        title = page.xpath('/html/head/title/text()')
        self.title = title[0].strip()

        match = re.findall(r"<div.*?>(.*?)</div>", Html)
        self.div_num = len(match)   # get the <div> number

        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        s = re_cdata.sub('', Html)
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        s = re_br.sub('\n', Html)
        blank_line = re.compile('\n+')  # 去掉多余的空行
        s = blank_line.sub('', s)
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_comment.sub('', s)  # 去掉HTML注释
        re_style = re.compile('<style\s*[^>]*>(.*?)</style\s*>')  # style
        s = re_style.sub('', s)
        re_script = re.compile('<script\s*[^>]*>(.*?)</script>')
        s = re_script.sub('', s)
        re_h = re.compile('</?[^>]*>')  # 处理html标签
        s = re_h.sub('', s)
        s = replaceCharEntity(s)  # 替换实体
        s = s.replace(" ", "")
        cut_web_text = cut_all(s)
        self.keyword = get_keyword(cut_web_text)
        if chardet.detect(self.title)['encoding'] == 'GB2312':
            self.title = unicode(self.title, "gb2312").encode('utf-8')
        if chardet.detect(self.keyword)['encoding'] == 'GB2312':
            self.keyword = unicode(self.keyword, "gb2312").encode('utf-8')
        return [self.div_num, self.keyword, self.title]

    def save_info(self, url, path, url_type):
        with open(pjoin(path, 'id.txt'), 'wb') as f:  # 存取文件
            f.write(str(self.div_num) + ' ' + self.keyword)
        f.close()
        self.write_mongo(url, self.title, self.keyword, url_type)  # 写入数据库


def replaceCharEntity(htmlstr):
    # 替换常用HTML字符实体.
    # 使用正常的字符替换HTML中特殊的字符实体.
    # htmlstr HTML字符串.
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        # entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr

if __name__ == '__main__':

    h = extract_html()
    #h.get_html_file('http://www.sina.com/', 'protected')
    with open('main.html') as f:
        html = f.read()
    # print html
    a = h.get_keyword(html)
    for i in a:
        print i
