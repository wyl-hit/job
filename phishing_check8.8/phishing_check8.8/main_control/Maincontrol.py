#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
# import traceback

sys.path.append('../server_base')
from ServerBase import ServerBase
from mysql_handle import MysqlOperate

engine_list = {'domain': '01', 'search': '02', 'filtrate': '04', 'web_save': '05',
               'qt_crawler': '06', 'view_collect': '07', 'title': '08', 'structure': '09',
               'view_emd': '10', 'feature_save': '12', 'whois_search': '13'}


class MainControl(ServerBase):

    def __init__(self):
        super(MainControl, self).__init__('control')
        self.mysql_handle = MysqlOperate(self.mysql_db, self.mysql_host,
                                         self.mysql_user, self. mysql_password)

    def read_task_info(self, task_id):
        '''
        read task type and run engine
        '''
        table_name = 'task_info'
        fields = ['task_type', 'task_engine']
        wheres = {'task_id': [task_id, 'd']}
        task_info = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            sys.stderr.write(
                '%s  task no exist, task_id: %s\n' % (time.ctime(), task_id))
            os._exit(0)
        task_type = task_info['task_type']
        task_engines = task_info['task_engine'].split('-')
        return task_type, task_engines

    def read_running_engine(self, task_id):
        task_start_time = self.mysql_handle.get_task_last_time(task_id)
        table_name = 'task_result'
        fields = ['e_domain_state', 'e_search_state', 'e_filtrate_state',
                  'e_web_save_state', 'e_qt_crawler_state', 'e_feature_save_state',
                  'e_whois_search_state', 'e_title_state', 'e_structure_state',
                  'e_view_collect_state', 'e_view_emd_state']
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        select_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        if select_result is False:
            return False
        running_engine_list = []
        for engine in select_result:
            engine_state = select_result[engine]
            if engine_state == 2:
                engine_num = engine_list[engine[2:-6]]
                running_engine_list.append(engine_num)
        print 'running_engine_list', running_engine_list
        return running_engine_list

    def update_start_state(self, task_id):
        task_start_time = self.mysql_handle.get_task_last_time(task_id)
        self.mysql_handle.update_task_state(task_id, task_start_time, 2)

    def update_finished_state(self, task_id, task_state=3):
        # update task finished state to mysql: task_state, task_run_time, task_stop_time
        # get task last_time in task_info
        task_start_time = self.mysql_handle.get_task_last_time(task_id)
        # update task_state, task_run_time, task_stop_time
        task_start_time_stamp = time.mktime(time.strptime(str(task_start_time),
                                                          "%Y-%m-%d %H:%M:%S"))
        task_stop_time_stamp = time.time()
        task_run_time = task_stop_time_stamp - task_start_time_stamp
        task_stop_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(task_stop_time_stamp))
        table_name = 'task_result'
        fields = {'task_state': [task_state, 'd'],
                  'task_run_time': [task_run_time, 'd'],
                  'task_stop_time': [task_stop_time, 's']}
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        result = self.mysql_handle.require_post(
            table_name, fields, wheres, post_type='update')
        sys.stdout.write(
            '%s |*|task win over|*|, task_id: %s, task_state: %s\n' % (time.ctime(), task_id, task_state))
        return result

    def check_engine_state(self, task_id, task_type, engines):
        '''
        Determine whether all the detection engine run over
        '''
        task_start_time = self.mysql_handle.get_task_last_time(task_id)
        table_name = 'task_result'
        fields = ['e_title_state', 'e_structure_state', 'e_view_emd_state']
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        task_result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one')
        e_title_state = task_result['e_title_state']
        e_structure_state = task_result['e_structure_state']
        e_view_emd_state = task_result['e_view_emd_state']
        if '08' in engines or task_type == 5:
            if e_title_state != 3:
                return False
        if '09' in engines or task_type == 5:
            if e_structure_state != 3:
                return False
        if '10' in engines or task_type == 5:
            if e_view_emd_state != 3:
                return False
        return True

    '''
    重写响应函数
    '''

    def web_request_start(self, task_id):
        '''
        重写守护进程基类，响应请求
        '''
        sys.stdout.write('%s  control receive task_id start request: %s\n' %
                         (time.ctime(), task_id))
        message_result = False
        task_type, task_engines = self.read_task_info(task_id)
        if task_type == 1 or task_type == 3:
            if '01' in task_engines:
                message_result = self.message_other_engine(0, ['01'], task_id)
                self.update_start_state(task_id)
            if '02' in task_engines:
                message_result = self.message_other_engine(0, ['02'], task_id)
                self.update_start_state(task_id)
            if '13' in task_engines:
                message_result = self.message_other_engine(0, ['13'], task_id)
                self.update_start_state(task_id)
        elif task_type == 2:
            # 04: filtrate engine, check first filtrate
            message_result = self.message_other_engine(0, ['04'], task_id)
            self.update_start_state(task_id)
        elif task_type == 4:
            # 05: web save engine
            message_result = self.message_other_engine(0, ['05'], task_id)
            self.update_start_state(task_id)
        elif task_type == 5:
            # 13: whois search engine
            message_result = self.message_other_engine(0, ['13'], task_id)
            self.update_start_state(task_id)
        else:
            sys.stderr.write(
                '%s  task_type error, task_id: %s, task_type: %d' % (time.ctime(), task_id, task_type))
        return message_result

    def web_request_stop(self, task_id):
        '''
        主控服务响应前台客户端任务结束请求
        '''
        sys.stdout.write('%s  control receive task_id stop request: %s\n' %
                         (time.ctime(), task_id))
        running_engine_list = self.read_running_engine(task_id)
        message_result = self.message_other_engine(
            1, running_engine_list, task_id)
        if message_result is True:
            stop_result = self.update_finished_state(task_id)
        else:
            stop_result = False
        return stop_result

    def filtrate_to_control(self, task_id):
        '''
        message 2: filtrate engine finished message control
        '''
        sys.stdout.write('%s  control receive from filtrate engine task_id: %s\n' %
                         (time.ctime(), task_id))
        # 05: web_save engine, end filtrate,start web_save
        self.message_other_engine(0, ['05'], task_id)

    def web_save_to_control(self, task_id):
        '''
        message 3: web_save engine finished message control
        '''
        sys.stdout.write('%s  control receive from web_save engine task_id: %s\n' %
                         (time.ctime(), task_id))
        # 06: qt_crawler engine, 08: title engine
        # end web_save_,start qt_crawler and title engine
        task_type, task_engines = self.read_task_info(task_id)
        self.message_other_engine(0, ['06'], task_id)
        if '08' in task_engines or task_type == 5:
            self.message_other_engine(0, ['08'], task_id)

    def qt_crawler_to_control(self, task_id):
        '''
        message 4: qt_crawler engine finished message control
        '''
        sys.stdout.write('%s  control receive from qt_crawler engine task_id: %s\n' %
                         (time.ctime(), task_id))
        # 09: structure engine, 10: view engine
        # end qt_crawler,start structure and view engine
        task_type, task_engines = self.read_task_info(task_id)
        self.message_other_engine(0, ['12'], task_id)
        self.message_other_engine(0, ['07'], task_id)
        if task_type == 5 or '09' in task_engines:
            self.message_other_engine(0, ['09'], task_id)

    def detect_to_control(self, task_id):
        '''
        message 5: detect(domain or search or whois) engine finished message control
        '''
        sys.stdout.write('%s  control receive from detect engine task_id: %s\n' %
                         (time.ctime(), task_id))
        task_type, task_engines = self.read_task_info(task_id)
        if task_type == 3 or task_type == 5:
            self.message_other_engine(0, ['04'], task_id)
        elif task_type == 1:  # task over
            self.update_finished_state(task_id)

    def check_to_control(self, task_id):
        '''
        message 6: check(title or structure or view) engine finished message control,
        over task
        '''
        task_type, task_engines = self.read_task_info(task_id)
        check_result = self.check_engine_state(
            task_id, task_type, task_engines)
        if check_result is True:  # all check engine overf, task over
            self.update_finished_state(task_id)

    def feature_save_to_control(self, task_id):
        '''
        message 7: feature_save is task_type 4 last engine, other task_type no last
        over task
        '''
        task_type, task_engines = self.read_task_info(task_id)
        if task_type == 4:
            self.update_finished_state(task_id)

    def engine_failure_to_control(self, task_id):
        '''
        message 8: engine_failure,
        over task is error
        '''
        self.update_finished_state(task_id, 0)

    def engine_win_over_to_control(self, task_id):
        '''
        message 9: engine over, After engine need not start
        over task
        '''
        self.update_finished_state(task_id)

    def view_collect_to_control(self, task_id):
        '''
        message 10: view_collect engine over, After start view_emd
        '''
        task_type, task_engines = self.read_task_info(task_id)
        if task_type == 5 or '10' in task_engines:
            self.message_other_engine(0, ['10'], task_id)
        elif task_type == 4:
            self.update_finished_state(task_id)

if __name__ == '__main__':
    main_control = MainControl()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            main_control.start()
        elif 'stop' == sys.argv[1]:
            main_control.stop()
        elif 'restart' == sys.argv[1]:
            main_control.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
