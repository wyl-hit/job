#!/usr/bin/python
#-*-coding:utf-8-*-
'''
模块功能： 生成网页保存的路径
输入 ： url
接口： get_file_save_path（url） 返回 md5值 和 路径 (格式：web/域名/md5)
       get_html_path（url）      返回 html文件路径和 时间戳路径

'''
import os
import sys
import time
_SAVE_PATH = os.path.abspath('..')    # 获取当前工作路径的上级目录 ...phishing/ 目录
from urlparse import urlparse
from extra_opration import get_hash_path


class WebSavePath():

    def __init__(self):
        pass

    # root_md5_path 路径为 /.../web_save/web/域名/md5
    def get_last_hash(self, root_md5_path, rel_md5_path):
        '''
        根据时间戳文件的顺序排序，获取最新的时间戳文件数据,返回该文件的md5数据，不存在该文件返回None
        '''
        file_list = os.listdir(root_md5_path)
        file_list_new = sorted(file_list)
        if not file_list:  # /md5/路径下没有时间戳文件
            return None
        the_last_file = file_list_new[-1]
        identity_file_path = root_md5_path + '/' + the_last_file + '/id.txt'
        if os.path.isfile(identity_file_path):
            f = open(identity_file_path, 'r')
            identity_data = f.read().split(' ')
            f.close()
            return identity_data
        else:
            return None

    def get_file_save_path(self, url, web_type):
        '''
        获取 网页保存的路径，路径格式 web_save/web/域名/md5
        web_type: 'gray', 'protected', 'counterfeit'
        '''
        if web_type not in ['gray', 'protected', 'counterfeit', 'monitor']:
            sys.stderr.write('%s  web_type error: %s\n' %
                             (time.ctime(), web_type))
            return False
        parts = urlparse(url)
        host = parts.netloc  # 域名
        # url_md5 is like:  89891222/56462214/22344152/88784125
        url_md5 = get_hash_path(url)
        # root_md5_path  路径为 /.../phishing_check/web/域名/md5
        # rel_md5_path  路径为   域名/md5
        root_md5_path = _SAVE_PATH + '/web_info/' + \
            web_type + '_web/' + host + '/' + url_md5
        rel_md5_path = web_type + '_web/' + host + '/' + url_md5
        if os.path.isdir(root_md5_path):
            md5_hash = self.get_last_hash(root_md5_path, rel_md5_path)
        else:
            md5_hash = None
        return rel_md5_path, md5_hash

    def get_time_html_path_rel(self, root_md5_path, rel_md5_path):
        '''
        根据时间戳文件的顺序排序，获取最新的时间戳文件数据,返回该文件的md5数据，不存在该文件返回None
        '''
        file_list = os.listdir(root_md5_path)
        file_list_new = sorted(file_list)
        if not file_list:  # /md5/路径下没有时间戳文件
            return None, None
        the_last_file = file_list_new[-1]
        Relative_time_path = rel_md5_path + '/' + the_last_file
        html_path = root_md5_path + '/' + the_last_file + '/main.html'
        Relative_html_path = rel_md5_path + \
            '/' + the_last_file + '/main.html'
        if os.path.isfile(html_path):
            return Relative_html_path, Relative_time_path
        else:
            return None, None

    def get_html_path_rel(self, url, web_type):
        '''
        获取最后一个时间戳文件的main.html路径 和时间戳路径，没有则返回None
        '''
        parts = urlparse(url)
        host = parts.netloc  # 域名
        url_md5 = get_hash_path(url)
        # root_md5_path  路径为 .../phishing_check/web/域名/md5
        # rel_md5_path  路径为   域名/md5
        root_md5_path = _SAVE_PATH + '/web_info/' + \
            web_type + '_web/' + host + '/' + url_md5
        rel_md5_path = '/web_info/' + web_type + '_web/' + host + '/' + url_md5
        if os.path.isdir(root_md5_path):
            html_path, time_path = self.get_time_html_path_rel(
                root_md5_path, rel_md5_path)
            return html_path, time_path
        else:
            return None, None

    def get_time_html_path_abs(self, root_md5_path):
        '''
        根据时间戳文件的顺序排序，获取最新的时间戳文件数据,返回该文件的md5数据，不存在该文件返回None
        input:
            root_md5_path: root/域名/md5
        output:
            html_path: root/域名 /md5/time/.html
            time_path: root/域名/md5/time/
        '''
        file_list = os.listdir(root_md5_path)
        file_list_new = sorted(file_list)
        the_last_file = file_list_new[-1]
        time_path = root_md5_path + '/' + the_last_file
        html_path = time_path + '/main.html'
        if os.path.isfile(html_path):
            return html_path, time_path
        else:
            return None, None

    def get_html_path_abs(self, url, web_type):
        '''
        获取最后一个时间戳文件的main.html路径 和时间戳路径，没有则返回None
        input:
            url
        output:
            html_path: root/域名/md5/time/.html
            time_path: root/域名/md5/time/
        '''
        parts = urlparse(url)
        host = parts.netloc  # 域名
        url_md5 = get_hash_path(url)
        # root_md5_path  路径为 .../phishing_check/web/域名/md5
        root_md5_path = _SAVE_PATH + '/web_info/' + \
            web_type + '_web/' + host + '/' + url_md5
        if os.path.isdir(root_md5_path):
            html_path, time_path = self.get_time_html_path_abs(
                root_md5_path)
            return html_path, time_path
        else:
            return None, None  # 2015-05-24 13_04

    def get_transfer_path(self, url, web_type, target_type):
        '''
        获得网页信息转移的源路径和目标路径
        '''
        parts = urlparse(url)
        host = parts.netloc  # 域名
        source_file_path = _SAVE_PATH + '/web_info/' + \
            web_type + '_web/' + host
        target_file_path = _SAVE_PATH + '/web_info/' + \
            target_type + '_web/' + host
        return source_file_path, target_file_path


if __name__ == '__main__':
    h = WebSavePath()
    print h.get_html_path_rel('http://www.sina.cn/', 'gray')
    # print h.get_html_path_abs('http://www.sina.com/','protected')
