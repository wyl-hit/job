#!/usr/bin/python
#-*-coding:utf-8-*-
'''
extra_opration
'''

import hashlib
import os
from socket import gethostbyname
import shutil
import sys
import time
import traceback


def hash_md5(date):
    '''
    对给定数据进行MD5哈希，返回十六进制数
    '''
    md5 = hashlib.md5()
    while True:
        temp = date[:2048]
        if temp == '':
            break
        else:
            md5.update(temp)
            date = date[2048:]
    return md5.hexdigest()


def get_hash_path(url, layer_num=8):
    '''
    存取url经md5后的列表
    '''
    md5_path = ''
    url_md5 = hash_md5(url)
    for i in range(len(url_md5) / layer_num):
        if md5_path == '':
            md5_path = url_md5[0:layer_num]
            url_md5 = url_md5[layer_num:]
        else:
            md5_path = md5_path + '/' + url_md5[0:layer_num]
            url_md5 = url_md5[layer_num:]
    return md5_path


def exist_url_wipe_repeat(root_path, url_list):
    '''
    基于Hash目录树的URL去重，对变换后存在的域名去重
    接收URL列表，输出不存在的URL列表
    '''
    url_exist_list = []  # 储存hash目录树中不存在的url
    for url in url_list:
        # md5_path is like adcf4789/aedcb874/.../...
        hash_path = get_hash_path(url)
        folder_list = hash_path.split('/')
        exist_flag = 1
        current_path = root_path  # 去重根路径
        for folder_name in folder_list:
            current_path = current_path + '/' + folder_name
            if os.path.exists(current_path):
                continue
            else:
                os.mkdir(current_path)
                exist_flag = 0  # 目录不存在 标志位置为零
        if exist_flag == 0:
            url_exist_list.append(url)
    return url_exist_list


def dns_check(url):
    '''
    探测URL的IP
    '''
    if url.find("//") != -1:
        url = url[url.find("//") + 2:]
    if url[-1] == '/':
        url = url[:-1]
    try:
        ip = gethostbyname(url)
    except:
        ip = ''
    return ip


def update_frequency(div_num, dived_num, min_num, max_num):
    '''
    engine run update to task_result frequency
    '''
    frequency = int((div_num + dived_num - 1) / dived_num)
    if frequency > max_num:
        frequency = max_num
    elif frequency < min_num:
        frequency = min_num
    return frequency


def web_info_transfer(source_file_path, target_file_path):
    try:
        if os.path.isdir(source_file_path):
            shutil.copytree(source_file_path, target_file_path)
        elif os.path.isfile(source_file_path):
            shutil.copyfile(
                source_file_path, target_file_path)
        else:
            sys.stderr.write(
                '%s  web_info_transfer, source_file_path no exist: %s\n' % (time.ctime(), source_file_path))
            return False
    except OSError:
        sys.stderr.write(
            '%s  web_info_transfer, target_file_path already exists: %s\n' % (time.ctime(), source_file_path))
    except:
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print dns_check('http://www.sina.com/')
    web_info_transfer('http://www.sina.com/', 'protected', 'gray')
    pass
