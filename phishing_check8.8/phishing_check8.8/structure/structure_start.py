# encoding:utf8
import sys
import multiprocessing
import time
# import traceback

from structure_compare import StructureCompare
from mongo_handle import Mongo_Operate
from mysql_handle import MysqlOperate


class StructureStart(multiprocessing.Process):

    def __init__(self, task_id, mysql_host, mysql_db,
                 mysql_user, mysql_password, mongo_db, mongo_host,
                 mongo_port, mongo_user, mongo_password,
                 message_other_engine, write_process_pid, remove_process_pid,
                 structure_num_compare_k, structure_num_compare_b,
                 structure_area_compare_k, structure_area_compare_b):
        super(StructureStart, self).__init__()
        self.task_id = task_id
        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.message_other_engine = message_other_engine
        self.write_process_pid = write_process_pid
        self.remove_process_pid = remove_process_pid
        self.structure_num_compare_k = structure_num_compare_k
        self.structure_num_compare_b = structure_num_compare_b
        self.structure_area_compare_k = structure_area_compare_k
        self.structure_area_compare_b = structure_area_compare_b
        self.mongo_db = mongo_db
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password

        # 初始化操作
        self.run_start_time = 0
        self.structure_check_num = 0  # 检查数量
        self.structure_find_num = 0  # 检查到钓鱼url的数量
        self.mongo_operate = Mongo_Operate(mongo_db, mongo_host,
                                           mongo_port, mongo_user,
                                           mongo_password)
        self.read_task_info()

    def read_task_info(self):
        self.task_start_time = self.mysql_handle.get_task_last_time(
            self.task_id)
        saved_urls_iters = self.mysql_handle.read_saved_urls(
            self.task_id, self.mongo_operate)
        self.get_gray_iter = saved_urls_iters['get_gray_iter']
        self.get_monitor_iter = saved_urls_iters['get_monitor_iter']
        self.protected_dict = self.mysql_handle.get_all_protected_feature(
            self.mongo_operate.get_web_tree)
        self.counterfeit_dict = self.mysql_handle.get_all_counterfeit_feature(
            self.mongo_operate.get_web_tree)

    # 任务执行中更新状态
    def update_running_state(self):
        '''
        在mysql中更新探测状态及结果
        '''
        table_name = 'task_result'
        fields = {'structure_check_num': [self.structure_check_num, 'd'],
                  'structure_find_num': [self.structure_find_num, 'd'], }
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')

    def update_finished_state(self):
        '''
        在mysql中更新探测状态及结果
        '''
        run_time = int(time.time()) - int(self.run_start_time)
        table_name = 'task_result'
        fields = {'e_structure_state': [03, 'd'],
                  'structure_run_time': [run_time, 's'],
                  'structure_check_num': [self.structure_check_num, 'd'],
                  'structure_find_num': [self.structure_find_num, 'd']}
        wheres = {'task_id': [self.task_id, 'd'],
                  'start_time': [self.task_start_time, 's']}
        self.mysql_handle.require_post(
            table_name, fields, wheres, 'update')
        self.engine_over_handle()

    def engine_over_handle(self):
        # message to control
        send_result = self.message_other_engine(6, ['00'], self.task_id)
        if send_result is False:  # control engine no response, stop task
            self.mysql_handle.update_task_state(
                self.task_id, self.task_start_time, 0)
        sys.stdout.write(
            '%s |*|engine win over|*|, task_id: %s\n' % (time.ctime(), self.task_id))
        self.remove_process_pid(self.task_id)

    def run_structure_compare(self):
        structure_compare = StructureCompare(self.structure_num_compare_k,
                                             self.structure_num_compare_b,
                                             self.structure_area_compare_k,
                                             self.structure_area_compare_b
                                             )
        while True:
            try:
                gray_url = self.get_gray_iter.next()
                gray_block_list = self.mongo_operate.get_web_tree(
                    gray_url, 'gray')
                # mongo not have tree of url
                if gray_block_list is False or gray_block_list == []:
                    continue
                # cehck to protected
                for protected_url in self.protected_dict.keys():
                    protected_block_list = self.protected_dict[protected_url]
                    if protected_block_list == []:
                        continue
                    check_result = structure_compare.once_compare(
                        protected_block_list, gray_block_list)
                    if check_result == 1:
                        self.structure_find_num += 1
                        self.mysql_handle.undate_gray_list_check_result(
                            gray_url, 'structure', source_url=protected_url)
                        self.mysql_handle.undate_task_result_check_result(
                            self.task_id, self.task_start_time, gray_url, 'structure')
                        break
                # check to counterfeit
                for counterfeit_url in self.counterfeit_dict.keys():
                    counterfeit_block_list = self.counterfeit_dict[counterfeit_url]
                    if counterfeit_block_list == []:
                        continue
                    check_result = structure_compare.once_compare(
                        counterfeit_block_list, gray_block_list)
                    if check_result == 1:
                        self.structure_find_num += 1
                        self.mysql_handle.undate_gray_list_check_result(
                            gray_url, 'structure', counterfeit_url=counterfeit_url)
                        self.mysql_handle.undate_task_result_check_result(
                            self.task_id, self.task_start_time, gray_url, 'structure')
                        break
                self.structure_check_num += 1
                self.update_running_state()
            except StopIteration:
                break

    def run(self):
        # write child process pid to engine pids
        self.write_process_pid(self.task_id)
        self.run_start_time = time.time()
        self.mysql_handle.update_engine_state(
            self.task_id, self.task_start_time, 'structure', 2)
        self.run_structure_compare()
        self.update_finished_state()


if __name__ == '__main__':
    url_list = ['http://www.taobao.com/', 'http://www.vip.com/']
    qtc = QtCrawler(url_list, 6, stdout=0, stderr=0, mysql_host='172.31.159.248', mysql_user='root',
                    mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                    mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='')
    qtc.start()
