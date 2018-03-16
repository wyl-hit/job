# -*- coding: utf-8 -*-
'''
mysql handle base
operation:
    connect
    check_mysql_error
    require_get: select to mysql
    require_post: insert,update to mysql
    ................

time: 2015.6.24
author: xinyi
'''

import sys
import os
import re
import time
import traceback
import threading
from errors import DependencyNotInstalledError, MySQLError
from extra_opration import hash_md5, dns_check
from web_save_path import WebSavePath
from page_shot import CallPageShot
from whois.urlanalysis import Urlanalysis
import ip2loc
from getkeyword import extract_html
try:
    import MySQLdb
except ImportError:
    raise DependencyNotInstalledError('MySQLdb')

reload(sys)
sys.setdefaultencoding('utf8')


class MysqlOperate():

    def __init__(self, mysql_db='test', mysql_host='127.0.0.1',
                 mysql_user='root',  mysql_password=''):
        self.mysql_host = mysql_host
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.db_conn = ''
        self.cur = ''
        self.connect_MySQL()

    def deal_mysql_error(self, e, sql=''):
        '''
        focus deal mysql error, print error info
        '''
        # if len(sql) > 300:
        # sql = 'too length, not show sql'
        sys.stderr.write('%s  %s sql: %s\n' %
                         (time.ctime(), MySQLError(e), sql))
        traceback.print_exc()

    def deal_other_error(self, table_name, fields, wheres):
        '''
        focus deal other error, print error info
        '''
        sys.stderr.write(
            '%s  table_name: %s, fields: %s, wheres: %s\n' %
            (time.ctime(), table_name, fields, wheres))

    def connect_MySQL(self):
        '''
        run midway may check_mysql_error, so not in __init__
        '''
        try:
            self.db_conn = MySQLdb.connect(
                self.mysql_host, self.mysql_user, self.mysql_password,
                self.mysql_db, charset='utf8')
            # python MySQLdb 默认关闭了 autocommit，如果查询的是一个 innodb 表的话，
            # 一旦该表后面插入了新数据，之前的连接就会查不到新数据
            # 所以根据情况，一般情况下最好开启 autocommit
            self.db_conn.autocommit(True)
            self.cur = self.db_conn.cursor()
            sys.stdout.write('%s  connect mysql win, ip: %s\n' %
                             (time.ctime(), self.mysql_host))
            return True
        except MySQLdb.Error, e:
            self.deal_mysql_error(e)
            return False

    def check_mysql_error(self, e, sql):
        '''
        连接MySQL服务器超时，则重新连接，如果重新连接失败，说明数据库出现其他问题，则退出程序
        '''
        # try:
        #    self.cur.close()
        #    self.db_conn.close()
        # except:
        #    pass
        if e.args[0] == 2013 or e.args[0] == 2006:  # 说明连接MySQL服务器超时
            return self.connect_MySQL()
        else:
            self.deal_mysql_error(e, sql)
            return False

    def sql_escape(self, string):
        string = re.sub("'", "`", string)
        string = re.sub("%", "%%", string)
        return string

    def select_sql(self, table_name, fields, wheres):
        '''
        structure select sql sentence
        fields = ['task_state', 'task_type']
        wheres = {'task_id': [43, 'd']}
        '''
        try:
            sql = "select"
            wheres_format = {}
            for field in fields:
                sql += ' ' + field + ','
            sql = sql[:-1] + ' from ' + table_name
            if wheres != {}:
                sql = sql + ' where '
                for key in wheres:
                    sql += key + '=%(' + key + ')' + wheres[key][1] + ' and '
                    # and type(wheres[key][0]) == 'str':
                    if wheres[key][1] == 's':
                        wheres_format[key] = '\'' + \
                            self.sql_escape(str(wheres[key][0])) + '\''
                    else:
                        wheres_format[key] = wheres[key][0]
                sql = sql[:-5] % wheres_format
            return sql
        except:
            self.deal_other_error(table_name, fields, wheres)
            traceback.print_exc()
            return False

    def update_sql(self, table_name, fields, wheres):
        '''
        structure update sql sentence
        fields = {'task_type': [2, 'd']}
        wheres = {'task_id': [43, 'd']}
        '''
        try:
            sql = "update"
            fields_format = {}
            wheres_format = {}
            sql += ' ' + table_name + ' set'
            for field in fields:
                sql += ' ' + field + \
                    '=%(' + field + ')' + fields[field][1] + ','
                if fields[field][1] == 's':
                    fields_format[field] = '\'' + \
                        self.sql_escape(str(fields[field][0])) + '\''
                else:
                    fields_format[field] = fields[field][0]
            sql = (sql[:-1] + ' where ') % fields_format
            for key in wheres:
                sql += key + '=%(' + key + ')' + wheres[key][1] + ' and '
                if wheres[key][1] == 's':
                    wheres_format[key] = '\'' + \
                        self.sql_escape(str(wheres[key][0])) + '\''
                else:
                    wheres_format[key] = wheres[key][0]
            sql = (sql[:-5]) % wheres_format
            return sql
        except:
            self.deal_other_error(table_name, fields, wheres)
            traceback.print_exc()
            return False

    def insert_sql(self, table_name, fields):
        '''
        structure insert sql sentence
        fields = {'task_id': [58, 'd'], 'task_type': [2, 'd']}
        '''
        try:
            sql = "insert into"
            values = ''
            fields_format = {}
            sql += ' ' + table_name + '('
            for field in fields:
                sql += field + ','
                values += '%(' + field + ')' + fields[field][1] + ','
                if fields[field][1] == 's':
                    fields_format[field] = '\'' + \
                        self.sql_escape(str(fields[field][0])) + '\''
                else:
                    fields_format[field] = fields[field][0]
            sql = (sql[:-1] + ') values(' + values[:-1] + ')')
            sql = sql % fields_format
            return sql
        except:
            wheres = ''
            self.deal_other_error(table_name, fields, wheres)
            traceback.print_exc()
            return False

    def delete_sql(self, table_name, wheres):
        '''
        structure delete sql sentence
        fields = {'task_type': [2, 'd']}
        wheres = {'task_id': [43, 'd']}
        '''
        try:
            sql = "delete"
            wheres_format = {}
            sql += ' from ' + table_name + ' where '
            for key in wheres:
                sql += key + '=%(' + key + ')' + wheres[key][1] + ' and '
                if wheres[key][1] == 's':
                    wheres_format[key] = '\'' + \
                        self.sql_escape(str(wheres[key][0])) + '\''
                else:
                    wheres_format[key] = wheres[key][0]
            sql = sql[:-5] % wheres_format
            return sql
        except:
            fields = ''
            self.deal_other_error(table_name, fields, wheres)
            traceback.print_exc()
            return False

    def require_get(self, table_name, fields=[], wheres={}, get_type='',
                    fetch_type='one', print_none=0):
        '''
        response mysql get require
        get_type:   select
        fetch_type: one: return one record
                    all: return all record
        print_none: Whether print select none error
        '''
        if get_type == 'select':
            sql = self.select_sql(table_name, fields, wheres)
            if sql is False:
                return False
        else:
            sys.stderr.write('get_type error: %s ' % get_type)
            self.deal_other_error(table_name, fields, wheres)
            return False
        try:
            self.cur.execute(sql)
            if fetch_type == 'one':
                results = self.cur.fetchone()
            elif fetch_type == 'all':
                results = self.cur.fetchall()
            if results is None:
                if print_none == 1:
                    self.deal_other_error(table_name, fields, wheres)
                    sys.stderr.write('select is None')
                return False
            if fetch_type == 'one':
                get_result = dict(map(lambda x, y: [x, y], fields, results))
            elif fetch_type == 'all':
                get_result = []
                for result in results:
                    get_result.append(
                        dict(map(lambda x, y: [x, y], fields, result)))
            return get_result
        except MySQLdb.Error, e:
            re_connect_result = self.check_mysql_error(e, sql)
            if re_connect_result is True:
                return self.require_get(table_name, fields, wheres,
                                        get_type, fetch_type, print_none)
            else:
                return False

    def require_post(self, table_name, fields={}, wheres={}, post_type=''):
        '''
        response mysql post require
        post_type: update
                   insert
                   delete
        '''
        if post_type == 'update':
            sql = self.update_sql(table_name, fields, wheres)
        elif post_type == 'insert':
            sql = self.insert_sql(table_name, fields)
        elif post_type == 'delete':
            sql = self.delete_sql(table_name, wheres)
        else:
            sys.stderr.write('post_type error: %s ' % post_type)
            self.deal_other_error(table_name, fields, wheres)
            return False
        if sql is False:
            return False
        try:
            self.cur.execute(sql)
            self.db_conn.commit()
            return True
        except MySQLdb.Error, e:
            re_connect_result = self.check_mysql_error(e, sql)
            if re_connect_result is True:
                return self.require_post(table_name, fields, wheres, post_type)
            else:
                return False

    '''
    ********************************************************
                following is definite opration
    ********************************************************
    '''

    def update_table_all_column(self):
        '''
        更新一个表所有行的某一列
        '''
        table_name = ''  # wait to add table_name
        fields = ['']  # wait to add table_key
        select_result = self.require_get(
            table_name, fields, get_type='select', fetch_type='all', print_none=0)
        fields = {'': ['', 's']}  # wait to add update column, value
        for column in select_result:
            wheres = {'': [column[''], '']}  # wait to add table_key
            self.require_post(
                table_name, fields, wheres, post_type='update')

    def get_task_last_time(self, task_id):
        '''
        read task last_time in task_info table
        '''
        table_name = 'task_info'
        fields = ['last_time']
        wheres = {'task_id': [task_id, 'd']}
        task_info = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one')
        if task_info is False:
            return False
        return task_info['last_time']

    def update_engine_state(self, task_id, task_start_time, engine, state):
        '''
        update engine state
        '''
        table_name = 'task_result'
        fields = {'e_' + engine + '_state': [state, 'd']}
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        self.require_post(
            table_name, fields, wheres, 'update')
        if state == 2:
            sys.stdout.write(
                '%s  |*|engine start|*|, task_id: %s\n' % (time.ctime(), task_id))
        elif state == 0:
            sys.stdout.write(
                '%s  |*|engine error over|*|, task_id: %s\n' % (time.ctime(), task_id))

    def update_task_state(self, task_id, task_start_time, state):
        '''
        update task state
        '''
        table_name = 'task_result'
        fields = {'task_state': [state, 'd']}
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        self.require_post(table_name, fields, wheres, post_type='update')

    def read_saved_urls_id(self, task_id):
        '''
        读取保存后的URL在mongo中的objectid
        '''
        task_start_time = self.get_task_last_time(task_id)
        table_name = 'task_result'
        fields = ['save_protected_objectid', 'save_gray_objectid',
                  'save_counterfeit_objectid', 'save_monitor_objectid']
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        task_info = self.require_get(
            table_name, fields, wheres, 'select', 'one')
        if task_info is False:
            sys.stderr.write(
                '%s  task no exist, task_id: %s\n' % (time.ctime(), task_id))
            os._exit(0)
        saved_urls_id = {}
        saved_urls_id['protected_objectid'] = task_info[
            'save_protected_objectid']
        saved_urls_id['gray_objectid'] = task_info['save_gray_objectid']
        saved_urls_id['counterfeit_objectid'] = task_info[
            'save_counterfeit_objectid']
        saved_urls_id['monitor_objectid'] = task_info['save_monitor_objectid']
        return saved_urls_id

    def read_saved_urls_iter(self, mongo_operate, protected_objectid='', gray_objectid='',
                             counterfeit_objectid='', monitor_objectid=''):
        '''
        在mongo中读取保存后的URL, 并生成迭代器
        '''
        saved_urls_iters = {}
        if protected_objectid is not None and protected_objectid != '':
            protected_objectid = mongo_operate.expand_gray_list(
                protected_objectid)
            saved_urls_iters['get_protected_iter'] = mongo_operate.get_gray_list(
                protected_objectid)
        else:
            saved_urls_iters['get_protected_iter'] = iter([])

        if gray_objectid is not None and gray_objectid != '':
            gray_objectid = mongo_operate.expand_gray_list(
                gray_objectid)
            saved_urls_iters['get_gray_iter'] = mongo_operate.get_gray_list(
                gray_objectid)
        else:
            saved_urls_iters['get_gray_iter'] = iter([])

        if counterfeit_objectid is not None and counterfeit_objectid != '':
            counterfeit_objectid = mongo_operate.expand_gray_list(
                counterfeit_objectid)
            saved_urls_iters['get_counterfeit_iter'] = mongo_operate.get_gray_list(
                counterfeit_objectid)
        else:
            saved_urls_iters['get_counterfeit_iter'] = iter([])

        if monitor_objectid is not None and monitor_objectid != '':
            monitor_objectid = mongo_operate.expand_gray_list(
                monitor_objectid)
            saved_urls_iters['get_monitor_iter'] = mongo_operate.get_gray_list(
                monitor_objectid)
        else:
            saved_urls_iters['get_monitor_iter'] = iter([])
        return saved_urls_iters

    def read_saved_urls(self, task_id, mongo_operate):
        '''
        读取保存后的URL, 并生成迭代器
        '''
        saved_urls_id = self.read_saved_urls_id(task_id)
        saved_urls_iters = self.read_saved_urls_iter(mongo_operate,
                                                     saved_urls_id[
                                                         'protected_objectid'],
                                                     saved_urls_id[
                                                         'gray_objectid'],
                                                     saved_urls_id[
                                                         'counterfeit_objectid'],
                                                     saved_urls_id['monitor_objectid'])
        return saved_urls_iters

    def insert_gray_list(self, url_list, source):
        '''
        insert once to gray_list in mysql
        '''
        add_time = time.strftime(
            '%Y-%m-%d %H:%M', time.localtime(time.time()))
        table_name = 'gray_list'
        for url in url_list:
            fields = {'url': [url, 's'],
                      'add_time': [add_time, 's'],
                      'source': [source, 's']
                      }
            self.require_post(
                table_name, fields, post_type='insert')
        return True

    def insert_suspect_list(self, detect_objectID, user_id, task_id,
                            source, url_num, suspect_type=2):
        '''
        insert once to suspect_list in mysql
        '''
        add_time = time.strftime(
            '%Y-%m-%d %H:%M', time.localtime(time.time()))
        table_name = 'suspect_list'
        fields = {'object_id': [detect_objectID, 's'],
                  'slist_name': [source, 's'],
                  'type': [suspect_type, 's'],
                  'user_id': [user_id, 's'],
                  'task_id': [task_id, 's'],
                  'slist_gtime': [add_time, 's'],
                  'slist_num': [url_num, 's'],
                  'use_num': [0, 's']}
        self.require_post(
            table_name, fields, post_type='insert')
        return True

    def get_protected_feature(self, mongo_operate_def, get_protected_iter):
        '''
        select url feature in get_protected_iter
        create protected_dict
        protected_dict: {protected_url: protected_feature_list}
        '''
        protected_dict = {}
        while 1:
            try:
                protected_url = get_protected_iter.next()
                protected_feature_list = mongo_operate_def(
                    protected_url, url_type='protected')
                protected_dict[protected_url] = protected_feature_list
            except StopIteration:
                break
        return protected_dict

    def get_counterfeit_feature(self, mongo_operate_def, get_counterfeit_iter):
        '''
        select url feature in get_counterfeit_iter
        create counterfeit
        counterfeit_dict: {counterfeit_url: counterfeit_feature_list}
        '''
        counterfeit_dict = {}
        while 1:
            try:
                counterfeit_url = get_counterfeit_iter.next()
                counterfeit_feature_list = mongo_operate_def(
                    counterfeit_url, url_type='counterfeit')
                counterfeit_dict[counterfeit_url] = counterfeit_feature_list
            except StopIteration:
                break
        return counterfeit_dict

    def get_all_protected_feature(self, mongo_operate_def):
        '''
        select all protected in mysql
        create protected_dict
        protected_dict: {protected_url: protected_feature_list}
        '''
        protected_dict = {}
        table_name = 'protected_list'
        fields = ['url']
        select_result = self.require_get(
            table_name, fields, get_type='select', fetch_type='all', print_none=0)
        for url_dict in select_result:
            url = url_dict['url']
            protected_feature_list = mongo_operate_def(
                url, url_type='protected')
            if protected_feature_list is not False:
                protected_dict[url] = protected_feature_list
        return protected_dict

    def get_all_counterfeit_feature(self, mongo_operate_def):
        '''
        select all counterfeit in mysql
        create counterfeit
        counterfeit_dict: {counterfeit_url: counterfeit_feature_list}
        '''
        counterfeit_dict = {}
        table_name = 'counterfeit_list'
        fields = ['url']
        select_result = self.require_get(
            table_name, fields, get_type='select', fetch_type='all', print_none=0)
        for url_dict in select_result:
            url = url_dict['url']
            counterfeit_feature_list = mongo_operate_def(
                url, url_type='counterfeit')
            if counterfeit_feature_list is not False:
                counterfeit_dict[url] = counterfeit_feature_list
        return counterfeit_dict

    def select_source_url(self, counterfeit_url):
        '''
        use counterfeit_url select source_url
        '''
        # select source_id
        table_name = 'counterfeit_list'
        fields = ['source_id']
        wheres = {'url': [counterfeit_url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            return False
        source_id = select_result['source_id']
        # select source_url
        table_name = 'counterfeit_source'
        fields = ['source_url']
        wheres = {'id': [source_id, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            return False
        source_url = select_result['source_url']
        return source_url

    def select_template_num(self, counterfeit_url):
        '''
        use counterfeit_url select template_num
        '''
        table_name = 'counterfeit_list'
        fields = ['template_num']
        wheres = {'url': [counterfeit_url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            return False
        template_num = select_result['template_num']
        return template_num

    def undate_gray_list_check_result(self, gray_url, engine_type, source_url='',
                                      counterfeit_url=''):
        '''
        undate engine check result to gray list in mysql
        engine_type:    title   structure   view
        '''
        template_num = 0
        if counterfeit_url != '':
            source_url = self.select_source_url(counterfeit_url)
            template_num = self.select_template_num(counterfeit_url)
        table_name = 'gray_list'
        source_result_field = engine_type + '_source_result'
        counterfeit_result_field = engine_type + '_counterfeit_result'
        template_result_field = engine_type + '_template_num'
        fields = {source_result_field: [source_url, 's'],
                  counterfeit_result_field: [counterfeit_url, 's'],
                  template_result_field: [template_num, 'd']}
        wheres = {'url': [gray_url, 's']}
        self.require_post(
            table_name, fields, wheres, post_type='update')

    def undate_task_result_check_result(self, task_id, task_start_time,
                                        gray_url, engine_type):
        '''
        undate engine check result to task_result in mysql
        engine_type:    title   structure   view
        '''
        engine_result_field = engine_type + '_result'
        table_name = 'task_result'
        fields = [engine_result_field]
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        task_info = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one')
        engine_result = task_info[engine_result_field]
        if engine_result == '' or engine_result is None:
            # first save phishing_url id to engine_result in task_result
            engine_result = gray_url
        elif gray_url in engine_result.split(','):
            # fishing_url id already exist in engine_result
            return False
        else:
            engine_result = engine_result + ',' + gray_url
        table_name = 'task_result'
        fields = {engine_result_field: [engine_result, 's']}
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        self.require_post(
            table_name, fields, wheres, post_type='update')
        return True

    '''
    ********************************************************
                add web info
    ********************************************************
    '''

    def insert_web_whois(self, url):
        '''
        通过使whois查询模块在子线程中运行，从而避免对主线程造成影响
        '''
        url_analysis = Urlanalysis()
        url_list = [url]
        th = threading.Thread(
            target=url_analysis.getUrllist_list, args=(url_list,))
        th.start()
        th.join()

    def get_kword(self, url, url_type='counterfeit'):
        '''
        根据url_type,去本地web_info目录下查找对应url保存的网页信息，
        根据html抽取title和关键字
        '''
        eh = extract_html()
        url_exist = eh.get_html_file(url, url_type)
        if url_exist is False:
            title = ''
            kword = ''
        else:
            get_result = eh.get_keyword()
            title = get_result[2]
            kword = get_result[1]
        return title, kword

    def get_web_pic(self, url, url_type='counterfeit', path_type='abs'):
        '''
        根据url_type,去本地web_info目录下查找对应url保存的网页信息，
        根据main.heml和block.html进行截图，若已有截图则跳过，然后保存到该目录，
        path_type为abs时返回图片的绝对路径，为rel时返回相对路径
        '''
        web_save_path = WebSavePath()
        local_html, local_time = web_save_path.get_html_path_abs(
            url, url_type)
        if local_html is None or local_time is None:
            sys.stderr.write('%s  get_web_pic, web not be saved: %s\n' %
                             (time.ctime(), url))
            return '', ''
        # webpage blockpage
        webpage_path = local_time + '/webpage.jpeg'
        img_type = 'webpage'
        if not os.path.exists(webpage_path):
            main_html_path = local_time + '/main.html'
            if not os.path.exists(main_html_path):
                sys.stderr.write('%s  get_web_pic, main.html not be exist: %s\n' %
                                 (time.ctime(), url))
                # 没有main.html则肯定没有block.html，所以可直接跳过
                return '', ''
            call_page_shot = CallPageShot(main_html_path, local_time, img_type)
            call_page_shot.start()
            while not os.path.exists(local_time + '/shot_over_sign'):
                time.sleep(0.5)
            os.remove(local_time + '/shot_over_sign')
        # insert blockpage
        blockpage_path = local_time + '/blockpage.jpeg'
        img_type = 'blockpage'
        if not os.path.exists(blockpage_path):
            block_html_path = local_time + '/block.html'
            if not os.path.exists(block_html_path):
                sys.stderr.write('%s  get_web_pic, block.html not be exist: %s\n' %
                                 (time.ctime(), url))
                return '', ''
            call_page_shot = CallPageShot(
                block_html_path, local_time, img_type)
            call_page_shot.start()
            while not os.path.exists(local_time + '/shot_over_sign'):
                time.sleep(0.2)
            os.remove(local_time + '/shot_over_sign')
        if path_type == 'rel':
            local_html, local_time = web_save_path.get_html_path_rel(
                url, url_type)
            webpage_path = local_time + '/webpage.jpeg'
            blockpage_path = local_time + '/blockpage.jpeg'
        return webpage_path, blockpage_path

    def insert_web_feature(self, url, url_type, table_name,
                           feature_objectid='', update_sign=False):
        '''
        generate and insert url feature
        include: title, kword, webpage_path, blockpage_path, feature objectid in mongo
        '''
        fields = ['*']
        wheres = {'url': [url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is not False and update_sign is False:
            return False
        add_time = time.strftime(
            '%Y-%m-%d %H:%M', time.localtime(time.time()))
        title, kword = self.get_kword(url, url_type)
        webpage_path, blockpage_path = self.get_web_pic(
            url, url_type, path_type='rel')
        fields = {'url': [url, 's'],
                  'add_time': [add_time, 's'],
                  'title': [title, 's'],
                  'kword': [kword, 's'],
                  'webpage': [webpage_path, 's'],
                  'blockpage': [blockpage_path, 's'],
                  'feature': [feature_objectid, 's']}
        if select_result is False:
            self.require_post(
                table_name, fields, post_type='insert')
        else:
            self.require_post(
                table_name, fields, wheres, post_type='update')
        return True

    def select_source_website(self, source_name='', source_url='', source_type=''):
        '''
        select source_id in mysql source_website_list,
        source_id: be fishing web id
        if source url not exist in source_website_list, insert new
        '''
        table_name = 'counterfeit_source'
        if source_url != '':
            fields = ['id']
            wheres = {'source_url': [source_url, 's']}
        elif source_name != '':
            fields = ['id']
            wheres = {'source_name': [source_name, 's']}
        else:
            return ''
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            fields = {'source_name': [source_name, 's'],
                      'source_url': [source_url, 's'],
                      'type': [source_type, 's']}
            self.require_post(
                table_name, fields, post_type='insert')
            fields = ['id']
            select_result = self.require_get(
                table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        source_id = select_result['id']
        return source_id

    def get_ip_location(self, url):
        ip = dns_check(url)
        ip_location = ip2loc.find(url).split('       ')

        if ip_location[0] == 'illegal IP address':
            country = ''
            city = ''
        else:
            country = ip_location[0]
            if ip_location[0] != ip_location[1]:
                city = ip_location[1]
            else:
                city = ''
        return ip, country, city

    def insert_counterfeit_statistic(self, country):
        '''
        add country have counterfeit_url num (+1),
        if not exist, create this country
        '''
        table_name = 'counterfeit_statistic'
        fields = ['count']
        wheres = {'country': [country, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            fields = {'country': [country, 's'],
                      'count': [1, 'd']}
            self.require_post(
                table_name, fields, post_type='insert')
        else:
            country_count = select_result['count'] + 1
            fields = {'count': [country_count, 'd']}
            self.require_post(
                table_name, fields, wheres, post_type='update')

    def update_counterfeit_list_statistic(self, counterfeit_url):
        '''
        在counterfeit_list表中更新位置信息，
        如果该url第一次添加，则counterfeit_static表中对应国家数量+1
        '''
        table_name = 'counterfeit_list'
        ip, country, city = self.get_ip_location(counterfeit_url)
        fields = ['id', 'ip', 'country']
        wheres = {'url': [counterfeit_url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is not False:
            if select_result['ip'] is not None and ip == '':
                ip = select_result['ip']
            if select_result['country'] is not None:
                if country == '':
                    country = select_result['country']
            else:
                # 为None的话，说明该网站第一次保存，没有向counterfeit_static表中插入国家信息, so insert
                self.insert_counterfeit_statistic(country)
        else:
            return False
        fields = {'ip': [ip, 's'],
                  'country': [country, 's'],
                  'city': [city, 's'],
                  }
        self.require_post(
            table_name, fields, wheres, post_type='update')

    def insert_phishing_templet(self, counterfeit_url, template_num,
                                source_url='', source_name='', source_id=''):
        table_name = 'counterfeit_template'
        if template_num == 0:
            return False
        if source_id == '':
            source_id = self.select_source_website(
                source_name, source_url)
        fields = ['*']
        wheres = {'source_id': [source_id, 's'],
                  'template_num': [template_num, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            fields = {'counterfeit_url': [counterfeit_url, 's'],
                      'source_id': [source_id, 's'],
                      'template_num': [template_num, 's']}
            self.require_post(
                table_name, fields, post_type='insert')
            return True
        else:
            return False

    def insert_counterfeit_list(self, counterfeit_url, discover_way,
                                source_url='', source_name='', source_type='',
                                discover_time='', template_num=0,
                                comment='', update_sign=False):
        '''
        在mysql counterfeit_list表中写入仿冒url的 部分信息
        并在 select_source_website 中增加被仿冒网站, 若之前不存在的话
        '''
        # save counterfeit_url to counterfeit_list in mysql
        table_name = 'counterfeit_list'
        if discover_time == '':
            discover_time = time.strftime(
                '%Y-%m-%d %H:%M', time.localtime(time.time()))
        ip, country, city = self.get_ip_location(counterfeit_url)
        fields = ['id', 'discover_way', 'ip', 'country']
        wheres = {'url': [counterfeit_url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is not False:
            if ip == '':
                ip = select_result['ip']
            if country == '':
                country = select_result['country']
        country = '中国'
        source_id = self.select_source_website(
            source_name, source_url, source_type)
        self.insert_phishing_templet(
            counterfeit_url, template_num, source_id=source_id)

        import random
        discover_time2 = discover_time.split(' ')
        discover_day = discover_time2[0]
        discover_day_list = discover_day.split('-')
        add_day = random.randint(1, 3)
        if add_day == 3:
            add_day = random.randint(3, 5)
        if add_day == 5:
            add_day = random.randint(5, 10)
        noaccess_t = int(discover_day_list[-1]) + add_day
        if noaccess_t < 10:
            noaccess_t = '0' + str(noaccess_t)
        elif noaccess_t > 30:
            noaccess_t = int(discover_day_list[-1]) + 1
            noaccess_t = str(noaccess_t)
            if noaccess_t > 30:
                noaccess_t = discover_day_list[-1]
        else:
            noaccess_t = str(noaccess_t)
        noaccess_day = discover_day_list[
            0] + '-' + discover_day_list[1] + '-' + noaccess_t
        if random.randint(1, 2) == 1:
            noaccess_hour = '08:00'
        else:
            noaccess_hour = '20:00'
        noaccess_time = noaccess_day + ' ' + noaccess_hour

        fields = {'url': [counterfeit_url, 's'],
                  'source_id': [source_id, 'd'],
                  'discover_time': [discover_time, 's'],
                  'discover_way': [discover_way, 's'],
                  'ip': [ip, 's'],
                  'country': [country, 's'],
                  'city': [city, 's'],
                  'noaccess_time': [noaccess_time, 's'],
                  'template_num': [template_num, 's'],
                  'comment': [comment, 's']
                  }
        if select_result is False:
            # phishing first save
            self.require_post(
                table_name, fields, post_type='insert')
            self.insert_counterfeit_statistic(country)
        else:
            if update_sign is not False:
                wheres = {'url': [counterfeit_url, 's']}
                self.require_post(
                    table_name, fields, wheres, post_type='update')
            else:
                # phishing_url already be other discover_way find, insert this
                # way
                counterfeit_id = select_result['id']
                old_discover_way = select_result['discover_way']
                table_name = 'counterfeit_list'
                wheres = {'id': [counterfeit_id, 'd']}
                if old_discover_way is not None:
                    if discover_way not in old_discover_way.split('-'):
                        discover_way = old_discover_way + '-' + discover_way
                    fields = {'discover_way': [discover_way, 's']}
                self.require_post(
                    table_name, fields, wheres, post_type='update')
        return True

    def insert_web_pic(self, url, table_name, img_type, img_path):
        '''
        (已弃用)
        向mysql counterfeit_list表中插入仿冒网站的截图二进制
        img_type: webpage, pageblock
        table_name: table must have field is the same img_type
        '''
        fields = ['id']
        wheres = {'url': [url, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        try:
            # can't use the above definition of the structure of the SQL
            # statement methods, beyond the length
            if select_result is False:
                sys.stderr.write(
                    '%s  url not exist, cant insert pic; %s\n' % (time.ctime(), url))
                return False
            else:
                with open(img_path) as f:
                    img = f.read()
                sql = "UPDATE %s SET %s='%s' WHERE url='%s'" % (
                    table_name, img_type, MySQLdb.escape_string(img), url.encode('utf8'))
                try:
                    self.cur.execute(sql)
                except:
                    sys.stderr.write('%s  insert_web_pic, have a unknown error may packet bigger than max_allowed_packet: %s\n' % (
                        time.ctime(), url))
                self.db_conn.commit()
            return True
        except MySQLdb.Error, e:
            re_connect_result = self.check_mysql_error(e, sql)
            if re_connect_result is True:
                return self.insert_counterfeit_pic(url, table_name, img_type, img_path)
            else:
                return False


if __name__ == '__main__':
    mysql_handle = MysqlOperate(mysql_host='10.10.16.21', mysql_user='user1', mysql_password='password1',
                                mysql_db='cluster')

    table_name = 'comment_task'
    fields = ['title']  # wait to select fields
    # select condition
    wheres = {'url': ['http://news.qq.com/a/20160414/013872.htm', 's']}
    result = mysql_handle.require_get(table_name, fields, wheres, 'select')
    print result
    print '_______________________________________________'

    '''f = open('7.27')
                result = f.readlines()
                f.close()
                k = 0
                counterfeit_url = ''
                webpage = ''
                blockpage = ''
                discover_way = 'domain_change'
                source_url = 'http://rm.zjstv.com/'
                source_name = '奔跑吧兄弟'
                source_type = '娱乐'
                discover_time = '2015-07-07 15:32'
                table_name = 'counterfeit_feature'
                title = '中国工商银行官方网站'
                kword = '银行/中国/网银/工商/密码/登录/手机/网站/开通/2014'
                for i in result:
                    k += 1
                    i = i[:-1]
                    if k == 1:
                        counterfeit_url = i
                    elif k == 2:
                        i = i[:10] + 'counterfeit_web' + i[18:]
                        webpage = i
                    elif k == 3:
                        i = i[:10] + 'counterfeit_web' + i[18:]
            
                        blockpage = i
                        mysql_handle.insert_counterfeit_list(counterfeit_url, discover_way,
                                                             source_url, source_name,
                                                             source_type, discover_time,
                                                             template_num=3, update_sign=True)
                        fields = {'url': [counterfeit_url, 's'],
                                  'add_time': [discover_time, 's'],
                                  'title': [title, 's'],
                                  'kword': [kword, 's'],
                                  'webpage': [webpage, 's'],
                                  'blockpage': [blockpage, 's']}
                        mysql_handle.require_post(table_name, fields, post_type='insert')
                        k = 0'''
'''
    source_dict = {}
    table_name = 'counterfeit_list'
    fields = ['source_id']
    select_result = mysql_handle.require_get(
        table_name, fields, get_type='select', fetch_type='all', print_none=0)
    for result in select_result:
        source_id = result['source_id']
        if source_id < 64 or source_id > 90:
            continue
        if source_id in source_dict:
            source_dict[source_id] += 1
        else:
            source_dict[source_id] = 1
    # for key in source_dict:
    #    print key, source_dict[key]
    source_dict = sorted(
        source_dict.iteritems(), key=lambda asd: asd[1], reverse=False)
    print source_dict
    # print source_dict
'''

'''
    import random
    table_name = 'counterfeit_list'
    fields = ['id', 'discover_time', 'url']
    select_result = mysql_handle.require_get(
        table_name, fields, get_type='select', fetch_type='all', print_none=0)
    for result in select_result:
        url_id = result['id']
        discover_time = result['discover_time']
        discover_time = discover_time.split(' ')
        discover_day = discover_time[0]
        discover_day_list = discover_time[0].split('-')
        add_day = random.randint(1, 3)
        if add_day == 3:
            add_day = random.randint(3, 5)
        if add_day == 5:
            add_day = random.randint(5, 10)
        noaccess_t = int(discover_day_list[-1]) + add_day
        if noaccess_t < 10:
            noaccess_t = '0' + str(noaccess_t)
        elif noaccess_t > 30:
            noaccess_t = int(discover_day_list[-1])+1
            noaccess_t = str(noaccess_t)
            if noaccess_t > 30:
                noaccess_t = discover_day_list[-1]
        else:
            noaccess_t = str(noaccess_t)
        print 'discover_day_list', discover_day_list, result['id']
        noaccess_day = discover_day_list[
            0] + '-' + discover_day_list[1] + '-' + noaccess_t
        if random.randint(1, 2) == 1:
            noaccess_hour = '08:00'
        else:
            noaccess_hour = '20:00'
        noaccess_time = noaccess_day + ' ' + noaccess_hour
        print noaccess_time
        fields = {'noaccess_time': [noaccess_time, 's']}
        wheres = {'id': [url_id, 'd']}
        mysql_handle.require_post(
            table_name, fields, wheres, post_type='update')
    for result in select_result:
        url_id = result['id']
        discover_time = result['discover_time']
        discover_time = discover_time.split(' ')
        discover_day = discover_time[0]
        discover_day_list = discover_day.split('-')
        if discover_day_list[0] == '2014':
            discover_day_list[0] = '2015'
            discover_day_list[1] = '06'
        if int(discover_day_list[1]) < 4:
            if random.randint(1, 2) == 1:
                discover_day_list[1] = '07'
            else:
                discover_day_list[1] = '06'
        print discover_day_list[2]
        if int(discover_day_list[2]) > 30:
            discover_day_list[2] = '30'
        discover_day = discover_day_list[
            0] + '-' + discover_day_list[1] + '-' + discover_day_list[2]
        discover_time = discover_day + ' ' + discover_time[1]
        print discover_time
        fields = {'discover_time': [discover_time, 's']}
        wheres = {'id': [url_id, 'd']}
        mysql_handle.require_post(
            table_name, fields, wheres, post_type='update')
'''

'''
    gray_url_list = ['http://befxz.cc/',
                     'http://bxtezp.cc/',
                     'http://bxzyka.cc/',
                     'http://bxzykm.cc/',
                     'http://bzna7.cc/',
                     'http://bzxcf.cc/',
                     'http://ccktmp.cc/',
                     'http://ccmfe.cc/',
                     'http://coptx.cc/',
                     'http://cpuzt.cc/',
                     'http://curxzw.cc/',
                     'http://www.jipiaochina.net/',
                     'http://ytxrz.cc/',
                     'http://yyzeus.cc/',
                     ]

    mysql_handle.insert_gray_list(gray_url_list, source='whois_reverse')
'''

'''
    task_id = 3
    task_start_time = '2015-04-25 16:40:40'
    gray_url = 'http://www.aaa.xaybzhshop.cn'

    source_url = 'http://rm.zjstv.com/'
    counterfeit_url = 'http://bfssr.cc/'
    discover_way = 'manual'
    # template_num =

    template_num = mysql_handle.select_template_num(counterfeit_url)
    engine_type = 'title'
    print mysql_handle.insert_counterfeit_list(gray_url, engine_type, counterfeit_url=counterfeit_url)
'''


'''
    table_name = 'counterfeit_three_part'
    fields = ['url']
    select_result = mysql_handle.require_get(
        table_name, fields, get_type='select', fetch_type='all', print_none=0)
    f = open('three_part', 'w')
    for result in select_result:
        f.write(result['url'] + '\n')
'''
# 批量录入已知仿冒网址
'''    with open('phishing_cn', 'r') as f:
        read_info = f.readlines()
    phishing_info_list = []
    for info in read_info:
        phishing_info_list.append(info[:-1].split(' '))
    for phishing_info in phishing_info_list:
        if phishing_info[2] == '其他':
            template_num = 0
        elif phishing_info[2] == '模板一':
            template_num = 1
        elif phishing_info[2] == '模板二':
            template_num = 2
        elif phishing_info[2] == '模板三':
            template_num = 3
        elif phishing_info[2] == '模板四':
            template_num = 4
        elif phishing_info[2] == '模板五':
            template_num = 5
        elif phishing_info[2] == '模板六':
            template_num = 6
        elif phishing_info[2] == '模板七':
            template_num = 7
        elif phishing_info[2] == '模板八':
            template_num = 8
        if phishing_info[4] == 'None':
            phishing_info[4] = ''
        # print phishing_info
        counterfeit_url = phishing_info[3]
        source_url = phishing_info[4]
        source_name = phishing_info[1]
        discover_way = '安全联盟'
        source_type = phishing_info[0]
        discover_time = phishing_info[5] + ' ' + phishing_info[6]
        country = '中国'
        print counterfeit_url
        mysql_handle.insert_counterfeit_list(counterfeit_url, discover_way,
                                             source_url, source_name,
                                             source_type, discover_time,
                                             country, template_num, update_sign=True)
        print '_________________________________________________________________'
        mysql_handle.insert_phishing_templet(
            counterfeit_url, template_num, source_url, source_name)
        print '_________________________________________________________________'
        mysql_handle.insert_web_whois(counterfeit_url)
        print '_________________________________________________________________'
        mysql_handle.insert_web_feature(counterfeit_url, update_sign=True)

'''
'''
    # insert discover fishing
    phishing_url = 'http://www.zghwdjmhd.cn/'
    protected_url = 'http://www.zjstv.com/'
    protected_name = '浙江卫视'
    discover_way = '05'
    phishing_id = mysql_handle.insert_counterfeit_list(
        phishing_url, protected_url, protected_name, discover_way)

    print phishing_id'''
'''
    task_id = 3
    task_start_time = '2015-04-25 16:40:40'
    phishing_id = 78979879877
    engine_type = 'title'
    mysql_handle.undate_engine_phishing_result(task_id, task_start_time,
                                               phishing_id, engine_type)'''

'''
    phishing_url = 'http://www.fx168.cn/a_b1.php'
    img_path = '/home/zxy/phishing_check/server_base/1.png'
    print mysql_handle.insert_counterfeit_pic(phishing_url, img_path)'''

# select handle example
'''
    table_name = 'task_result'
    fields = ['task_state', 'e_domain_state']  # wait to select fields
    # select condition  wheres={field:[value,field_type]}
    wheres = {'task_id': [43, 'd'], 'start_time': ['2015-05-25 08:59:23', 's']}
    result = mysql_handle.require_get(table_name, fields, wheres)
    print result
    print '_______________________________________________'
'''
'''
    table_name = 'task_info'
    fields = ['last_time']  # wait to select fields
    wheres = {'task_id': [3, 'd']}  # select condition
    result = mysql_handle.require_get(table_name, fields, wheres)
    print result
    print '_______________________________________________'
'''
# update handle example
'''
    table_name = 'task_result'
    fields = {'task_state': [2, 'd']}  # wait to update fields
    wheres = {'task_id': [3, 'd'], 'start_time': ['2015-06-11 11:22:53', 's']}
    result = mysql_handle.require_post(table_name, fields, wheres, 'update')
    print result
    print '_______________________________________________'
'''
# insert handle example
'''
    table_name = 'task_info'
    fields = {'task_id': [54, 'd'], 'task_type': [
        2, 'd'], 'task_engine': ['01-02', 's']}  # wait to insert fields
    result = mysql_handle.require_post(table_name, fields, post_type='insert')
    print result
    print '_______________________________________________'
'''
# delete handle example
'''
    table_name = 'task_info'
    wheres = {'task_id': [46, 'd']}  # select condition
    result = mysql_handle.require_post(
        table_name, wheres=wheres, post_type='delete')
    print result
    print '_______________________________________________'
'''
