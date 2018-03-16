# encoding:utf8
import sys
import os
os.putenv('DISPLAY', ':0.0')
import json
from json import *
import multiprocessing
from PyQt4.QtGui import QApplication
from screen_shot_pyqt import Pagescreen
#from mysql_handle import MysqlOperate
current_path = sys.path[0]

class QtShot(multiprocessing.Process):

    def __init__(self, task, qtshot, write_process_pid):
        super(QtShot, self).__init__()
        # self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
        # mysql_user, mysql_password)
        self.task = task
        self.write_process_pid = write_process_pid
        self.check_file = '/tmp/' + qtshot + '_qt_callback.txt'

    def run(self):
        self.write_process_pid()
        f = open(self.check_file, 'w')
        f.write(self.task['model_url'] + ' ' + str(os.getpid()))
        f.close()

        
        self.app = QApplication(sys.argv)

        self.shot = Pagescreen(self.task)
        sys.exit(self.app.exec_())


if __name__ == '__main__':
    print current_path
