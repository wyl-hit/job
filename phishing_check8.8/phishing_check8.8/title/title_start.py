#!/usr/bin/python
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
import traceback

from title_main import TitleMain
from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate


class Title_start(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db, mysql_user, mysql_password,
                 mongo_db, mongo_host, mongo_port, mongo_user, mongo_password,
                 message_other_engine, write_process_pid, remove_process_pid):
        super(Title_start, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.task_start_time = ''
        self.user_id = ''
        self.gary_objectid = ''
        self.protected_list_id = []
        self.get_protect_dict = {}
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid
        self.mongo_operate = Mongo_Operate(
            mongo_db, mongo_host, mongo_port, mongo_user, mongo_password)
        self.read_task_info()
        self.run_start_time = 0
        self.title_check_num = 0  # 检查数量
        self.title_find_num = 0  # 检查到钓鱼url的数量

        # self.split_values = 10  # 设置数值，分割每多少个url更新入数据库
        self.once_update_num = 1

    def read_task_info(self):
        '''
        读取任务信息
        '''
        self.task_start_time = self.mysql_handle.get_task_last_time(
            self.task_id)
        saved_urls_iters = self.mysql_handle.read_saved_urls(
            self.task_id, self.mongo_operate)
        self.get_gray_iter = saved_urls_iters['get_gray_iter']
        self.get_monitor_iter = saved_urls_iters['get_monitor_iter']
        self.protected_title_dict = self.mysql_handle.get_all_protected_feature(
            self.mongo_operate.get_web_title)
        self.protected_text_dict = self.mysql_handle.get_all_protected_feature(
            self.mongo_operate.get_web_text)

        self.counterfeit_title_dict = self.mysql_handle.get_all_counterfeit_feature(
            self.mongo_operate.get_web_title)
        self.counterfeit_text_dict = self.mysql_handle.get_all_counterfeit_feature(
            self.mongo_operate.get_web_text)

    # 任务执行中更新状态
    def update_running_state(self, title_check_num, title_find_num):
        '''
        在mysql中更新探测状态及结果
        '''

        table_name = 'task_result'
        fields = {'title_check_num': [
            title_check_num, 'd'], 'title_find_num': [title_find_num, 'd']}
        wheres = {
            'task_id': [self.task_id, 'd'], 'start_time': [self.task_start_time, 's']}
        result = self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    # 任务完成更新状态
    def update_finished_state(self):
        '''
        在mysql中更新探测状态及结果
        '''
        run_time = int(time.time()) - int(self.run_start_time)
        table_name = 'task_result'
        fields = {'e_title_state': [03, 'd'], 'title_run_time': [run_time, 's'],
                  'title_check_num': [self.title_check_num, 'd'], 'title_find_num':
                  [self.title_find_num, 'd']}
        wheres = {
            'task_id': [self.task_id, 'd'], 'start_time': [self.task_start_time, 's']}
        result = self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        self.engine_over_handle()

    def engine_over_handle(self):
        # message to control
        send_result = self.message_other_engine(6, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))
        self.remove_process_pid(self.task_id)

    def run(self):
        self.run_start_time = time.time()
        self.write_process_pid(self.task_id)
        sys.stdout.write(
            '%s  |*|title engine start|*|, task_id: %s\n' % (time.ctime(), self.task_id))

        title_main = TitleMain(self.task_id, self.task_start_time,
                               self.protected_title_dict, self.protected_text_dict, self.mongo_operate, self.mysql_handle)
        update_count = 0
        counterfeit_get_gray_iter = []
        while True:
            try:
                gray_url = self.get_gray_iter.next()
                counterfeit_get_gray_iter.append(gray_url)  
                check_result = title_main.title_run(gray_url)
                self.title_find_num += check_result
                self.title_check_num += 1
                update_count += 1
                if update_count >= self.once_update_num:
                    update_count = 0
                    self.update_running_state(
                        self.title_check_num, self.title_find_num)
            except StopIteration:
                break
        title_main2 = TitleMain(self.task_id, self.task_start_time,
                                self.counterfeit_title_dict, self.counterfeit_text_dict,
                                self.mongo_operate, self.mysql_handle, 'counterfeit')
        while True:
            try:
                gray_url = counterfeit_get_gray_iter.pop()
                check_result = title_main2.title_run(gray_url)
                self.title_find_num += check_result
                self.title_check_num += 1
                update_count += 1
                if update_count >= self.once_update_num:
                    update_count = 0
                    self.update_running_state(
                        self.title_check_num, self.title_find_num)
            except IndexError:
                break
        self.update_finished_state()

if __name__ == '__main__':
    U = Title_start(mysql_host='172.31.159.248', mysql_user='root', mysql_password='',
                    mysql_db='phishing_check', task_id=2, read_url=None, title_pid_path='./pid')
    U.start()
