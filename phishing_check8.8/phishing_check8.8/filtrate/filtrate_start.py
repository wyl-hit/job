#!/usr/bin/env python
# coding=utf-8
'''
输入参数是taskid，取出灰名单列表后进行黑白名单对比，
将黑名单和白名单的条数写入mongo，将依旧是白名单的新建集合，写入
'''
import time
import sys
import os
import multiprocessing
#import traceback

from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate


class FiltrateStart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(FiltrateStart, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        # 初始化操作
        self.user_id = ''
        self.gray_urls = []
        self.task_start_time = ''
        self.run_start_time = 0
        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)
        self.read_task_info()

    def read_task_info(self):
        '''
        读取任务信息
        '''
        table_name = 'task_info'
        fields = ['last_time', 'user_id', 'gray_id']
        wheres = {'task_id': [self.task_id, 'd']}
        task_info = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            sys.stderr.write(
                '%s  task no exist, task_id: %s\n' % (time.ctime(), self.task_id))
            os._exit(0)
        self.task_start_time = task_info['last_time']
        self.user_id = task_info['user_id']
        gray_id = task_info['gray_id']
        # read gray url
        if gray_id is not None and gray_id != '':
            gray_id = gray_id.split('-')
            table_name = 'gray_list'
            fields = ['url']
            for once_gray_id in gray_id:
                wheres = {'id': [int(once_gray_id), 'd']}
                select_result = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if select_result is False:
                    continue
                gray_url = select_result['url'].encode('utf-8')
                self.gray_urls.append(gray_url)
        # read detected url
        table_name = 'task_result'
        fields = ['original_grayid']
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        select_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        gary_objectid = select_result['original_grayid']
        if gary_objectid is not None and gary_objectid != '':
            gary_objectid = self.mongo_operate.expand_gray_list(
                gary_objectid)
            self.get_gray_iter = self.mongo_operate.get_gray_list(
                gary_objectid)
        else:
            self.get_gray_iter = iter([])

    def update_finish_state(self, trusted_filtrate_num, counterfeit_filtrate_num, filtrate_objectid,
                            filtrate_trusted_objectid, filtrate_counterfeit_objectid):
        '''
        task run over, update information in mysql
        '''
        run_time = int(time.time() - self.run_start_time)
        table_name = 'task_result'
        fields = {'e_filtrate_state': [03, 'd'],
                  'filtrate_trusted_num': [trusted_filtrate_num, 'd'],
                  'filtrate_counterfeit_num': [counterfeit_filtrate_num, 'd'],
                  'filtrate_run_time': [run_time, 's'],
                  'filtrate_objectid': [filtrate_objectid, 's'],
                  'filtrate_trusted_objectid': [filtrate_trusted_objectid, 's'],
                  'filtrate_counterfeit_objectid': [filtrate_counterfeit_objectid, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        # message to control
        send_result = self.message_other_engine(2, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    def trusted_select(self, gray_url):
        '''
        在被信任名单中查询
        '''
        table_name = 'trusted_list'
        fields = ['*']
        wheres = {'url': [gray_url, 's']}
        select_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one', 0)
        return select_result

    def counterfeit_select(self, gray_url):
        '''
        在仿冒名单中查询
        '''
        table_name = 'counterfeit_list'
        fields = ['*']
        wheres = {'url': [gray_url, 's']}
        select_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one', 0)
        return select_result

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.run_start_time = time.time()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'filtrate', 2)

        trusted_filtrate_num = 0
        counterfeit_filtrate_num = 0
        suspect_grays = []  # not filtrate url
        trusted_grays = []
        counterfeit_grays = []
        while 1:
            try:
                gray_url = self.get_gray_iter.next()
            except StopIteration:
                try:
                    gray_url = self.gray_urls.pop()
                except IndexError:
                    break
            '''
            对gray_url进行黑白名单比对，属于黑白名单则更新filtrate_num，
            否则放到suspect_grays中
            '''
            select_result = self.trusted_select(gray_url)
            if select_result is not False:
                trusted_filtrate_num += 1
                trusted_grays.append(gray_url)
                continue
            else:
                select_result = self.counterfeit_select(gray_url)
                if select_result is not False:
                    counterfeit_filtrate_num += 1
                    counterfeit_grays.append(gray_url)
                    continue
                else:
                    suspect_grays.append(gray_url)
        # not filtrate url add gray_list in mongo
        filtrate_objectid = self.mongo_operate.create_gray(
            gray_name='suspect_grays', gray_type='filtrate',
            usr_id=self.user_id, task_id=self.task_id)
        self.mongo_operate.add_gray_list(
            suspect_grays, filtrate_objectid)
        filtrate_trusted_objectid = self.mongo_operate.create_gray(
            gray_name='trusted_grays', gray_type='filtrate',
            usr_id=self.user_id, task_id=self.task_id)
        self.mongo_operate.add_gray_list(
            trusted_grays, filtrate_trusted_objectid)
        filtrate_counterfeit_objectid = self.mongo_operate.create_gray(
            gray_name='counterfeit_grays', gray_type='filtrate',
            usr_id=self.user_id, task_id=self.task_id)
        self.mongo_operate.add_gray_list(
            counterfeit_grays, filtrate_counterfeit_objectid)
        self.update_finish_state(
            trusted_filtrate_num, counterfeit_filtrate_num, filtrate_objectid,
            filtrate_trusted_objectid, filtrate_counterfeit_objectid)

if __name__ == "__main__":
    test = FiltrateStart("172.31.159.248", "", "", "phishing_check", 1)
    test.get_gray_list()
