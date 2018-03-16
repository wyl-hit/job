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
import re
import multiprocessing
from twisted.internet import defer, reactor
from twisted.web.client import getPage
#import traceback

from domain_replace import URLGenerator
from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate

_NUM = 3  # max meantime request web num


class DomainStart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(DomainStart, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        # 初始化操作
        self.user_id = ''
        # 待变换网站列表, 包括已知仿冒网站和被保护网站,
        # 对已知仿冒网站和对被保护网站域名变换方式一样, 故统一处理
        self.wait_change_url_list = []
        self.original_host_rules = []
        self.original_top_rules = []
        self.original_path_rules = []
        self.exist_list = []  # 记录存在的url
        self.task_start_time = ''
        self.run_start_time = 0
        self.url_create_list = []
        self.protect_url = ''
        self.deferreds = []
        self.read_task_info()
        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)
        # 创建域名生成器对象
        self.url_gen = URLGenerator(self.task_id, self.mongo_operate,
                                    self.update_running_state,
                                    self.wait_change_url_list, self.original_host_rules,
                                    self.original_top_rules, self.original_path_rules)
        self.domain_change_url = self.url_gen.URL_Generator()  # 创建生成器

        self.domain_save_path = '/tmp/' + \
            str(task_id) + '_domain_request_urls.txt'
        self.domain_live_path = '/tmp/' + \
            str(task_id) + '_domain_live.txt'
        self.file_request_urls = open(self.domain_save_path, 'w')
        self.file_live_url = open(self.domain_live_path, 'w')

    def read_task_info(self):
        '''
        读取任务信息
        '''
        table_name = 'task_info'
        fields = ['last_time', 'user_id', 'protected_id', 'counterfeit_id',
                  'host_rule_id', 'top_rule_id', 'path_rule_id']
        wheres = {'task_id': [self.task_id, 'd']}
        task_info = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            os._exit(0)
        self.task_start_time = task_info['last_time']
        self.user_id = task_info['user_id']
        protected_list_id = task_info['protected_id']
        counterfeit_list_id = task_info['counterfeit_id']
        host_rule_id = task_info['host_rule_id']
        top_rule_id = task_info['top_rule_id']
        path_rule_id = task_info['path_rule_id']
        self.read_rule_config(
            protected_list_id, counterfeit_list_id, host_rule_id,
            top_rule_id, path_rule_id)

    def read_rule_config(self, protected_list_id, counterfeit_list_id,
                         host_rule_id, top_rule_id, path_rule_id):
        '''
        从mysql中读取变换规则和被保护名单
        '''
        if protected_list_id is not None and protected_list_id != '':
            protected_list_id = protected_list_id.split('-')
            for protected_id in protected_list_id:  # 读取mysql中的被保护名单
                table_name = 'protected_list'
                fields = ['url']
                wheres = {'id': [int(protected_id), 'd']}
                task_info = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if task_info is False:
                    continue
                protected = task_info['url']
                self.wait_change_url_list.append(protected)
        if counterfeit_list_id is not None and counterfeit_list_id != '':
            counterfeit_list_id = counterfeit_list_id.split('-')
            for counterfeit_id in counterfeit_list_id:  # 读取mysql中的待变换已知仿冒网站
                table_name = 'counterfeit_list'
                fields = ['url']
                wheres = {'id': [int(counterfeit_id), 'd']}
                task_info = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if task_info is False:
                    continue
                counterfeit = task_info['url']
                self.wait_change_url_list.append(counterfeit)
        if host_rule_id is not None and host_rule_id != '':
            host_rule_id = host_rule_id.split('-')
            for rule_id in host_rule_id:  # 读取mysql中的主机域名变换规则
                table_name = 'host_change_rule'
                fields = ['change_rule']
                wheres = {'id': [int(rule_id), 'd']}
                task_info = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if task_info is False:
                    continue
                result = task_info['change_rule']
                result = result.split('|')
                for once_result in result:
                    self.original_host_rules.append(str(once_result))
        if top_rule_id is not None and top_rule_id != '':
            top_rule_id = top_rule_id.split('-')
            for top_id in top_rule_id:  # 读取mysql中的顶级域名变换规则
                table_name = 'top_change_rule'
                fields = ['change_rule']
                wheres = {'id': [int(top_id), 'd']}
                task_info = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if task_info is False:
                    continue
                result = task_info['change_rule']
                self.original_top_rules.append(str(result))
        if path_rule_id is not None and path_rule_id != '':
            path_rule_id = path_rule_id.split('-')
            for path_id in path_rule_id:  # 读取mysql中的路径变换规则
                table_name = 'path_change_rule'
                fields = ['change_rule']
                wheres = {'id': [int(path_id), 'd']}
                task_info = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'one')
                if task_info is False:
                    continue
                result = task_info['change_rule']
                self.original_path_rules.append(str(result))

    def update_running_state(self, all_change_num, all_exist_change_num,
                             changed_num, gray_exist_num, update_type=0):
        '''
        在mysql中更新探测状态及结果
        update_type=0: domain change update
        update_type=1: url exist check update
        '''
        table_name = 'task_result'
        wheres = {
            'task_id': [self.task_id, 'd'],
            'start_time': [self.task_start_time, 's']}
        if update_type == 0:
            fields = {'domain_changed_all_num': [all_change_num, 'd'],
                      'domain_changed_exist_num': [all_exist_change_num, 'd'],
                      'domain_detected_num': [changed_num, 'd']}
            self.mysql_handle.require_post(
                table_name, fields, wheres, 'update')
        if update_type == 1:
            fields = {'domain_gray_url_num': [gray_exist_num, 'd']}
            self.mysql_handle.require_post(
                table_name, fields, wheres, 'update')

    def create_gray_mongo(self, exist_list):
        gray_name = 'NO.' + str(self.task_id) + ' task domian'
        detect_objectID = self.mongo_operate.create_gray(
            gray_name=gray_name, gray_type='domain_change',
            usr_id=self.user_id, task_id=self.task_id)
        self.mongo_operate.add_gray_list(exist_list, detect_objectID)
        return detect_objectID

    def update_finish_state(self, exist_list, run_time):
        '''
        task run over, update information in mysql
        '''
        detect_objectID = self.create_gray_mongo(exist_list)
        exist_url_num = len(exist_list)
        # save domain engine result in mysql task_result
        table_name = 'task_result'
        fields = {'e_domain_state': [03, 'd'],
                  'domain_gray_url_num': [exist_url_num, 'd'],
                  'original_grayid': [detect_objectID, 's'],
                  'domain_run_time': [run_time, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        if exist_list == []:
            send_result = self.message_other_engine(9, ['00'], self.task_id)
        else:
            # save gray_list info in mysql
            self.mysql_handle.insert_suspect_list(detect_objectID, self.user_id, self.task_id,
                                                  'domain_change', exist_url_num, suspect_type=2)
            self.mysql_handle.insert_gray_list(exist_list, source='domain_change')
            # quit deal
            # message to control
            send_result = self.message_other_engine(5, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))

    def pageCallback(self, result, url, protect):
        '''
        用 getpage检测 网页存在
        网页存在,调用此回调函数
        '''
        global _NUM
        match = re.search(r"<title>(.*?)</title>", result)
        try:
            title = match.group(1)
        except:
            title = 'None'
        if title.find("Redirect") == -1:
            self.exist_list.append(url)
            self.update_running_state(
                gray_exist_num=len(self.exist_list), update_type=1)

        self.file_request_urls.write(url + '\n')
        self.file_request_urls.flush()

        self.file_live_url.seek(0)
        self.file_live_url.truncate(0)
        self.file_live_url.write(url + ' ' + str(self.engine_pid))
        self.file_live_url.flush()
        _NUM += 1
        self.download()

    def finish(self, ign):
        '''
        所有的defer处理完后调用finish结束reacter循环
        '''
        try:
            reactor.stop()
            os.remove(self.domain_save_path)
            os.remove(self.domain_live_path)
        except:
            pass

    def fetch_error(self, error, url, protect):
        '''
        用getpage检测，网页不存在调用此回调函数
        '''
        global _NUM
        if error.getErrorMessage().find('User timeout caused connection failure') != -1:
            d = getPage(url)
            d.addCallback(self.pageCallback, url, protect)
            d.addErrback(self.fetch_error, url, protect)
        else:
            self.file_live_url.seek(0)
            self.file_live_url.truncate(0)
            self.file_live_url.write(url + ' ' + str(self.engine_pid))
            self.file_live_url.flush()
            _NUM += 1
            self.download()

    def download(self):
        global _NUM
        while _NUM > 0:
            try:
                url = self.url_create_list.pop(0)
                d = getPage(url.encode('utf-8'))
                d.addCallback(
                    self.pageCallback, url.encode('utf-8'), self.protect_url)
                d.addErrback(
                    self.fetch_error, url.encode('utf-8'), self.protect_url)
                _NUM -= 1
                self.deferreds.append(d)
            except IndexError:
                try:
                    self.url_create_list = []
                    self.url_create_list = self.domain_change_url.next()
                    # print 'download', self.url_create_list
                    self.protect_url = self.url_create_list[0]
                    self.url_create_list = self.url_create_list[1:]
                except StopIteration:
                    dl = defer.DeferredList(self.deferreds)
                    dl.addCallback(self.finish)
                    break

    def run(self):
        '''
        程序入口
        '''
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.engine_pid = os.getpid()
        self.run_start_time = time.time()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'domain', 2)
        try:
            self.url_create_list = self.domain_change_url.next()
            self.protect_url = self.url_create_list[0]
            self.url_create_list = self.url_create_list[1:]
        except StopIteration:
            pass
        self.download()
        # start
        reactor.run()
        # finaish
        run_time = int(time.time()) - int(self.run_start_time)
        self.update_finish_state(self.exist_list, run_time)

if __name__ == '__main__':
    exist_changed_path = os.path.dirname(
        os.path.abspath(__file__)) + '/exists_changed_wipe'
    U = Domain_start(exist_changed_path, task_id=3, mysql_host='172.31.159.248',
                     mysql_user='root', mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                     mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='')
    U.start()
    print 'program over'
