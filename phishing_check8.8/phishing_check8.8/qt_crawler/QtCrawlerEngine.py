#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
import traceback
import threading
sys.path.append('../server_base')
from ServerBase import ServerBase
from qtcrawler_start import QtCrawler
from errors import OtherError


class QtCrawlerEngine(ServerBase):

    def __init__(self):
        super(QtCrawlerEngine, self).__init__('qt_crawler')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = QtCrawler(task_id, self.mysql_host, self.mysql_db,
                               self.mysql_user, self.mysql_password,
                               self.mongo_db, self.mongo_host, self.mongo_port,
                               self.mongo_user, self.mongo_password, self.message_other_engine,
                               self.write_process_pid, self.remove_process_pid)
            engine.start()
            self.start_thread_work(engine, task_id)
        except Exception, e:
            sys.stderr.write('%s  %s  task_id: %s: \n' %
                             (time.ctime(), OtherError(e, 'engine_start'), task_id))
            traceback.print_exc()
            task_start_time = self.mysql_handle.get_task_last_time(task_id)
            if task_start_time is not False:
                self.mysql_handle.update_engine_state(
                    task_id, task_start_time, 'qt_crawler', 0)
            os._exit(0)

    def start_thread_work(self, engine, task_id):

        t = threading.Thread(
            target=self.check_engine_live, args=(engine, task_id,))
        t.start()

    def check_engine_live(self, engine, task_id):
        '''
        执行线程工作
        '''
        start_time = time.time()
        sys.stdout.write(
            '%s  engine stuck check start task_id: %s\n' % (time.ctime(), task_id))
        request_url = ''
        # save struct check log
        task_callback_path = '/tmp/' + \
            str(task_id) + '_qt_callback.txt'
        while True:
            time.sleep(60)
            if os.path.isfile(task_callback_path):
                f = open(task_callback_path, 'r')
                current_context = f.readline()
                f.close()
                if current_context != '':
                    current_context = current_context.split(' ')
                else:
                    continue
            else:
                break
            # 两个相隔时间 文件值没有变，且所有待保存网页都已发出请求, 说明卡死
            if current_context[0] == request_url:
                try:
                    sys.stdout.write(
                        '%s  qt_engine struct, wait kill, task_id: %s\n' %
                        (time.ctime(), task_id))
                    run_time = int(time.time() - start_time)
                    engine.update_finish_state(int(current_context[1]), run_time)
                    os.system('kill -9 ' + current_context[2])
                    self.remove_process_pid(task_id)
                    os.remove(task_callback_path)
                    sys.stdout.write(
                        '%s  kill achieved: %s\n' % (time.ctime(), task_id))
                    break
                except:
                    sys.stderr.write(
                        '%s  error to kill: %s, task_id: %s\n' %
                        (time.ctime(), current_context[2], task_id))
                    traceback.print_exc()
                    break
            else:
                # file_context 记录本次的url
                request_url = current_context[0]
        sys.stdout.write('%s engine stuck check quit task_id: %s: \n' %
                         (time.ctime(), task_id))

if __name__ == '__main__':
    qtcrawler_engine = QtCrawlerEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            qtcrawler_engine.start()
        elif 'stop' == sys.argv[1]:
            qtcrawler_engine.stop()
        elif 'restart' == sys.argv[1]:
            qtcrawler_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
