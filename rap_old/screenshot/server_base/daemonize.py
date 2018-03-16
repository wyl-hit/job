#!/usr/bin/env python
# coding: utf-8
'''
系统服务守护进程基类
author：wyl
2015.4.25
输入：
    config目录下配置文件，根据初始化提供的引擎名称拼接路径并读取
功能：创建守护进程，在mysql中动态更新服务存活状态。
      监听指定端口，并根据给定消息格式响应请求，具体响应函数需各引擎重写。并可向其他使用该服务的引擎发送socket消息。
接口：
    start()             启动守护进程
    stop()              关闭守护进程
    restart()           重启守护进程
    register_sever()    守护进程(服务)注册
    start_update_state()  记录服务存活
    run_server()       监听端口信息
    _daemonize          将进程脱离终端，形成守护进程
    read_config()       读取数据库配置文件
启动方式 ：              python XXX.py start 启动守护进程
查看守护进程状态命令：     ps -ef | grep base.py |grep -v grep
关闭方式：               python XXX.py stop
也可使用  kill -9 pid 关闭守护进程，不过还要手动删除 /tmp/*.pid文件 保证下次启动守护进程可以正常启动
'''
import os
import sys
import time
import atexit
import signal


class _Daemonize(object):

    def __init__(self):
        self.log_path = sys.path[0] + '/log/'
        self.pidfile = self.log_path + \
            'engine.pid'  # 进程文件，记录守护进程的进程号，避免重复启动
        self.stdin = '/dev/null'
        self.stdout = self.log_path + \
            'engine_stdout.log'  # 标准输入流
        self.stderr = self.log_path + \
            'engine_stderr.log'  # 标准输出流
        self.child_process_pids = self.log_path + \
            'engine_pids/'  # save child process pid
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    def _daemonize(self, stdin, stdout, stderr):
        '''
        将进程脱离终端，形成守护进程
        '''
        try:
            pid = os.fork()  # 第一次fork，生成子进程，脱离父进程
            if pid > 0:         # pid>0 为父进程
                sys.exit(0)  # 父进程退出
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' %
                             (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")  # 修改工作目录
        os.setsid()  # 设置新的会话连接
        os.umask(0)  # 重新设置文件创建权限

        try:
            pid = os.fork()  # 第二次fork，禁止进程打开终端
            if pid > 0:
                sys.exit(0)  # 父进程退出
        except OSError, e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' %
                             (e.errno, e.strerror))
            sys.exit(1)
        # 重定向文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(stdin, 'r')
        so = file(stdout, 'a+')
        se = file(stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

    def delpid(self):
        '''
        被 stop() 调用 删除进程文件，标志守护进程退出
        '''
        os.remove(self.pidfile)
        pidfiles_path = self.child_process_pids
        file_list = os.listdir(pidfiles_path)
        for file_name in file_list:
            os.remove(pidfiles_path + file_name)

    def start(self):
        '''
        启动守护进程
        '''
        try:  # 检查pid文件是否存在以探测是否存在进程
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())  # pid 文件中 存放守护进程的进程号
            pf.close()
        except IOError:
            pid = None
        if pid:  # 进程文件存在并获取到 守护进程号，说明守护进程已经启动，不会重复启动，退出
            sys.stderr.write(
                'pidfile already exist. Daemon already running!\n')
            sys.exit(1)

        sys.stdout.write(
            '\n————————————————  正在开启，请看日志文件  ———————————————\n')
        # 与控制台脱离, become daemonize
        self._daemonize(self.stdin, self.stdout, self.stderr)
        # 注册退出函数，根据文件pid判断是否存在进程
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)
        if not os.path.exists(self.child_process_pids):
            os.mkdir(self.child_process_pids)
        sys.stdout.write(
            '\n***********************************************************\n')
        sys.stdout.write('%s: engine server start\n' % (time.ctime(),))
        sys.stderr.write(
            '\n***********************************************************\n')
        sys.stderr.write('%s: engine server start\n' % (time.ctime(),))
        self.start_operation()  # 启动守护进程的服务，首先注册并用线程更新，然后监听端口

    def kill_process(self, pid_file):
        '''
        use pid form pid_file to kill precess
        '''
        # 从pid文件中获取pid
        try:
            pf = file(pid_file, 'r')
            pid = pf.read().strip()
            pf.close()
        except IOError:
            pid = None
        if not pid:  # 进程号不存在说明进程已经关闭
            message = '%s  pid_file %s not exist!\n'
            sys.stderr.write(message % (time.ctime(), pid_file))
            return False  # pid_file not exist
        try:
            while 1:
                os.kill(int(pid), 9)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(pid_file):
                    os.remove(pid_file)  # kill杀死进程后，删除进程文件
                message = '%s  pid_file %s kill win!\n'
                sys.stdout.write(message % (time.ctime(), pid_file))
                return True  # kill win
            else:
                print str(err)
            message = '%s  pid_file %s kill error!\n'
            sys.stderr.write(message % (time.ctime(), pid_file))
            return False  # kill error

    def write_process_pid(self):
        '''
        write task_process pid to file, in /engine_pids/...
        '''
        pid = str(os.getpid())
        pidfile_path = self.log_path + 'engine_pids/' + str(pid)
        file(pidfile_path, 'w+').write('%s\n' % pid)

    def stop(self):
        '''
        关闭守护进程
        '''
        # kill all child task process
        pidfiles_path = self.child_process_pids
        file_list = os.listdir(pidfiles_path)
        for file_name in file_list:
            self.kill_process(pidfiles_path + file_name)
        # kill Daemon process
        self.kill_process(self.pidfile)
        self.stop_operation()
        sys.exit(1)

    def restart(self):
        '''
        重启守护进程
        '''
        self.stop()
        self.start()


    def remove_process_pid(self, process_name):
        '''
        remove task_process pid file, in /engine_pids/...
        '''
        pidfile_path = self.child_process_pids + str(process_name)
        if os.path.exists(pidfile_path):
            os.remove(pidfile_path)

    def kill_task_process(self, process_name):
        '''
        use process_name stop task, kill task_process
        '''
        pidfile_path = self.child_process_pids + str(process_name)
        self.kill_process(pidfile_path)

    def start_operation(self):
        pass

    def stop_operation(self):
        pass

if __name__ is '__main__':
    pass
