# coding=utf-8


import logging
import parse
import urlparse
import urldb
import optparse
import re
import socket
import sys
_CurrentPath = sys.path[0]

try:
    import threadpool
except Exception:
    print "please install python-threadpool module firstly"


class Urlanalysis():

    def __init__(self, threadnums=1, host='172.31.159.248', username='root', password='', database='phishing_check'):
        self.conn_list = []  # 标注安全的线程
        self.mysql = {}
        self.mysql['host'] = host.strip('\'" ')
        self.mysql['username'] = username.strip('\'" ')
        self.mysql['password'] = password.strip('\'" ')
        self.mysql['database'] = database.strip('\'" ')
        self.threadnums = threadnums

    def getmysqlfrom_ini(self, file):
        try:
            fp = open(file, 'r')
        except Exception, e:
            logging.error(str(e))

        if fp is None:
            logging.error('Cannot open ini file %s' % file)

        self.mysql = {}

        lines = fp.readline()
        self.mysql['host'] = lines.strip('\'" ')
        self.mysql['host'] = self.mysql['host'].split("=")[1][:-1]

        lines = fp.readline()
        self.mysql['username'] = lines.strip('\'" ')
        self.mysql['username'] = self.mysql['username'].split("=")[1][:-1]

        lines = fp.readline()
        self.mysql['password'] = lines.strip('\'" ')
        self.mysql['password'] = self.mysql['password'].split("=")[1][:-1]

        lines = fp.readline()
        self.mysql['database'] = lines.strip('\'" ')
        self.mysql['database'] = self.mysql['database'].split("=")[1][:-1]

        lines = fp.readline()
        self.threadnums = lines.strip('\'" ')
        self.threadnums = int(self.threadnums.split("=")[1])

    def getUrllist_list(self, url_list):
        self.url_list = url_list
        self.url_begin()

    def getUrllist_txt(self, file):

        self.url_list = []
        try:
            fp = open(file, 'r')
        except Exception, e:
            logging.error(str(e))

        if fp is None:
            logging.error('Cannot open url file %s' % file)

        lines = fp.read().splitlines()
        for line in lines:
            if '.' not in line:
                logging.error('Invalide url "%s" in file %s' % (line, file))
                continue
            self.url_list.append(line)
        self.url_begin()

    def get_top_host(self, url):
        if not url.startswith('http'):
            url = 'http://' + url
        parts = urlparse.urlparse(url)
        host = parts.netloc
        topHostPostfix = (
            '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me',
            '.mobi', '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn',
            '.net.cn', '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag',
            '.net.ag', '.org.ag', '.am', '.asia', '.at', '.be', '.com.br',
            '.net.br', '.bz', '.com.bz', '.net.bz', '.cc', '.com.co',
            '.net.co', '.nom.co', '.de', '.es', '.com.es', '.nom.es',
            '.org.es', '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in',
            '.gen.in', '.ind.in', '.net.in', '.org.in', '.it', '.jobs',
            '.jp', '.ms', '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz',
            '.org.nz', '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw',
            '.org.tw', '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', '.br', '.fr')
        extractPattern = r'[^\.]+(' + '|'.join([h.replace('.', r'\.')
                                                for h in topHostPostfix]) + ')$'
        pattern = re.compile(extractPattern, re.IGNORECASE)
        m = pattern.search(host)
        return m.group() if m else host

    def getWhois(self, url):
        if url is None or url == '':
            return
        # 判断是否存在数据库连接
        if len(self.conn_list) == 0:
            logging.critical('mysql conntction is empty.')
            exit()
        conn = self.conn_list.pop(0)
        '''
        域名解析模块，把任何输入形式的域名都解析成baidu.com的形式
        '''
        netloc = self.get_top_host(url)
        temp = netloc.split(".")
        # print 'temp', temp
        try:
            if 0 < int(temp[0]) and int(temp[0]) < 255 and 0 < int(temp[3]) and int(temp[3]) < 255:
                try:
                    netloc = socket.gethostbyaddr(netloc)[0]
                except:  # 已放弃 (核心已转储)
                    return
                netloc = self.get_top_host(netloc)
        except ValueError:  # invalid literal for int() with base 10
            pass
        '''
        检测域名是否在表domain中存在，即该域名的WHOIS信息被查询过
        '''
        check_sql = 'select auto_id from whois_domain where name="%s"' % netloc
        results = conn.getIDFromMysql(check_sql)

        if conn.status.startswith('Error:'):
            logging.error(conn.status)
            self.conn_list.append(conn)
            return
        elif results is not None:
            logging.info('Url:%s in database.' % url)
            self.conn_list.append(conn)
            return

        '''
        对于mysql中现在还不存在的域名，查询whois信息，并存在whois_dict中
        '''
        try:
            whois_dict = parse.get_whois(netloc)
            #print whois_dict
            if whois_dict['status'].startswith('Error:'):
                logging.error('%s:%s' % (url, whois_dict['status']))
                self.conn_list.append(conn)
                return
        except Exception as e:
            logging.critical('Fatal Error: %r', str(e))
            self.conn_list.append(conn)
            return
        '''
        把得到的信息写入mysql中
        '''
        try:
            conn.writeToDB(whois_dict)  # 把得到的信息写入数据库
        except Exception as e:
            logging.error('In writeToDB %s', str(e))

        self.conn_list.append(conn)

    def url_begin(self):
        logging.basicConfig(filename=_CurrentPath + '/url.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)-5.5s %(message)s', filemode='a+')
        # 配置日志文件
        for i in range(self.threadnums):  # 循环线程
            udb = urldb.UrlDB(self.mysql['host'], self.mysql['username'],
                              self.mysql['password'], self.mysql['database'])
            # 连接数据库
            if udb.status.startswith('Error:'):
                logging.error(udb.status)
                exit()
            else:
                self.conn_list.append(udb)
        # 开始多线程
        pool = threadpool.ThreadPool(self.threadnums)
        requests = threadpool.makeRequests(self.getWhois, self.url_list)
        [pool.putRequest(req) for req in requests]
        pool.wait()

if __name__ == '__main__':
    a = Urlanalysis()
    url_list = [
        "baodetang.cn"]
    a.getUrllist_list(url_list)
    # a.getUrllist_txt('D://url.txt')
    # a.getmysqlfrom_ini('D://url.ini')
    # a.getUrllist_txt('D://url.txt')
