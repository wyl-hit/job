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
import sys
import time
import socket
import threading
import traceback

from errors import SocketError, OtherError, ConfigurationError
try:
    from mysql_handle import MysqlOperate
except ImportError:
    raise ConfigurationError('Mysql_Operate')


class _ServerSession(object):

    def __init__(self, server_ip='127.0.0.1', server_port='1234', server_type='default',
                 server_num=5, mysql_host='127.0.0.1', mysql_user='root',
                 mysql_password='', mysql_db='test', message_len=''):
        self.server_ip = server_ip  # 守护进程的ip
        self.server_port = server_port  # 监听的端口号
        self.server_type = server_type  # 服务类型
        self.server_num = server_num  # 能接受链接的服务数量，socket listen 数量
        # 服务之间通信协议定义，由short int和int构成，分别代表消息类型和任务ID，
        self.message_len = message_len
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.try_send_message_num = 3

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
        wheres = {
            'ip': [self.server_ip, 's'],
            'port': [self.server_port, 's']}
        while True:
            time.sleep(60)
            current_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
            fields = {'time': [current_time, 's']}
            self.mysql_handle.require_post(
                table_name, fields, wheres, 'update')

    def start_update_state(self):
        '''
        开启子线程，定期检查服务是否存活
        '''
        t1 = threading.Thread(target=self.update_sever)
        t1.start()

    def over_sever(self):
        '''
        守护进程(服务)将之前注册在数据库server_live表中信息删除。
        '''
        table_name = 'server_live'
        wheres = {
            'ip': [self.server_ip, 's'], 'port': [self.server_port, 's']}
        result = self.mysql_handle.require_post(
            table_name, {}, wheres, 'delete')
        if result is True:
            sys.stdout.write('%s: server logout\n' % (time.ctime(),))

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
            sys.stdout.write('%s  request from : %s: \n' %
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
            massage = conn.recv(self.message_len)
            self.analysis_message(conn, massage)
        except:
            ip_port = conn.getpeername()
            sys.stderr.write('%s  ServerBase response_server, message from: ip: %s  port: %s \n' % (
                time.ctime(), ip_port[0], ip_port[1]))
            conn.send('task send error')
            traceback.print_exc()
        conn.close()

    def send_message(self, message_type, args, goal_ip, goal_port):
        '''
        向其他服务发送消息
        '''
        try:
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write(
                '%s\n' % SocketError(msg, 'send_message, socket create'))
            return False
        try:
            send_sock.connect((goal_ip, goal_port))
        except socket.error, msg:
            sys.stderr.write('%s' % SocketError(msg, 'send_message, connect'))
            return False
        try:
            message = self.structure_message(message_type, args)
            send_sock.send(message)  # send message
        except socket.error, msg:
            sys.stderr.write(
                '%s' % SocketError(msg, 'send_message, send message'))
            return False
        send_sock.close()
        return True

    def message_other_engine(self, message_type, server_types, *args):
        '''
        send message to multiple engine

        loop self.try_send_message_num,
            loop engine in engine_types
                get engine ip_port from current server,
                    and send message to specified engine
                if win, send_win_engine append engine
            all engine send win, return
            engine_types remove send_win_engine
        '''
        try_num = self.try_send_message_num
        wait_send_num = len(server_types)  # need引擎数量
        table_name = 'server_live'
        fields = ['ip', 'port']
        while try_num:
            send_win_engine = []
            for server_type in server_types:
                wheres = {'type': [server_type, 's'],
                          'status': [1, 'd']}
                ip_ports = self.mysql_handle.require_get(
                    table_name, fields, wheres, 'select', 'all')
                if ip_ports is not False:
                    for ip_port in ip_ports:
                        send_result = self.send_message(
                            message_type, args, ip_port['ip'], int(ip_port['port']))
                        if send_result is True:
                            sys.stdout.write('%s  message ip: %s, port: %s, server_type: %s\n' %
                                             (time.ctime(), ip_port['ip'], ip_port['port'], server_type))
                            wait_send_num -= 1
                            send_win_engine.append(server_type)
                            break
                        else:
                            sys.stderr.write('%s  error to message other server ip: %s,  port: %s,  type: %s\n' %
                                             (time.ctime(), ip_port['ip'], ip_port['port'], server_type))
                else:
                    sys.stdout.write('%s  no free NO. %s server\n' %
                                     (time.ctime(), server_type))
            if wait_send_num == 0:
                return True
            else:
                for server_type in send_win_engine:
                    server_types.remove(server_type)
                try_num -= 1
                time.sleep(10)
        sys.stdout.write('%s  send message fail, server type: %s\n' %
                         (time.ctime(), server_types))
        return False

    def analysis_message(self, conn, massage):
        pass

    def structure_message(self, args):
        pass

if __name__ is '__main__':
    pass
