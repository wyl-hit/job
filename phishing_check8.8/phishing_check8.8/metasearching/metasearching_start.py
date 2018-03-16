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
import MySQLdb
from errors import ConfigurationError, MongoError
from metasearching import Metasearching
import traceback
_PATH = sys.path[0]
try:
    from mongo_handle import Mongo_Operate
except ImportError:
    raise ConfigurationError('Mongo_Operate')
try:
    from mysql_handle import MysqlOperate
except ImportError:
    raise ConfigurationError('Mysql_Operate')


class Metasearching_start(multiprocessing.Process):

    def __init__(self, task_id, stdout, stderr, mysql_host, mysql_user,
                 mysql_password, mysql_db, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine
                 ):
        super(Metasearching_start, self).__init__()
        self.task_id = task_id
        self.start_time = ''
        self.start_run_time = time.time()
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.mongo_db = mongo_db
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.message_other_engine = message_other_engine

        self.user_id = ''
        self.kword_list_id = []    # 记录存在的url
        self.kword_list = []  # 关键字

        # 初始化操作
        self.mysql_handle = MysqlOperate(stdout, stderr, self.mysql_host, self.mysql_user,
                                         self.mysql_password, self.mysql_db, 'domain_start')
        self.mysql_handle.connect_MySQL()
        self.read_task_info()
        # 读取关键字
        self.read_kword_list()
        # 初始化 mongo 连接操作
        self.mongo_operate = Mongo_Operate(
            mongo_db, mongo_host, mongo_port, mongo_user, mongo_password)

    def read_task_info(self):
        '''
        读取任务信息
        '''
        try:
            self.mysql_handle.cur.execute(
                'select last_time, user_id, kword_id from task_info where task_id=%d' % (self.task_id))
            task_info = self.mysql_handle.cur.fetchone()
            if task_info is None:
                sys.stderr.write(
                    '%s  %s\n' % 'metasearching_start read_task_info, task not exist, task_id' %
                    (time.ctime(), self.task_id))
                os._exit(0)
            else:
                self.start_time = task_info[0]
                self.user_id = task_info[1]
                self.kword_list_id = task_info[2].split('-')

        except MySQLdb.Error, e:
            re_connect_result = self.mysql_handle.re_connect_MySQL(
                e, 'metasearching_start read_task_info')
            if re_connect_result is True:
                return self.read_task_info()
            else:
                os._exit(0)
        except:
            traceback.print_exc()

    def read_kword_list(self):
        '''
        读取关键字
        '''
        try:
            for key_id in self.kword_list_id:
                self.mysql_handle.cur.execute('select sensitive_word from sensitive_kword \
                                              where id=%d' % (int(key_id)))
                sensitive_word = self.mysql_handle.cur.fetchone()
                if sensitive_word is None:
                    sys.stderr.write(
                        '%s\n' % 'metasearching_start read_kword_list, not exist')
                    os._exit(0)
                else:
                    self.kword_list.append(sensitive_word[0])
        except MySQLdb.Error, e:
            re_connect_result = self.mysql_handle.re_connect_MySQL(
                e, 'metasearching_start read_kword_list')
            if re_connect_result is True:
                self.read_kword_list()
            else:
                os._exit(0)

    def update_start_state(self):
        try:
            self.mysql_handle.cur.execute("UPDATE task_result SET e_search_state=02, \
                                          search_kword_num=%d WHERE task_id=%d and start_time='%s'"
                                          % (len(self.kword_list_id), self.task_id, self.start_time))
            self.mysql_handle.db_conn.commit()
        except MySQLdb.Error, e:
            re_connect_result = self.mysql_handle.re_connect_MySQL(
                e, 'metasearching_start run, update start stat')
            if re_connect_result is True:
                return self.update_start_state()
            else:
                os._exit(0)
        except:
            traceback.print_exc()

    # 存储 MySQL 信息
    def update_running_state(self, search_url_num, search_kword_num):
        '''
        连接  MySQL
        '''
        try:
            run_time = int(time.time()) - int(self.start_run_time)

            self.mysql_handle.cur.execute("UPDATE task_result SET search_url_num=%d, search_kword_num='%d', search_run_time='%s' WHERE task_id=%d and start_time='%s'"
                                          % (search_url_num, search_kword_num, run_time, self.task_id, self.start_time))
            self.mysql_handle.db_conn.commit()
        except MySQLdb.Error, e:
            re_connect_result = self.mysql_handle.re_connect_MySQL(
                e, 'metasearching_start run, update_running_state stat')
            if re_connect_result is True:
                return self.update_running_state()
            else:
                os._exit(0)
        except:
            traceback.print_exc()

    def update_stop_state(self, objectID):
        run_time = int(time.time()) - int(self.start_run_time)
        try:
            # save metasearching engine result in mysql task_result
            self.mysql_handle.cur.execute("UPDATE task_result SET e_search_state=03, \
                                          search_run_time='%s' WHERE task_id=%d and start_time='%s'"
                                          % (run_time, self.task_id, self.start_time))
            self.mysql_handle.db_conn.commit()
            self.mysql_handle.cur.execute("UPDATE task_info SET suspected_id='%s' \
                                          WHERE task_id=%d" % (objectID, self.task_id))
            self.mysql_handle.db_conn.commit()

        except MySQLdb.Error, e:
            re_connect_result = self.mysql_handle.re_connect_MySQL(
                e, 'metasearching_start run, update over state')
            if re_connect_result is True:
                return self.update_stop_state()
            else:
                os._exit(0)
        except:
            traceback.print_exc()

    def run(self):
        '''
        程序入口
        '''
        global _PATH
        objectids = []
        sys.stdout.write(
            '%s  |*|metasearching engine start|*|, task_id: %s\n' % (time.ctime(), self.task_id))
        # 写 mongo 数据库
        gray_name = 'NO.' + str(self.task_id) + ' task meta'
        try:
            objectID = self.mongo_operate.create_gray(gray_name=gray_name, gray_type='meta_change',
                                                      usr_id=self.user_id, task_id=self.task_id)
            objectids.append(objectID)
            objectid_childs = self.mongo_operate.expand_gray_list(objectids)
        except Exception, e:
            print ('%s\n' % MongoError(e, 'mate_run add gray'))
            print (' task_id: %s\n' % self.task_id)

        linkinfo_file = _PATH + '/runinfo/link_info.ini'
        numinfo_file = _PATH + '/runinfo/num_info.ini'
        with open(linkinfo_file, 'wb') as f:
            pass
        with open(numinfo_file, 'wb') as f:
            pass

        m = Metasearching(self.kword_list, self.mongo_operate, objectID, linkinfo_file, numinfo_file,
                          _PATH, self.update_running_state)
        # 开始检索
        m.start_search()
        # 打印错误
        for error in m.error_list:
            sys.stdout.write(
                'error1: %s, error1: %s, error1: %s, task_id: %s\n' %
                (error[0], error[1], error[2], self.task_id))
        # 结束打印
        self.update_stop_state(objectID)
        self.message_other_engine(5, ['00'], self.task_id)
        sys.stdout.write(
            '%s |*|metasearching engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))


if __name__ == '__main__':
    U = Metasearching_start(task_id=4, mysql_host='172.31.159.248', mysql_user='root',
                            mysql_password='', mysql_db='phishing_check',  mongo_db='test2',
                            mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root',
                            mongo_password='')
    U.start()
