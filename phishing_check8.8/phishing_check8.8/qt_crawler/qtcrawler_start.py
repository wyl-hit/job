# encoding:utf8
import sys
import os
import multiprocessing
import time
from PyQt4.QtGui import QApplication

from page_to_block import Browser
from web_save_path import WebSavePath
from page_shot import CallPageShot
from mysql_handle import MysqlOperate
from mongo_handle import Mongo_Operate


class QtCrawler(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host, mongo_port,
                 mongo_user, mongo_password, message_other_engine,
                 write_process_pid, remove_process_pid):
        super(QtCrawler, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid

        # 初始化操作
        self.run_start_time = 0
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

    def update_running_state(self, crawler_num):  # 任务执行中更新状态
        '''
        在mysql中更新探测状态及结果
        '''
        table_name = 'task_result'
        fields = {'qt_crawler_num': [crawler_num, 'd']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    def update_finish_state(self, crawler_num, run_time):
        table_name = 'task_result'
        fields = {'e_qt_crawler_state': [03, 'd'],
                  'qt_crawler_num': [crawler_num, 'd'],
                  'qt_crawler_run_time': [run_time, 's']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        self.engine_over_handle()

    def engine_over_handle(self):
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))
        send_result = self.message_other_engine(4, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        self.remove_process_pid(self.task_id)
        # self.page_shot()

    def page_shot(self):
        self.read_crawler_config()
        get_protected_iter = self.get_protected_iter
        get_gray_iter = self.get_gray_iter
        get_counterfeit_iter = self.get_counterfeit_iter
        get_monitor_iter = self.get_monitor_iter
        url_type = ''
        while 1:
            try:
                url = get_protected_iter.next()
                url_type = 'protected'
            except StopIteration:
                try:
                    url = get_gray_iter.next()
                    url_type = 'gray'
                except StopIteration:
                    try:
                        url = get_counterfeit_iter.next()
                        url_type = 'counterfeit'
                    except StopIteration:
                        try:
                            url = get_monitor_iter.next()
                            url_type = 'monitor'
                        except StopIteration:
                            break
            print 'shot: ', url

            web_save_path = WebSavePath()
            local_html, local_time = web_save_path.get_html_path_abs(
                url, url_type)
            if local_time is None:
                sys.stderr.write('%s  insert_web_info, web not be saved: %s\n' %
                                 (time.ctime(), url))
                continue
            # webpage blockpage
            webpage_path = local_time + '/webpage.jpeg'
            img_type = 'webpage'  # img name : webpage.jpeg
            if not os.path.exists(webpage_path):
                main_html_path = local_time + '/main.html'
                if not os.path.exists(main_html_path):
                    sys.stderr.write('%s  insert_web_info, main.html not be exist: %s\n' %
                                     (time.ctime(), url))
                    continue
                call_page_shot = CallPageShot(
                    main_html_path, local_time, img_type)
                call_page_shot.start()
                while not os.path.exists(local_time + '/shot_over_sign'):
                    time.sleep(0.5)
                os.remove(local_time + '/shot_over_sign')
        print 'shot over'

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.run_start_time = time.time()

        # self.read_task_info()
        # self.read_crawler_config()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'qt_crawler', 2)
        self.app = QApplication(sys.argv)
        self.br = Browser(self.task_id, self.get_protected_iter, self.get_gray_iter,
                          self.get_counterfeit_iter, self.get_monitor_iter,
                          self.mongo_operate, self.update_running_state,
                          self.update_finish_state, self.mysql_handle, self.run_start_time)
        # self.br.showMaximized() # show web
        # self.br.show()
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    url_list = ['http://www.taobao.com/', 'http://www.vip.com/']
    qtc = QtCrawler(url_list, 6, stdout=0, stderr=0, mysql_host='172.31.159.248', mysql_user='root',
                    mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                    mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='')
    qtc.start()
