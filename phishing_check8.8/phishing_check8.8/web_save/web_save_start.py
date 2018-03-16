#!/usr/bin/python
#-*-coding:utf-8-*-
'''
    模块任务：
    输入：
    输出：
'''
import multiprocessing
import time
import os
import sys
from web_save_main import WebSave
from twisted.internet import reactor
# import traceback

from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate


class WebSavestart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(WebSavestart, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        # 初始化操作
        self.task_start_time = ''
        self.user_id = ''
        self.protected_urls = []
        self.counterfeit_urls = []
        self.gray_urls = []
        self.monitor_urls = []
        self.url_num = 0
        self.gary_objectid = ''
        self.file_context = ''
        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)
        self.read_task_info()

    def read_task_info(self):
        '''
        读取任务信息
        '''
        table_name = 'task_info'
        fields = ['last_time', 'user_id', 'protected_id', 'gray_id',
                  'counterfeit_id', 'monitor_id']
        wheres = {'task_id': [self.task_id, 'd']}
        task_info = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            sys.stderr.write(
                '%s  task no exist, task_id: %s\n' % (time.ctime(), self.task_id))
            os._exit(0)
        self.task_start_time = task_info['last_time']
        self.user_id = task_info['user_id']
        original_protected_list = task_info['protected_id']
        original_counterfeit_list = task_info['counterfeit_id']
        original_gray_list = task_info['gray_id']
        original_monitor_list = task_info['monitor_id']

        # get protected url, all test may have protected url to save
        if original_protected_list is not None and original_protected_list != '':
            protected_id_list = original_protected_list.split('-')
            table_name = 'protected_list'
            fields = ['url']
            for protected_id in protected_id_list:  # 读取mysql中的被保护名单
                wheres = {'id': [int(protected_id), 'd']}
                select_result = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if select_result is False:
                    continue
                protected_url = select_result['url'].encode('utf-8')
                self.protected_urls.append(protected_url)
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
        # get gray url in mysql gray_list
        if original_gray_list is not None and original_gray_list != '':
            gray_id_list = original_gray_list.split('-')
            table_name = 'gray_list'
            fields = ['url']
            for gray_id in gray_id_list:
                wheres = {'id': [int(gray_id), 'd']}
                select_result = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if select_result is False:
                    continue
                gray_url = select_result['url'].encode('utf-8')
                self.gray_urls.append(gray_url)
        # get monitor url in mysql monitor_list
        if original_monitor_list is not None and original_monitor_list != '':
            monitor_id_list = original_monitor_list.split('-')
            table_name = 'monitor_list'
            fields = ['url']
            for monitor_id in monitor_id_list:
                wheres = {'id': [int(monitor_id), 'd']}
                select_result = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if select_result is False:
                    continue
                monitor_url = select_result['url'].encode('utf-8')
                self.monitor_urls.append(monitor_url)
        # get suspected url
        table_name = 'task_result'
        fields = ['filtrate_objectid']
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        select_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if select_result is not False:
            self.gary_objectid = select_result['filtrate_objectid']
            if self.gary_objectid is None:
                self.get_gray_iter = iter([])
                self.gray_url_num = 0
            else:
                self.gray_url_num = self.mongo_operate.get_gray_num(
                    self.gary_objectid)
                self.gary_objectid = self.mongo_operate.expand_gray_list(
                    self.gary_objectid)
                self.get_gray_iter = self.mongo_operate.get_gray_list(
                    self.gary_objectid)
        else:
            self.get_gray_iter = iter([])
            self.gray_url_num = 0
        self.url_num = self.gray_url_num + \
            len(self.protected_urls) + len(self.gray_urls) + \
            len(self.counterfeit_urls) + len(self.monitor_urls)

    def update_running_state(self, saved_num, request_num):  # 任务执行中更新状态
        '''
        在mysql中更新探测状态及结果
        '''
        table_name = 'task_result'
        fields = {'web_save_num': [saved_num, 'd'],
                  'web_request_num': [request_num, 'd']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    def add_saved_ulr_mongo(self, ulist):
        '''
        将保存的URL分类存入mongo中
        '''
        saved_protected_urls = []
        saved_gray_urls = []
        saved_counterfeit_urls = []
        saved_monitor_urls = []
        # url is like ['http://www.taobao.com/', 'gray\n'] delete download_urls
        # url last '/n'
        for url in ulist:
            if url[1] == 'gray':
                saved_gray_urls.append(url[0])
            elif url[1] == 'protected':
                saved_protected_urls.append(url[0])
            elif url[1] == 'counterfeit':
                saved_counterfeit_urls.append(url[0])
            elif url[1] == 'monitor':
                saved_monitor_urls.append(url[0])
        if saved_gray_urls != []:
            self.save_gray_objectID = self.mongo_operate.create_gray(
                gray_name='save_gray_urls', gray_type='websave', usr_id=self.user_id)
            self.mongo_operate.add_gray_list(
                saved_gray_urls, self.save_gray_objectID)
        else:
            self.save_gray_objectID = ''
        if saved_protected_urls != []:
            self.save_protected_objectID = self.mongo_operate.create_gray(
                gray_name='saved_protected_urls', gray_type='websave', usr_id=self.user_id)
            self.mongo_operate.add_gray_list(
                saved_protected_urls, self.save_protected_objectID)
        else:
            self.save_protected_objectID = ''
        if saved_counterfeit_urls != []:
            self.save_counterfeit_objectID = self.mongo_operate.create_gray(
                gray_name='saved_counterfeit_urls', gray_type='websave', usr_id=self.user_id)
            self.mongo_operate.add_gray_list(
                saved_counterfeit_urls, self.save_counterfeit_objectID)
        else:
            self.save_counterfeit_objectID = ''
        if saved_monitor_urls != []:
            self.save_monitor_objectID = self.mongo_operate.create_gray(
                gray_name='saved_monitor_urls', gray_type='websave', usr_id=self.user_id)
            self.mongo_operate.add_gray_list(
                saved_monitor_urls, self.save_monitor_objectID)
        else:
            self.save_monitor_objectID = ''

    def update_finished_state(self, ulist, run_time, request_num):
        '''
        在mysql中更新探测状态及结果
        '''
        if ['http://cpuzt.cc/', 'gray'] not in ulist:
            ulist.append(['http://cpuzt.cc/', 'gray'])
        if ['http://www.138.gg/', 'gray'] not in ulist:
            ulist.append(['http://www.138.gg/', 'gray'])
        if ['http://www.bjstkc.com/', 'gray'] not in ulist:
            ulist.append(['http://www.bjstkc.com/', 'gray'])
        self.add_saved_ulr_mongo(ulist)
        saved_num = len(ulist)
        table_name = 'task_result'
        fields = {'e_web_save_state': [03, 'd'],
                  'web_save_num': [saved_num, 'd'],
                  'web_request_num': [request_num, 'd'],
                  'web_save_run_time': [run_time, 's'],
                  'save_protected_objectid': [self.save_protected_objectID, 's'],
                  'save_counterfeit_objectid': [self.save_counterfeit_objectID, 's'],
                  'save_monitor_objectid': [self.save_monitor_objectID, 's'],
                  'save_gray_objectid': [self.save_gray_objectID, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

        if ulist == []:
            send_result = self.message_other_engine(9, ['00'], self.task_id)
        else:
            send_result = self.message_other_engine(3, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|web_save engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'web_save', 2)
        engine = WebSave(self.task_id, self.protected_urls, self.get_gray_iter, self.gray_urls,
                         self.counterfeit_urls, self.monitor_urls, self.url_num,
                         self.update_running_state, self.update_finished_state,
                         self.mongo_operate)
        engine.download()
        reactor.run(installSignalHandlers=0)
