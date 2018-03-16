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

from config_read import Config
from server_session import _ServerSession
from daemonize import _Daemonize


class ServerBase(_Daemonize):

    def __init__(self, server_name):
        super(ServerBase, self).__init__()
        self.server_name = server_name
        self.read_config()  # 读取 数据库服务器ip，端口(默认)，数据库名,用户名和密码
        # 服务之间通信协议定义，由short int和int构成，分别代表消息类型和任务ID，
        self.message_struct = 'HI'
        message_size = struct.calcsize(self.message_struct)
        self.server_session = _ServerSession(self.server_ip,
                                             self.server_port, self.server_type,
                                             self.server_num, self.mysql_host, self.mysql_user,
                                             self.mysql_password, self.mysql_db, message_size)

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
        self.interval = user_config.phishtank.interval
        self.download_url = user_config.phishtank.download_url    

    def start_operation(self):

        self.server_session.register_sever()
        self.server_session.start_update_state()

    def stop_operation(self):
        self.server_session.over_sever()

if __name__ is '__main__':
    detcet_server = ServerBase('phishing_clawer')
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
