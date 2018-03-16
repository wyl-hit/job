#!/usr/bin/env python
# coding: utf-8

import sys
import time
import os
import traceback

sys.path.append('../server_base')
from ServerBase import ServerBase
from structure_start import StructureStart
from errors import OtherError


class StructureEngine(ServerBase):

    def __init__(self):
        super(StructureEngine, self).__init__('structure')

    def engine_start(self, task_id):
        sys.stdout.write(
            '%s  |*|receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = StructureStart(task_id, self.mysql_host, self.mysql_db,
                                    self.mysql_user, self.mysql_password,
                                    self.mongo_db, self.mongo_host, self.mongo_port,
                                    self.mongo_user, self.mongo_password, self.message_other_engine,
                                    self.write_process_pid, self.remove_process_pid,
                                    self.structure_num_compare_k, self.structure_num_compare_b,
                                    self.structure_area_compare_k, self.structure_area_compare_b)
            engine.start()
        except Exception, e:
            sys.stderr.write('%s  %s  task_id: %s: \n' %
                             (time.ctime(), OtherError(e, 'engine_start'), task_id))
            traceback.print_exc()
            task_start_time = self.mysql_handle.get_task_last_time(task_id)
            if task_start_time is not False:
                self.mysql_handle.update_engine_state(
                    task_id, task_start_time, 'structure', 0)
            os._exit(0)

if __name__ == '__main__':
    structure_engine = StructureEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            structure_engine.start()
        elif 'stop' == sys.argv[1]:
            structure_engine.stop()
        elif 'restart' == sys.argv[1]:
            structure_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
