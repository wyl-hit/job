# coding=utf-8
import urllib2
from lxml import etree
import urlparse
from mysql_handle import MysqlOperate
import re
import chardet
import warnings
warnings.filterwarnings('ignore', '.*', Warning, 'chardet')


class WhoisReverse():

    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password):

        self.mysql_handle = MysqlOperate(mysql_db, mysql_host,
                                         mysql_user, mysql_password)
        self.email = ['', '', '']
        self.name = ['', '', '']
        self.domain = []

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

    def get_reverse_whois(self, url):
        if url is None or url is '':
            return False
        self.original_domain = self.get_top_host(url)
        table_name = 'whois_domain'
        fields = ['admin', 'tech', 'registrant']  # wait to select fields
        wheres = {'name': [self.original_domain, 's']}
        self.contactid = self.mysql_handle.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one')
        if self.contactid is False:
            return []
        return self.get_source()

    def get_source(self):
        table_name = 'whois_contacts'
        fields = ['name', 'email']
        wheres = {'contacts_id': [self.contactid['admin'], 'd']}
        result = self.mysql_handle.require_get(
            table_name, fields, wheres, get_type='select', fetch_type='one')
        if result is False:
            self.email[0] = ''
            self.name[0] = ''
        else:
            self.email[0] = result['email']
            self.name[0] = result['name']
        if self.contactid['tech'] != self.contactid['admin']:
            wheres = {'contacts_id': [self.contactid['tech'], 'd']}
            result = self.mysql_handle.require_get(
                table_name, fields, wheres, get_type='select', fetch_type='one')
            if result is False:
                self.email[1] = ''
                self.name[1] = ''
            else:
                self.email[1] = result['email']
                self.name[1] = result['name']
        if self.contactid['registrant'] != self.contactid['admin'] and self.contactid['registrant'] != self.contactid['tech']:
            wheres = {'contacts_id': [self.contactid['registrant'], 'd']}
            result = self.mysql_handle.require_get(
                table_name, fields, wheres, get_type='select', fetch_type='one')
            if result is False:
                self.email[2] = ''
                self.name[2] = ''
            else:
                self.email[2] = result['email']
                self.name[2] = result['name']
        if self.email[2] == self.email[1] or self.email[2] == self.email[0]:
            self.email[2] = ''
        if self.email[1] == self.email[0]:
            self.email[1] = ''
        if self.name[2] == self.name[1] or self.name[2] == self.name[0]:
            self.name[2] = ''
        if self.name[1] == self.name[0]:
            self.name[1] = ''
        for i in self.email:
            if i != '':
                # print i
                self.search(i, 1)
                self.write_todb()
        for i in self.name:
            if i != '':
                # print i
                self.search(i, 2)
                self.write_todb()
        return self.domain

    def search(self, source, search_mod):
        self.source = source
        self.search_mod = search_mod
        if self.search_mod == 1:
            target_url = 'http://whois.chinaz.com/reverse?host=' + \
                self.source + '&ddlSearchMode=1'
        if self.search_mod == 2:
            self.source = '+'.join(self.source.split(' '))
            target_url = 'http://whois.chinaz.com/reverse?host=' + \
                self.source + '&ddlSearchMode=2'

        find = urllib2.urlopen(target_url).read()
        if chardet.detect(find)['encoding'] == 'GB2312':
            find = unicode(find, "gb2312").encode('utf-8')
        page = etree.HTML(find)
        original_urls = page.xpath(
            '//*[@id="detail"]/table/tbody/tr/td[1]/a/@href')
        j = 0
        for i in original_urls:
            original_urls[j] = urlparse.urlparse(i).path[1:]
            j = j + 1
        self.domain = original_urls
        # print self.domain

    def write_todb(self):
        table_name = 'whois_reverse'
        print 'whois_reverse domain', self.domain
        for i in self.domain:
            table_name = 'whois_reverse'
            fields = ['id']  # wait to select fields
            wheres = {'domain': [i, 's'],
                      'original_domain': [self.original_domain, 's']}
            flag = self.mysql_handle.require_get(
                table_name, fields, wheres, get_type='select', fetch_type='one')
            if flag is False:
                fields = {'domain': [i, 's'],
                          'original_domain': [self.original_domain, 's']}
                self.mysql_handle.require_post(
                    table_name, fields, post_type='insert')

if __name__ == '__main__':
    a = WhoisReverse()
    a.get_reverse_whois('huitu8.com')
