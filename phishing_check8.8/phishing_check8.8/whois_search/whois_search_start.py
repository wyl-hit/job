#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    模块任务： 根据config中定义的规则将被保护url名单生成url灰名单，并使用twisted对这些url进行存在性检测
    输入：
        URL灰名单列表，格式：[被保护url(个数1),域名变化的url(个数1)，路径变化的url(个数n)]
    输出：
        存在的url灰名单列表
    存在的问题：
        url重定向问题，不存在的url会根据当前网络运行商的不同，定位到不同界面  #去重保存路径，为绝对路径
'''
import os
import time
import sys
import multiprocessing
import traceback

from mongo_handle import Mongo_Operate
from whois_reverse import WhoisReverse
from mysql_handle import MysqlOperate
from whois.urlanalysis import Urlanalysis
from web_save_path import WebSavePath
from extra_opration import web_info_transfer


class WhoisSearchStart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(WhoisSearchStart, self).__init__()
        self.task_id = task_id
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)

        # 初始化操作
        self.task_start_time = ''
        self.user_id = ''
        self.whois_search_url = ''
        self.whois_reverse_url = ''
        self.counterfeit_urls = []
        self.task_state = 0

        self.read_task_info()

    def read_task_info(self):
        '''
        读取任务信息
        '''
        table_name = 'task_info'
        fields = ['last_time', 'user_id', 'counterfeit_id',
                  'whois_search_url', 'whois_reverse_url']
        wheres = {'task_id': [self.task_id, 'd']}
        task_info = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            sys.stderr.write(
                '%s  task no exist, task_id: %s\n' % (time.ctime(), self.task_id))
            os._exit(0)
        self.task_start_time = task_info['last_time']
        self.user_id = task_info['user_id']
        self.whois_search_url = task_info['whois_search_url']
        self.whois_reverse_url = task_info['whois_reverse_url']
        original_counterfeit_list = task_info['counterfeit_id']
        # get counterfeit url in mysql counterfeit_list
        if original_counterfeit_list is not None and original_counterfeit_list != '':
            counterfeit_id_list = original_counterfeit_list.split('-')
            table_name = 'counterfeit_list'
            fields = ['url']
            for counterfeit_id in counterfeit_id_list:
                wheres = {'id': [int(counterfeit_id), 'd']}
                select_result = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if select_result is False:
                    continue
                counterfeit_url = select_result['url'].encode('utf-8')
                self.counterfeit_urls.append(counterfeit_url)

    def add_gray_list(self, url_list):
        if url_list == []:
            return False
        gray_objectid = self.mongo_operate.create_gray(
            gray_name='whois_reverse_gray', gray_type='whois_reverse',
            usr_id=self.user_id, task_id=self.task_id)
        self.mongo_operate.add_gray_list(
            url_list, gray_objectid)
        table_name = 'task_result'
        fields = {'original_grayid': [gray_objectid, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        # save gray_list info in mysql suspect_list
        url_num = len(url_list)
        self.mysql_handle.insert_suspect_list(gray_objectid, self.user_id, self.task_id,
                                              'whois_reverse', url_num, suspect_type=2)
        self.mysql_handle.insert_gray_list(url_list, source='whois_reverse')

    def update_finish_state(self, new_gray_lsit):
        run_time = int(time.time() - self.run_start_time)
        table_name = 'task_result'
        fields = {'e_whois_search_state': [03, 'd'],
                  'whois_search_run_time': [run_time, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        # message to control
        if new_gray_lsit == []:
            send_result = self.message_other_engine(9, ['00'], self.task_id)
        else:
            self.add_gray_list(new_gray_lsit)
            send_result = self.message_other_engine(5, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    def run_whois_reverse(self, url):
        whois_reverse = WhoisReverse(self.mysql_host, self.mysql_db,
                                     self.mysql_user, self.mysql_password)
        try:
            reverse_url_list = []
            reverse_domain_list = whois_reverse.get_reverse_whois(url)
            for domian in reverse_domain_list:
                reverse_url = 'http://' + domian + '/'
                reverse_url_list.append(reverse_url)
            return reverse_url_list
        except:
            traceback.print_exc()
            return []

    def run_whois_search(self, url):
        '''
        通过使whois查询模块在子线程中运行，从而避免对主线程造成影响
        '''
        url_analysis = Urlanalysis(1, self.mysql_host, self.mysql_user,
                                   self.mysql_password, self.mysql_db)
        url_list = [url]
        try:
            url_analysis.getUrllist_list(url_list)
        except:
            traceback.print_exc()

    def web_save_transfer(self, url):
        self.mongo_operate.transfer_web_save(
            url, source_type='gray', goal_type='counterfeit')
        h = WebSavePath()
        source_file_path, target_file_path = h.get_transfer_path(
            url, 'gray', 'counterfeit')
        web_info_transfer(source_file_path, target_file_path)

    def whois_operation(self):
        if self.whois_search_url != '' and self.whois_search_url is not None:
            self.run_whois_search(self.whois_search_url)
        if self.whois_reverse_url != '' and self.whois_reverse_url is not None:
            self.run_whois_reverse(self.whois_reverse_url)
        new_gray_lsit = []
        while 1:
            try:
                url = self.counterfeit_urls.pop()
                #self.web_save_transfer(url)
                self.mysql_handle.update_counterfeit_list_statistic(url)
                self.run_whois_search(url)
                reverse_url_list = self.run_whois_reverse(url)
                new_gray_lsit.extend(reverse_url_list)
            except IndexError:
                break
        self.update_finish_state(new_gray_lsit)

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.run_start_time = time.time()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'whois_search', 2)
        self.whois_operation()

if __name__ == '__main__':
    exist_changed_path = os.path.dirname(
        os.path.abspath(__file__)) + '/exists_changed_wipe'
    U = Domain_start(exist_changed_path, task_id=3, mysql_host='172.31.159.248',
                     mysql_user='root', mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                     mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='')
    U.start()
    print 'program over'
