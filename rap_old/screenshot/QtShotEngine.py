#!/usr/bin/env python
# coding: utf-8
import sys
import time
import os
import json
import traceback
import threading
import beanstalkc
from server_base.daemonize import _Daemonize
from qtscreenshot_start import QtShot
qtshot = str(1)
_RENUM = 10


class QtShotEngine(_Daemonize):

    def __init__(self):
        super(QtShotEngine, self).__init__()
        self.thread_stop = False    # self.thread_stop 为True时停止检测线程
        self.flags = 0
        self.repeat_num = 0
        self.thread_running = False
        self.job_body = {}

    def _decode_dict(self, data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                pass
            elif isinstance(value, dict):
                value = self._decode_dict(value)
            rv[key] = value
        return rv

    def handle_pic(self):
        pass

    def start_operation(self):
        global _RENUM
        try:
            bean = beanstalkc.Connection('192.168.8.55', 11300)
            bean.watch('test')
            bean.ignore('default')
        except:
            sys.stderr.write('Can not connect to beanstalk server')
            return
        while True:
            try:
                job_msg = bean.reserve(timeout=60)
                assert job_msg
            except:
                self.thread_stop = True
                continue

            try:
                self.thread_stop = False
                self.repeat_num = 0
                self.job_body = json.loads(
                    job_msg.body, object_hook=self._decode_dict)
                if self.thread_running is False:
                    self.start_thread_work()
                if 'method' not in self.job_body:
                    sys.stderr.write('Abort message without method')
                elif self.job_body['method'] == 'manual':
                    try:
                        engine = QtShot(self.job_body, qtshot, self.write_process_pid)
                        engine.start()
                        engine.join()
                        while self.flags == 1 and self.repeat_num <= _RENUM:
                            self.flags = 0
                            print 'rerere'
                            if self.thread_running is False:
                                self.start_thread_work()
                            engine = QtShot(self.job_body, qtshot, self.write_process_pid)
                            engine.start()
                            engine.join()
                        if self.repeat_num > _RENUM:
                            print 222222
                        else:
                            self.handle_pic()
                    except:
                        traceback.print_exc()
                else:
                    sys.stderr.write('Abort message with method = ' +
                                     job_body['method'])
            except:
                traceback.print_exc()
            finally:
                try:
                    job_msg.delete()
                except beanstalkc.CommandFailed:
                    pass

    def start_thread_work(self):
        t = threading.Thread(
            target=self.check_engine_live)
        t.start()

    def check_engine_live(self):
        '''
        执行线程工作
        '''
        self.thread_running = True
        start_time = time.time()
        sys.stdout.write(
            '%s  子线程启动:\n' % (time.ctime()))
        request_url = ''
        pid = ''
        task_callback_path = '/tmp/' + qtshot + '_qt_callback.txt'
        while not self.thread_stop:
            time.sleep(100)
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
            if not self.thread_stop:
                if current_context[0] == request_url and current_context[1] == pid:
                    self.flags = 1
                    self.repeat_num += 1
                    try:
                        try:
                            os.system('kill -9 ' + current_context[1])
                        except:
                            pass
                        os.remove(task_callback_path)
                        sys.stdout.write(
                            '%s  kill achieved:\n' % (time.ctime()))
                        break
                    except:
                        sys.stderr.write(
                            '%s  error to kill: %s\n' %
                            (time.ctime(), current_context[1]))
                        traceback.print_exc()
                        break
                else:
                    request_url = current_context[0]
                    pid = current_context[1]
        print '子线程关闭'
        self.thread_running = False

if __name__ == '__main__':
    qtcrawler_engine = QtShotEngine()
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
