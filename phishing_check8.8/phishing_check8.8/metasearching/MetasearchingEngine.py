#!/usr/bin/env python
# coding: utf-8

import sys
import time
sys.path.append('../server_base')
from ServerBase import ServerBase
from metasearching_start import Metasearching_start
from errors import OtherError
import traceback


class MetasearchingEngine(ServerBase):

    def __init__(self):
        super(MetasearchingEngine, self).__init__('metasearching')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|MetasearchingEngine receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = Metasearching_start(task_id, self.stdout, self.stderr, self.mysql_host,
                                         self.mysql_user, self.mysql_password, self.mysql_db,
                                         self.mongo_db, self.mongo_host, self.mongo_port,
                                         self.mongo_user, self.mongo_password,
                                         self.message_other_engine)
            engine.start()
        except Exception, e:
            sys.stderr.write('%s  %s  task_id: %s: \n' %
                             (time.ctime(), OtherError(e, 'engine_start'), task_id))
            traceback.print_exc()

if __name__ == '__main__':
    metasearching_engine = MetasearchingEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            metasearching_engine.start()
        elif 'stop' == sys.argv[1]:
            metasearching_engine.stop()
        elif 'restart' == sys.argv[1]:
            metasearching_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
