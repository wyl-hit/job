#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
    模块任务：对生成的url灰名单进行title比对，判断是否为钓鱼url
    输入：    task_id
    输出：    钓鱼url列表
'''
import multiprocessing
import time
import os
import sys
from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate
from emd_calculate import ViewEmd


class View_Emd_start(multiprocessing.Process):

    def __init__(self, task_id, current_path, mysql_host, mysql_db, mysql_user, mysql_password,
                 mongo_db, mongo_host, mongo_port, mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(View_Emd_start, self).__init__()
        self.task_id = task_id
        self.task_start_time = ''
        self.user_id = ''
        self.view_protected_objectid = ''
        self.view_gray_objectid = ''
        self.view_counterfeit_objectid = ''
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.mongo_operate = Mongo_Operate(
            mongo_db, mongo_host, mongo_port, mongo_user, mongo_password)

        self.current_path = sys.path[0]
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid
        self.read_task_info()

    def read_task_info(self):
        '''
        读取任务信息
        '''
        self.task_start_time = self.mysql_handle.get_task_last_time(
            self.task_id)
        saved_urls_iters = self.mysql_handle.read_saved_urls(
            self.task_id, self.mongo_operate)
        self.get_protected_iter = saved_urls_iters['get_protected_iter']
        self.get_gray_iter = saved_urls_iters['get_gray_iter']
        self.get_counterfeit_iter = saved_urls_iters['get_counterfeit_iter']
        self.get_monitor_iter = saved_urls_iters['get_monitor_iter']

        self.protected_title_dict = self.mysql_handle.get_all_protected_feature(
            self.mongo_operate.get_web_title)

        self.counterfeit_title_dict = self.mysql_handle.get_all_counterfeit_feature(
            self.mongo_operate.get_web_title)

    def update_running_state(self, finish_num, view_find_num):  # 任务执行中更新状态
        '''
        在mysql中更新探测状态及结果

        '''
        table_name = 'task_result'
        fields = {
            'view_check_num': [finish_num, 'd'], 'view_find_num': [view_find_num, 'd']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    def engine_over_handle(self):
        send_result = self.message_other_engine(6, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    # 任务完成更新状态
    def update_finished_state(self, run_time, finish_num):
        '''
        在mysql中更新探测状态及结果
        '''
        table_name = 'task_result'
        fields = {'e_view_emd_state': [03, 'd'],
                  'view_emd_run_time': [run_time, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        self.engine_over_handle()

    def run(self):
        finish_num = 0
        view_find_num = 0
        view_find_flags = 0
        start_time = time.time()

        View_emd = ViewEmd(self.mysql_handle, self.mongo_operate, self.task_id, self.task_start_time,
                           self.protected_title_dict, self.counterfeit_title_dict)
        while True:
            try:
                gray_url = self.get_gray_iter.next()
                view_find_flags = View_emd.emdcalculate(gray_url)
                finish_num += 1
                view_find_num += view_find_flags
                self.update_running_state(finish_num, view_find_num)
            except StopIteration:
                break
        run_time = int(time.time()) - int(start_time)
        #run_time = time.ctime(run_time)

        self.update_finished_state(run_time, finish_num)
