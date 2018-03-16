#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
import traceback

sys.path.append('../server_base')
from ServerBase import ServerBase
from filtrate_start import FiltrateStart
from errors import OtherError


class FiltrateEngine(ServerBase):

    def __init__(self):
        super(FiltrateEngine, self).__init__('filtrate')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = FiltrateStart(task_id, self.mysql_host, self.mysql_db,
                                   self.mysql_user, self.mysql_password,
                                   self.mongo_db, self.mongo_host, self.mongo_port,
                                   self.mongo_user, self.mongo_password, self.message_other_engine,
                                   self.write_process_pid, self.remove_process_pid)
            engine.start()
        except Exception, e:
            sys.stderr.write('%s  %s  task_id: %s: \n' %
                             (time.ctime(), OtherError(e, 'engine_start'), task_id))
            traceback.print_exc()
            task_start_time = self.mysql_handle.get_task_last_time(task_id)
            if task_start_time is not False:
                self.mysql_handle.update_engine_state(
                    task_id, task_start_time, 'filtrate', 0)
            os._exit(0)

if __name__ == '__main__':
    filtrate_engine = FiltrateEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            filtrate_engine.start()
        elif 'stop' == sys.argv[1]:
            filtrate_engine.stop()
        elif 'restart' == sys.argv[1]:
            filtrate_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
