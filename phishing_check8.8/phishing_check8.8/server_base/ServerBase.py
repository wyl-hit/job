#!/usr/bin/env python
# coding: utf-8
'''
系统服务守护进程基类
author：邹新一
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
import socket
import threading
import struct
import traceback

from errors import SocketError, OtherError
from mysql_handle import MysqlOperate
from config_read import Config


class ServerBase(object):

    def __init__(self, server_name, ip='127.0.0.1', pidfile='/dev/null',
                 stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', server_num=5):
        self.server_name = server_name
        self.log_path = sys.path[0] + '/log/'
        self.stdin = stdin
        self.pidfile = self.log_path + \
            'engine.pid'  # 进程文件，记录守护进程的进程号，避免重复启动
        self.stdout = self.log_path + \
            'engine_stdout.log'  # 标准输入流
        self.stderr = self.log_path + \
            'engine_stderr.log'  # 标准输出流
        self.child_process_pids = self.log_path + \
            'engine_pids/'  # save child process pid
        self.server_ip = ip  # 守护进程的ip
        self.server_port = 0  # 监听的端口号
        self.server_type = ""  # 服务类型
        self.server_num = server_num  # 能接受链接的服务数量，socket listen 数量
        self.mysql_host = ""  # mysql_数据库ip
        self.mysql_db = ""  # mysql_数据库名
        self.mysql_user = ""  # mysql_用户名
        self.mysql_password = ""  # mysql_数据库密码
        self.mongo_db = ''
        self.mongo_host = ''
        self.mongo_port = ''
        self.mongo_user = ''
        self.mongo_password = ''

        self.try_send_message_num = 3
        # structure compare engine config
        self.structure_num_compare_k = 0
        self.structure_num_compare_b = 0
        self.structure_area_compare_k = 0
        self.structure_area_compare_b = 0
        # 服务之间通信协议定义，由short int和int构成，分别代表消息类型和任务ID，
        self.MESSAGE_SIZE = struct.calcsize('HI')
        self.read_config()  # 读取 数据库服务器ip，端口(默认)，数据库名,用户名和密码
        self.mysql_handle = MysqlOperate(self.mysql_db, self.mysql_host,
                                         self.mysql_user, self.mysql_password)
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
        pidfiles_path = self.log_path + 'engine_pids/'
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
        self.run_server()  # 启动守护进程的服务，首先注册并用线程更新，然后监听端口

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

    def stop(self):
        '''
        关闭守护进程
        '''
        # kill all child task process
        pidfiles_path = self.log_path + 'engine_pids/'
        file_list = os.listdir(pidfiles_path)
        for file_name in file_list:
            self.kill_process(pidfiles_path + file_name)
        # kill Daemon process
        self.kill_process(self.pidfile)
        self.over_sever()
        sys.exit(1)

    def write_process_pid(self, task_id):
        '''
        write task_process pid to file, in /engine_pids/...
        '''
        pid = str(os.getpid())
        pidfile_path = self.log_path + 'engine_pids/' + str(task_id)
        file(pidfile_path, 'w+').write('%s\n' % pid)

    def remove_process_pid(self, task_id):
        '''
        remove task_process pid file, in /engine_pids/...
        '''
        pidfile_path = self.log_path + 'engine_pids/' + str(task_id)
        if os.path.exists(pidfile_path):
            os.remove(pidfile_path)

    def kill_task_process(self, task_id):
        '''
        use task_id stop task, kill task_process
        '''
        pidfile_path = self.log_path + 'engine_pids/' + str(task_id)
        self.kill_process(pidfile_path)

    def restart(self):
        '''
        重启守护进程
        '''
        self.stop()
        self.start()

    def read_config(self):
        '''
        读取配置文件
        '''
        config_catalog = '../config'
        config_name = self.server_name + '_conf.yaml'
        config_path = os.path.join(config_catalog, config_name)
        if os.path.exists(config_path):
            user_config = Config(config_path)  # 导出配置文件到user_config对象
        else:
            sys.stderr.write('%s  config file not exist\n' % (time.ctime(),))
            sys.exit(1)
        self.server_ip = user_config.server.ip
        self.server_port = user_config.server.port
        self.server_type = user_config.server.type
        self.server_num = user_config.server.server_num
        self.mysql_host = user_config.mysql.mysql_host
        self.mysql_db = user_config.mysql.mysql_db
        self.mysql_user = user_config.mysql.mysql_user
        if user_config.mysql.mysql_password is not None:
            self.mysql_password = user_config.mysql.mysql_password
        self.mongo_db = user_config.mongo.mongo_db
        self.mongo_host = user_config.mongo.mongo_host
        self.mongo_port = user_config.mongo.mongo_port
        self.mongo_user = user_config.mongo.mongo_user
        if user_config.mongo.mongo_password is not None:
            self.mongo_password = user_config.mongo.mongo_password
        if self.server_name is 'structure':
            self.structure_num_compare_k = user_config.structure.structure_num_compare_k
            self.structure_num_compare_b = user_config.structure.structure_num_compare_b
            self.structure_area_compare_k = user_config.structure.structure_area_compare_k
            self.structure_area_compare_b = user_config.structure.structure_area_compare_b

    def register_sever(self):
        '''
        守护进程(服务)在数据库server_live表中注册信息
        '''
        current_time = time.strftime(
            '%Y-%m-%d %H:%M', time.localtime(time.time()))
        table_name = 'server_live'
        fields = ['*']  # wait to select fields
        # select condition  wheres={field:[value,field_type]}
        wheres = {
            'ip': [self.server_ip, 's'],
            'port': [self.server_port, 's']}
        result = self.mysql_handle.require_get(
            table_name, fields, wheres, 'select', 'one', 0)
        table_name = 'server_live'
        fields = {'ip': [self.server_ip, 's'],
                  'port': [self.server_port, 's'],
                  'type': [self.server_type, 's'],
                  'status': [1, 'd'],
                  'time': [current_time, 's']}
        if result is None:
            result = self.mysql_handle.require_post(
                table_name, fields, {}, 'insert')
        else:
            table_name_del = 'server_live'
            wheres_del = {
                'ip': [self.server_ip, 's'],
                'port': [self.server_port, 's']}
            self.mysql_handle.require_post(
                table_name_del, {}, wheres_del, 'delete')
            result = self.mysql_handle.require_post(
                table_name, fields, {}, 'insert')
        if result is True:
            sys.stdout.write('%s: server register\n' % (time.ctime(),))

    def update_sever(self):
        '''
        执行线程工作，定时更新数据库，记录服务存活
        '''
        table_name = 'server_live'
        wheres = {'ip': [self.server_ip, 's'],
                  'port': [self.server_port, 's']}
        while True:
            time.sleep(30)
            current_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            fields = {'time': [current_time, 's']}
            self.mysql_handle.require_post(
                table_name, fields, wheres, 'update')

    def over_sever(self):
        '''
        守护进程(服务)将之前注册在数据库server_live表中信息删除。
        '''
        table_name = 'server_live'
        wheres = {'ip': [self.server_ip, 's'],
                  'port': [self.server_port, 's']}
        result = self.mysql_handle.require_post(
            table_name, {}, wheres, 'delete')
        if result is True:
            sys.stdout.write('%s: server logout\n' % (time.ctime(),))

    def start_update_state(self):
        '''
        开启子线程，定期检查服务是否存活
        '''
        t1 = threading.Thread(target=self.update_sever)
        t1.start()

    def run_server(self):
        '''
        运行相应服务，建立socket连接，监听端口
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write(
                '%s\n' % SocketError(msg, 'run_server socket create'))
            sys.exit()
        # port re run
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((self.server_ip, self.server_port))  # 绑定于端口和ip
            sock.listen(self.server_num)
        except socket.error, msg:
            sys.stderr.write('%s' % SocketError(msg, 'run_server bind listen'))
            sys.stderr.write('  ip: %s port: %s \n' %
                             (self.server_ip, self.server_port))
            sys.exit()
        self.register_sever()  # 注册服务
        self.start_update_state()  # 更新服务存活状态
        sys.stdout.write('%s: monitor port %s\n' %
                         (time.ctime(), self.server_port))
        sys.stdout.write(
            '————————————————————————————————————————————————————\n')
        sys.stderr.write(
            '————————————————————————————————————————————————————\n')
        while True:
            conn, addr = sock.accept()
            sys.stdout.write('%s  request from : %s: ' %
                             (time.ctime(), addr))
            try:
                response_thread = threading.Thread(
                    target=self.response_server, args=(conn,))  # 创建线程
            except Exception, e:
                sys.stderr.write(
                    '%s\n' % OtherError(e, 'ServerBase run_server response message'))
            response_thread.start()  # 执行线程
        sock.close()

    def response_server(self, conn):
        '''
        响应当前服务接收到的请求，在子线程中完成，完成并行响应
        '''
        try:
            message = conn.recv(self.MESSAGE_SIZE)
            if message[0] is 'q':  # 用来解析客户端发来的请求，请求开始任务格式为qr+任务ID
                # conn.settimeout(5) #服务端等待客户端三秒
                sys.stdout.write('client message : %s \n' %
                                 (message, ))
                task_id = int(message[2:])
                if len(message) == 2:
                    conn.send('failed')
                    sys.stderr.write(
                        '%s  task request error, message: %s' % (time.ctime(), message))
                elif message[1] is 'r':
                    request_result = self.web_request_start(task_id)
                    if request_result is True:
                        conn.send('succeed')
                    else:
                        conn.send('failed')
                        sys.stderr.write(
                            '%s  task request error, message: %s' % (time.ctime(), message))
                elif message[1] is 's':
                    request_result = self.web_request_stop(task_id)
                    if request_result is True:
                        conn.send('succeed')
                    else:
                        conn.send('failed')
                        sys.stderr.write(
                            '%s  task request error, message: %s' % (time.ctime(), message))
            elif len(message) is self.MESSAGE_SIZE:  # 响应各服务之间消息响应
                message_type, task_id = struct.unpack('HI', message)
                sys.stdout.write('engine message_type : %s task_id : %s \n' %
                                 (message_type, task_id))
                if message_type is 0:  # 主控任务开启其他引擎服务
                    self.engine_start(task_id)
                    conn.send('engine start')
                if message_type is 1:  # 主控任务暂停其他引擎服务
                    self.engine_stop(task_id)
                    conn.send('engine stop')
                if message_type is 2:  # control response filtrated
                    self.filtrate_to_control(task_id)
                if message_type is 3:
                    self.web_save_to_control(task_id)
                if message_type is 4:
                    self.qt_crawler_to_control(task_id)
                if message_type is 5:
                    self.detect_to_control(task_id)
                if message_type is 6:
                    self.check_to_control(task_id)
                if message_type is 7:
                    self.feature_save_to_control(task_id)
                if message_type is 8:
                    self.engine_failure_to_control(task_id)
                if message_type is 9:
                    self.engine_win_over_to_control(task_id)
                if message_type is 10:
                    self.view_collect_to_control(task_id)
            else:
                conn.send('message error')
                sys.stderr.write(
                    'receive error message: %s in response_server\n' % message)
        except:
            ip_port = conn.getpeername()
            sys.stderr.write('%s  ServerBase response_server, message from: ip: %s  port: %s \n' % (
                time.ctime(), ip_port[0], ip_port[1]))
            conn.send('task send error')
            traceback.print_exc()
        conn.close()

    def send_message(self, message_type, task_id, goal_ip, goal_port):
        '''
        向其他服务发送消息
        '''
        try:
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write(
                '%s\n' % SocketError(msg, 'send_message socket create'))
            return False
        try:
            send_sock.connect((goal_ip, goal_port))
        except socket.error, msg:
            sys.stderr.write('%s' % SocketError(msg, 'send_message connect'))
            return False
        try:
            message = struct.pack('HI', message_type, task_id)
            send_sock.send(message)  # send message
        except socket.error, msg:
            sys.stderr.write(
                '%s' % SocketError(msg, 'send_message send message'))
            return False
        send_sock.close()
        return True

    def message_other_engine(self, message_type, engine_types, task_id, send_num='one'):
        '''
        send message to multiple engine

        loop self.try_send_message_num,
            loop engine in engine_types
                get engine ip_port from current server,
                    and send message to specified engine
                if win, send_win_engine append engine
            all engine send win, return
            engine_types remove send_win_engine

        send_num: all 将当前任务发送给指定编号的所有引擎
                  one 将当前任务发送给指定编号的一个引擎
        '''
        try_num = self.try_send_message_num
        wait_send_num = len(engine_types)  # need引擎数量
        table_name = 'server_live'
        fields = ['ip', 'port']
        while try_num:
            send_win_engine = []
            for engine_type in engine_types:
                wheres = {'type': [engine_type, 's'],
                          'status': [1, 'd']}
                ip_ports = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'all')
                if ip_ports is not False:
                    for ip_port in ip_ports:
                        send_result = self.send_message(
                            message_type=message_type, task_id=task_id,
                            goal_ip=ip_port['ip'], goal_port=int(ip_port['port']))
                        if send_result is True:
                            sys.stdout.write('%s  message ip: %s, port: %s, engine_type: %s, message_type: %s, for task: %d\n' %
                                             (time.ctime(), ip_port['ip'], ip_port['port'],
                                              engine_type, message_type, task_id))
                            if send_num == 'one':
                                wait_send_num -= 1
                                send_win_engine.append(engine_type)
                                break
                        else:
                            sys.stderr.write('%s  error to message other engine ip: %s,  port: %s,  type: %s,  for task: %d\n' %
                                             (time.ctime(), ip_port['ip'], ip_port['port'],
                                              engine_type, task_id))
                    if send_num == 'all':
                        wait_send_num -= 1
                        send_win_engine.append(engine_type)
                else:
                    sys.stdout.write('%s  no free NO. %s engine ,task_id: %s\n' %
                                     (time.ctime(), engine_type, task_id))
            if wait_send_num == 0:
                return True
            else:
                for engine_type in send_win_engine:
                    engine_types.remove(engine_type)
                try_num -= 1
        sys.stderr.write('%s  send message fail, engine type: %s,  for task: %d\n' %
                         (time.ctime(), engine_types, task_id))
        return False

    def web_request_start(self, task_id):
        '''
        主控服务响应前台客户端任务开始请求
        '''
        pass

    def web_request_stop(self, task_id):
        '''
        主控服务响应前台客户端任务结束请求
        '''
        pass

    def engine_start(self, task_id):
        '''
        message 0: 引擎服务响应主控进程任务开始请求
        '''
        pass

    def engine_stop(self, task_id):
        '''
        message 1: 引擎服务响应主控进程任务关闭请求
        '''
        self.kill_task_process(task_id)

    def filtrate_to_control(self, task_id):
        '''
        message 2: filtrate engine finished message control
        start web_save
        '''
        pass

    def web_save_to_control(self, task_id):
        '''
        message 3: web_save engine finished message control
        start title or qt_crawler
        '''
        pass

    def qt_crawler_to_control(self, task_id):
        '''
        message 4: qt_crawler engine finished message control
        start structure or view
        '''
        pass

    def detect_to_control(self, task_id):
        '''
        message 5: detect(domain or search) engine finished message control,
        start check
        '''
        pass

    def check_to_control(self, task_id):
        '''
        message 6: check(title or structure or view) engine finished message control,
        over task
        '''
        pass

    def feature_save_to_control(self, task_id):
        '''
        message 7: task_type 4 finaish
        over task
        '''
        pass

    def engine_failure_to_control(self, task_id):
        '''
        message 8: engine failure, over task
        over task
        '''
        pass

    def engine_win_over_to_control(self, task_id):
        '''
        message 9: engine over, After engine need not start, over task
        over task
        '''
        pass

    def view_collect_to_control(self, task_id):
        '''
        message 10: view_collect engine over, After start view_emd
        '''
        pass


if __name__ is '__main__':
    detcet_server = ServerBase()
    if len(sys.argv) is 2:
        if 'start' is sys.argv[1]:
            detcet_server.start()
        elif 'stop' is sys.argv[1]:
            detcet_server.stop()
        elif 'restart' is sys.argv[1]:
            detcet_server.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
