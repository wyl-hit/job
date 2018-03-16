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
import struct

from errors import ConfigurationError
try:
    from mysql_handle import MysqlOperate
except ImportError:
    raise ConfigurationError('Mysql_Operate')
from config_read import Config
from server_session import _ServerSession
from daemonize import _Daemonize


class ServerSession(_ServerSession):

    def __init__(self, server_base, message_struct, server_ip, server_port,
                 server_type, server_num, mysql_host, mysql_user,
                 mysql_password, mysql_db):
        self.message_struct = message_struct
        self.message_size = struct.calcsize(self.message_struct)
        super(ServerSession, self).__init__(server_ip, server_port,
                                            server_type, server_num, mysql_host,
                                            mysql_user, mysql_password, mysql_db,
                                            self.message_size)
        self.server_base = server_base

    def structure_message(self, message_type, args):
        message = struct.pack(self.message_struct, message_type, args[0])
        return message

    def analysis_message(self, conn, massage):
        if massage[0] is 'q':  # 用来解析客户端发来的请求，请求开始任务格式为qr+任务ID
            # conn.settimeout(5) #服务端等待客户端三秒
            task_id = int(massage[2:])
            if massage[1] is 'r':
                self.server_base.web_request_start(task_id)
                conn.send('task start')
            if massage[1] is 's':
                request_result = self.server_base.web_request_stop(task_id)
                if request_result is True:
                    conn.send('task stop win')
                else:
                    conn.send('task stop false')
        elif len(massage) is self.message_size:  # 响应各服务之间消息响应
            message_type, task_id = struct.unpack(self.message_struct, massage)
            if message_type is 0:  # 主控任务开启其他引擎服务
                self.server_base.engine_start(task_id)
                conn.send('engine start')
            if message_type is 1:  # 主控任务暂停其他引擎服务
                self.server_base.engine_stop(task_id)
                conn.send('engine stop')
            if message_type is 2:  # control response filtrated
                self.server_base.filtrate_to_control(task_id)
                conn.send('engine start')
            if message_type is 3:
                self.server_base.web_save_to_control(task_id)
                conn.send('engine start')
            if message_type is 4:
                self.server_base.qt_crawler_to_control(task_id)
                conn.send('engine start')
            if message_type is 5:
                self.server_base.detect_to_control(task_id)
                conn.send('engine start')
            if message_type is 6:
                self.server_base.check_to_control(task_id)
                conn.send('engine start')
        else:
            conn.send('message error')
            sys.stderr.write(
                'receive error message: %s in response_server\n' % massage)


class ServerBase(_Daemonize):

    def __init__(self, server_name):
        super(ServerBase, self).__init__()
        self.server_name = server_name
        self.read_config()  # 读取 数据库服务器ip，端口(默认)，数据库名,用户名和密码
        # 服务之间通信协议定义，由short int和int构成，分别代表消息类型和任务ID，
        self.message_struct = 'HI'
        self.mysql_handle = MysqlOperate(self.mysql_db, self.mysql_host,
                                         self.mysql_user, self.mysql_password)
        self.server_session = ServerSession(self, self.message_struct, self.server_ip, self.server_port, self.server_type,
                                            self.server_num, self.mysql_host, self.mysql_user,
                                            self.mysql_password, self.mysql_db)

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
        else:
            self.mysql_password = ''
        self.mongo_db = user_config.mongo.mongo_db
        self.mongo_host = user_config.mongo.mongo_host
        self.mongo_port = user_config.mongo.mongo_port
        self.mongo_user = user_config.mongo.mongo_user
        if user_config.mongo.mongo_password is not None:
            self.mongo_password = user_config.mongo.mongo_password
        else:
            self.mongo_password = ''
        if self.server_name is 'structure':
            self.structure_num_compare_k = user_config.structure.structure_num_compare_k
            self.structure_num_compare_b = user_config.structure.structure_num_compare_b
            self.structure_area_compare_k = user_config.structure.structure_area_compare_k
            self.structure_area_compare_b = user_config.structure.structure_area_compare_b

    def start_operation(self):
        self.server_session.run_server()

    def stop_operation(self):
        self.server_session.over_sever()

    def message_other_engine(self, server_types, message_type, task_id):
        message_arg = [message_type, task_id]
        self.server_session.message_other_engine(server_types, message_arg)

    def web_request_start(self, task_id):
        '''
        主控服务响应前台客户端任务开始请求
        '''
        pass

    def web_request_stop(self, task_id):
        '''
        主控服务响应前台客户端任务结束请求
        '''
        self.kkill_task_process()

    def engine_start(self, task_id):
        '''
        message 0: 引擎服务响应主控进程任务开始请求
        '''
        pass

    def engine_stop(self, task_id):
        '''
        message 1: 引擎服务响应主控进程任务关闭请求
        '''
        pass

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

if __name__ == '__main__':
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
