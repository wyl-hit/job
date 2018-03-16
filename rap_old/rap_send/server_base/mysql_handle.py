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
author: wyl
'''

import sys
import time
import traceback
from errors import DependencyNotInstalledError, MySQLError
try:
    import MySQLdb
except ImportError:
    raise DependencyNotInstalledError('MySQLdb')


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

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

    def deal_mysql_error(self, e):
        '''
        focus deal mysql error, print error info
        '''
        sys.stderr.write('%s  %s\n' % (time.ctime(), MySQLError(e)))
        traceback.print_exc()

    def deal_other_error(self, table_name, fields, wheres):
        '''
        focus deal other error, print error info
        '''
        sys.stderr.write(
            '%s  table_name: %s, fields: %s, wheres: %s\n' %
            (time.ctime(), table_name, fields, wheres))
        traceback.print_exc()

    def connect_MySQL(self):
        '''
        run midway may check_mysql_error, so not in __init__
        '''
        try:
            self.db_conn = MySQLdb.connect(
                self.mysql_host, self.mysql_user, self.mysql_password,
                self.mysql_db, charset='utf8')
            self.cur = self.db_conn.cursor()
            sys.stdout.write('%s  connect mysql win, ip: %s\n' %
                             (time.ctime(), self.mysql_host))
            return True
        except MySQLdb.Error, e:
            self.deal_mysql_error(e)
            return False

    def check_mysql_error(self, e):
        '''
        连接MySQL服务器超时，则重新连接，如果重新连接失败，说明数据库出现其他问题，则退出程序
        '''
        try:
            self.cur.close()
            self.db_conn.close()
        except:
            pass
        if e.args[0] == 2013 or e.args[0] == 2006:  # 说明连接MySQL服务器超时
            return self.connect_MySQL()
        else:
            self.deal_mysql_error(e)
            return False

    def select_sql(self, table_name, fields=[], wheres={}):
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
            if not wheres:
                sql = sql[:-1] + ' from ' + table_name
                return sql
            sql = sql[:-1] + ' from ' + table_name + ' where '
            for key in wheres:
                sql += key + '=%(' + key + ')' + wheres[key][1] + ' and '
                if wheres[key][1] == 's':  # and type(wheres[key][0]) == 'str':
                    wheres_format[key] = '\'' + str(wheres[key][0]) + '\''
                else:
                    wheres_format[key] = wheres[key][0]
            sql = sql[:-5] % wheres_format
            return sql
        except:
            self.deal_other_error(table_name, fields, wheres)
            return False

    def update_sql(self, table_name, fields={}, wheres={}):
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
                    fields_format[field] = '\'' + str(fields[field][0]) + '\''
                else:
                    fields_format[field] = fields[field][0]
            sql = (sql[:-1] + ' where ') % fields_format
            for key in wheres:
                sql += key + '=%(' + key + ')' + wheres[key][1] + ' and '
                if wheres[key][1] == 's':
                    wheres_format[key] = '\'' + str(wheres[key][0]) + '\''
                else:
                    wheres_format[key] = wheres[key][0]
            sql = sql[:-5] % wheres_format
            return sql
        except:
            self.deal_other_error(table_name, fields, wheres)
            return False

    def insert_sql(self, table_name, fields={}):
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
                    fields_format[field] = '\'' + str(fields[field][0]) + '\''
                else:
                    fields_format[field] = fields[field][0]
            sql = (sql[:-1] + ') values(' + values[:-1] + ')')
            sql = sql % fields_format
            return sql
        except:
            wheres = ''
            self.deal_other_error(table_name, fields, wheres)
            return False

    def delete_sql(self, table_name, wheres={}):
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
                    wheres_format[key] = '\'' + str(wheres[key][0]) + '\''
                else:
                    wheres_format[key] = wheres[key][0]
            sql = sql[:-5] % wheres_format
            return sql
        except:
            fields = ''
            self.deal_other_error(table_name, fields, wheres)
            return False

    def require_get(self, table_name, fields=[], wheres={}, get_type='',
                    fetch_type='one', print_none=1):
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
                index = self.cur.description
                results = self.cur.fetchone()
            elif fetch_type == 'all':
                index = self.cur.description
                results = self.cur.fetchall()
            if results is None:
                if print_none == 1:
                    self.deal_other_error(table_name, fields, wheres)
                return False
            if fetch_type == 'one':
                get_result = {}
                for i in range(len(index)):
                    get_result[index[i][0]] = results[i]
            elif fetch_type == 'all':
                get_result = []
                for result in results:
                    tmp_dict = {}
                    for i in range(len(index)):
                        tmp_dict[index[i][0]] = result[i]
                    get_result.append(tmp_dict)
                
            return get_result
        except MySQLdb.Error, e:
            re_connect_result = self.check_mysql_error(e)
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
            re_connect_result = self.check_mysql_error(e)
            if re_connect_result is True:
                return self.require_post(table_name, fields, wheres, post_type)
            else:
                return False

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
            sys.stderr.write(
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

    def insert_counterfeit_list(self, phishing_url, protected_url, protected_name,
                                discover_way):
        '''
        在mysql counterfeit_list表中写入仿冒url的部分信息
        '''
        # save phishing_url to counterfeit_list in mysql
        url_hash = hash_md5(phishing_url)
        discover_time = time.strftime(
            '%Y-%m-%d %H:%M', time.localtime(time.time()))
        table_name = 'counterfeit_list'
        fields = ['id', 'discover_way']
        wheres = {'hash': [url_hash, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        if select_result is False:
            # phishing first save
            self.cur.execute(
                'select id from counterfeit_list order by id DESC limit 1')
            phishing = self.cur.fetchone()
            current_phishing_id = int(phishing[0]) + 1
            table_name = 'counterfeit_list'
            fields = {'id': [current_phishing_id, 'd'],
                      'url': [phishing_url, 's'],
                      'hash': [url_hash, 's'],
                      'source_url': [protected_url, 's'],
                      'source_name': [protected_name, 's'],
                      'discover_way': [discover_way, 's'],
                      'discover_time': [discover_time, 's']}
            self.require_post(
                table_name, fields, post_type='insert')
        else:
            # phishing_url already be other discover_way find, insert this way
            current_phishing_id = select_result['id']
            old_discover_way = select_result['discover_way']
            if discover_way not in old_discover_way.split('-'):
                discover_way = old_discover_way + '-' + discover_way
                table_name = 'counterfeit_list'
                fields = {'discover_way': [discover_way, 's']}
                wheres = {'id': [current_phishing_id, 'd']}
                self.require_post(
                    table_name, fields, wheres, post_type='update')
        return current_phishing_id

    def undate_engine_phishing_result(self, task_id, task_start_time, phishing_id):
        '''
        undate engine check result to task_result in mysql
        '''
        phishing_id = str(phishing_id)
        table_name = 'task_result'
        fields = ['structure_result']
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        task_info = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one')
        structure_result = task_info['structure_result']
        if structure_result == '' or structure_result is None:
            # first save phishing_url id to structure_result in task_result
            structure_result = phishing_id
        elif phishing_id in structure_result.split('-'):
            # fishing_url id already exist in structure_result
            return False
        else:
            structure_result = structure_result + '-' + phishing_id
        table_name = 'task_result'
        fields = {'structure_result': [structure_result, 's']}
        wheres = {'task_id': [task_id, 'd'],
                  'start_time': [task_start_time, 's']}
        self.require_post(
            table_name, fields, wheres, post_type='update')

    def insert_counterfeit_pic(self, phishing_url, img_path):
        '''
        向mysql counterfeit_list表中插入仿冒网站的截图
        '''
        url_hash = hash_md5(phishing_url)
        with open(img_path) as f:
            img = f.read()
        table_name = 'counterfeit_list'
        fields = ['url']
        wheres = {'hash': [url_hash, 's']}
        select_result = self.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        try:
            # can't use the above definition of the structure of the SQL
            # statement methods, beyond the length
            if select_result is False:
                sql = "INSERT INTO counterfeit_list (url,hash,webpage) VALUES ('%s','%s','%s')" % (
                    phishing_url, url_hash, MySQLdb.escape_string(img))
                self.cur.execute(sql)
                self.db_conn.commit()
            else:
                sql = "UPDATE counterfeit_list SET webpage='%s' WHERE hash='%s'" % (
                    MySQLdb.escape_string(img), url_hash)
                self.cur.execute(sql)
                self.db_conn.commit()
            return True
        except MySQLdb.Error, e:
            re_connect_result = self.check_mysql_error(e)
            if re_connect_result is True:
                return self.insert_counterfeit_pic(phishing_url, img_path)
            else:
                return False

if __name__ == '__main__':
    mysql_handle = MysqlOperate(mysql_host='172.31.159.248', mysql_user='root', mysql_password='',
                                mysql_db='metaseaching')
    task_id = 'user_1'
    table_name = 'repeat_task'
    fields = ['*']
    wheres = {'task_id': [task_id, 's']}
    try:
        select_result = mysql_handle.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one', print_none=0)
        print select_result
    except:
        traceback.print_exc()

    '''table_name = 'repeat_task'
                task_id = 'user_1'
                key_word = 'ss'
                engine_s = '12'
                add_time = '111'
                username = 'www'
                fields = {'task_id': [task_id, 's'],
                          'key_word': [key_word, 's'],
                          'engine_id': [engine_s, 's'],
                          'create_time': [add_time, 's'],
                          'user_name': [username, 's']
                          }
                result = mysql_handle.require_post(table_name, fields, post_type='insert')
                print result
                print '_______________________________________________'
            '''
