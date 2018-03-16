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

from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate


class FeatureSaveStart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(FeatureSaveStart, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        # 初始化操作
        self.task_start_time = ''
        self.run_start_time = 0
        self.save_num = 0
        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)
        self.task_start_time = self.mysql_handle.get_task_last_time(
            self.task_id)
        saved_urls_iters = self.mysql_handle.read_saved_urls(
            self.task_id, self.mongo_operate)
        self.get_protected_iter = saved_urls_iters['get_protected_iter']
        self.get_gray_iter = saved_urls_iters['get_gray_iter']
        self.get_counterfeit_iter = saved_urls_iters['get_counterfeit_iter']
        self.get_monitor_iter = saved_urls_iters['get_monitor_iter']

    def update_running_state(self, save_num):  # 任务执行中更新状态
        '''
        在mysql中更新探测状态及结果
        '''
        table_name = 'task_result'
        fields = {'feature_save_num': [save_num, 'd']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    def update_finish_state(self, save_num):
        run_time = int(time.time() - self.run_start_time)
        table_name = 'task_result'
        fields = {'e_feature_save_state': [03, 'd'],
                  'feature_save_num': [save_num, 'd'],
                  'feature_save_run_time': [run_time, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        self.engine_over_handle()

    def engine_over_handle(self):
        send_result = self.message_other_engine(7, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    def save_web_feature(self):
        while 1:
            try:
                url = self.get_protected_iter.next()
                url_type = 'protected'
            except StopIteration:
                try:
                    url = self.get_gray_iter.next()
                    url_type = 'gray'
                except StopIteration:
                    try:
                        url = self.get_counterfeit_iter.next()
                        url_type = 'counterfeit'
                    except StopIteration:
                        try:
                            url = self.get_monitor_iter.next()
                            url_type = 'monitor'
                        except StopIteration:
                            break
            table_name = url_type + '_feature'
            self.mysql_handle.insert_web_feature(url, url_type, table_name, update_sign=True)
            self.save_num += 1
            self.update_running_state(self.save_num)

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.run_start_time = time.time()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'feature_save', 2)
        self.save_web_feature()
        self.update_finish_state(self.save_num)

if __name__ == '__main__':
    exist_changed_path = os.path.dirname(
        os.path.abspath(__file__)) + '/exists_changed_wipe'
    U = Domain_start(exist_changed_path, task_id=3, mysql_host='172.31.159.248',
                     mysql_user='root', mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                     mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='')
    U.start()
    print 'program over'
