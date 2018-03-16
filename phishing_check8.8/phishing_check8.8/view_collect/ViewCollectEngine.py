#!/usr/bin/python
#-*-coding:utf-8-*-
import os
import sys
import time
import traceback

sys.path.append('../server_base')
current_path = sys.path[0]
from ServerBase import ServerBase
from view_collect_start import View_start
from errors import OtherError


class ViewCollectEngine(ServerBase):

    def __init__(self):

        super(ViewCollectEngine, self).__init__('view_collect')

    def engine_start(self, task_id):
        global current_path
        sys.stdout.write(
            '%s  |*|view receive task_id|*|: %s\n' % (time.ctime(), task_id))
        try:
            engine = View_start(task_id, current_path, self.mysql_host, self.mysql_db,
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
                    task_id, task_start_time, 'view_collect', 0)
            os._exit(0)


if __name__ == '__main__':
    view_engine = ViewCollectEngine()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            view_engine.start()

            # title_engine.start_thread_work()
        elif 'stop' == sys.argv[1]:
            view_engine.stop()
        elif 'restart' == sys.argv[1]:
            view_engine.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)
