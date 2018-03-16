#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import sys
import time
import threading
import traceback

sys.path.append('../server_base')

from ServerBase import ServerBase
from web_save_start import WebSavestart
from errors import OtherError


class WebSaveEngine(ServerBase):

    def __init__(self):
        super(WebSaveEngine, self).__init__('web_save')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = WebSavestart(task_id, self.mysql_host, self.mysql_db,
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
                    task_id, task_start_time, 'web_save', 0)
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
        callback_last_time = ''
        resource_num = ''
        # save struct check log
        task_callback_path = '/tmp/' + str(task_id) + '_callback.txt'
        # save already saved url
        task_saved_urls_path = '/tmp/' + str(task_id) + '_saved_urls.txt'
        while True:
            time.sleep(60)
            if os.path.isfile(task_callback_path):
                f = open(task_callback_path, 'r')
                current_context = f.readline()
                f.close()
                if current_context != '':
                    current_context = current_context.split('-')
                else:
                    continue
            else:
                break
            # 两个相隔时间 文件值没有变，且所有待保存网页都已发出请求, 说明卡死
            # print current_context, callback_last_time
            if current_context[2] == callback_last_time and current_context[1] == resource_num:
                try:
                    run_time = int(time.time() - start_time)
                    # web_save_engine struct
                    sys.stderr.write(
                        '%s  web_save_engine struct, wait kill, task_id: %s\n' %
                        (time.ctime(), task_id))
                    saved_urls_file = open(task_saved_urls_path, 'r')
                    download_urls = saved_urls_file.readlines()
                    request_num = len(download_urls)
                    ulist = []
                    for line in download_urls:
                        line = line[:-1]           # delete '\n'
                        ulist.append(line.split(' '))
                    saved_urls_file.close()
                    engine.update_finished_state(
                        ulist, run_time, request_num)   # 完成后更新状态
                    os.system('kill -9 ' + current_context[0])
                    os.remove(task_callback_path)
                    os.remove(task_saved_urls_path)
                    sys.stderr.write(
                        '%s  kill achieved: %s\n' % (time.ctime(), task_id))
                    break
                except:
                    sys.stderr.write(
                        '%s  error to kill: %s, task_id: %s\n' %
                        (time.ctime(), current_context[0], task_id))
                    traceback.print_exc()
                    break
            else:
                # file_context 记录本次的url
                resource_num = current_context[1]
                callback_last_time = current_context[2]
        sys.stdout.write('%s engine stuck check quit task_id: %s: \n' %
                         (time.ctime(), task_id))

if __name__ == '__main__':
    web_save_engine = WebSaveEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            web_save_engine.start()
        elif 'stop' == sys.argv[1]:
            web_save_engine.stop()
        elif 'restart' == sys.argv[1]:
            web_save_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
