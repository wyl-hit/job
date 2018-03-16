#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
import traceback
import threading
sys.path.append('../server_base')
from ServerBase import ServerBase
from domain_start import DomainStart
from errors import OtherError


class DomainEngine(ServerBase):

    def __init__(self):
        super(DomainEngine, self).__init__('domain')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = DomainStart(task_id, self.mysql_host, self.mysql_db,
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
                    task_id, task_start_time, 'domain', 0)
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
        last_request_url = ''
        # save struct check log
        domain_save_path = '/tmp/' + \
            str(task_id) + '_domain_request_urls.txt'
        domain_live_path = '/tmp/' + \
            str(task_id) + '_domain_live.txt'

        while True:
            time.sleep(60)
            if os.path.isfile(domain_live_path):
                f = open(domain_live_path, 'r')
                current_context = f.readline()
                f.close()
                if current_context != '':
                    current_context = current_context.split(' ')
                else:
                    continue
            else:
                break
            # 两个相隔时间 文件值没有变，且所有待保存网页都已发出请求, 说明卡死
            # print current_context, callback_last_time
            if last_request_url == current_context[0]:
                try:
                    run_time = int(time.time() - start_time)
                    sys.stderr.write(
                        '%s  domain_engine struct, wait kill, task_id: %s\n' %
                        (time.ctime(), task_id))
                    exist_list = []
                    if os.path.isfile(domain_save_path):
                        save_file = open(domain_save_path, 'r')
                        url_context = save_file.readlines()
                        save_file.close()
                    print 'url_context', url_context
                    for url in url_context:
                        url = url[:-1]           # delete '\n'
                        exist_list.append(url)
                    os.system('kill -9 ' + current_context[1])
                    self.remove_process_pid(task_id)
                    engine.update_finish_state(exist_list, run_time)
                    os.remove(domain_save_path)
                    os.remove(domain_live_path)
                    sys.stderr.write(
                        '%s  kill achieved: %s\n' % (time.ctime(), task_id))
                    break
                except:
                    sys.stderr.write(
                        '%s  error to kill: %s, task_id: %s\n' %
                        (time.ctime(), current_context[1], task_id))
                    traceback.print_exc()
                    break
            else:
                # file_context 记录本次的url
                last_request_url = current_context[0]
        sys.stdout.write('%s engine stuck check quit task_id: %s: \n' %
                         (time.ctime(), task_id))

if __name__ == '__main__':
    domain_engine = DomainEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            domain_engine.start()
        elif 'stop' == sys.argv[1]:
            domain_engine.stop()
        elif 'restart' == sys.argv[1]:
            domain_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
