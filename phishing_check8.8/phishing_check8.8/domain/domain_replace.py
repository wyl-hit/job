#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    URL生成器
    time:2015.4.10
    输入：
        domain.config 主机域名变换规则，包括：a=b, a=b,c,d, a,b=c,d
        top.config 顶级域名变换规则，包括：a=b, a=b,c,d
        path.config   路径变换规则
        original_domain.config 原始url文件，格式是http://www.baidu.com/
    接口：
        host_rule_obtain()：读取domain.config并修改保存的规则
        top_rule_obtain()：读取top.config并修改保存的规则
        path_rule_obtain()：读取path.config并修改保存的规则
        Domain_change(Domain)：变换给定的域名
        URL_splice：路径拼接，URL生成
        url_analysis():对原始URL进行分词处理，得到后缀和主机名用于替换
        dns_check():用于对得到的URL存在性检测
    输出：
        整个文件只包含一个类URLGenerator,类中使用了两个yield，
        分别在拿到一条IP存在的可疑URL
        和得到一个对该URL路径拼接后的列表处
        框架实例化一个该类的对象，调用类的function（）函数，
        函数将这个列表返回给调用框架，下次调用时，因为yield本身的性质，
        函数会从上次yield的地方继续执行
    仍存在问题：
        生成的网站因为域名不存在而被重定向到导航网站的问题，
        现在准备采用的是比较简单的过滤方式，因为一般是重定向到运营商的那几个导航网站，
        可以添加已知的运营商导航网站的IP，再IP探测的时候直接过滤
        采用查whios的方式也可以解决，但是会比较慢，而且不稳定。后期有需要可分两次过滤
        替换一个字符串中任意一个字符，比如google,o-0,现在为g00gle，目标为go0gle,g0ogle
'''
import re
import socket
import urlparse
#import traceback
import sys
import os

from extra_opration import get_hash_path

current_path = sys.path[0]


class URLGenerator(object):

    '''
    update_running_state: changed once host_rule and changed once original_domain
    '''

    def __init__(self, task_id, mongo_operate,
                 update_running_state, wait_change_url_list, original_host_rules=[],
                 original_top_rules=[], original_path_rules=[]):
        self.task_id = task_id
        self.mongo_operate = mongo_operate
        self.update_running_state = update_running_state
        self.wait_change_url_list = wait_change_url_list

        self.original_host_rules = original_host_rules
        self.original_top_rules = original_top_rules
        self.original_path_rules = original_path_rules
        self.host_rule_list = []
        self.top_rule_list = []
        self.path_rule_list = []
        self.exist_change_domain = []
        self.all_change_num = 0  # 所有变换后的域名，没检测存在性
        self.all_exist_change_num = 0  # 所有变换后存在的域名
        self.changed_num = 0  # 变换的原始url数量

        self.host_rule_obtain()
        self.top_rule_obtain()
        self.path_rule_obtain()
        fp = file(current_path + '/filter_IP.txt', 'r')
        self.filter_IP = fp.read().strip().split('\n')

        # 存储对URL分词处理结果
        self.url_protocol = ''
        self.url_server = ''
        self.url_host = ''
        self.url_top = ''

        # 创建对替换后存在的域名去重的路径
        self.hash_root_path = current_path + '/exists_changed_wipe'
        try:
            if not os.path.exists(self.hash_root_path):
                os.mkdir(self.hash_root_path)
        except Exception, e:
            sys.stderr.write('%s, in Wipe_Repetition __init__\n' % e)

    def host_rule_obtain(self):
        '''
        将替换规则存入 self.host_rule_list
        例如规则为：alde=elde，列表中存入元素为[['alde'],['elde']]
        shop,adr=show,hhh(0--9)(a--z)，
        列表中存入元素为[[['alde'],['elde']],[['shop','adr'],['show','hhh(0--9)(a--z)']]]
        '''
        for host_rule in self.original_host_rules:
            host_rule = host_rule.split('=')
            if len(host_rule) == 1:
                continue
            if host_rule[0].find(',') != -1:
                original_host_rule = host_rule[0].split(',')
            else:
                original_host_rule = [host_rule[0]]
            if host_rule[1].find(',') != -1:
                goal_host_rule = host_rule[1].split(',')
            else:
                goal_host_rule = [host_rule[1]]
            self.host_rule_list.append([original_host_rule, goal_host_rule])

    def top_rule_obtain(self):
        '''
        将替换规则存入 self.top_rule_list
        例如规则为 /.com=.net,.cn,.tk，列表中存入元素为['/.com',['.net','.cn','.tk']]
        规则左边开始处加'/'，为转义'.'，避免re.sub时把'.'识别为正则表达式。
        '''
        for top_rule in self.original_top_rules:
            top_rule = top_rule.split('=')
            if len(top_rule) == 1:
                continue
            original_top_rule = top_rule[0]
            if top_rule[1].find(',') != -1:
                goal_top_rule = top_rule[1].split(',')
            else:
                goal_top_rule = [top_rule[1]]
            self.top_rule_list.append([original_top_rule, goal_top_rule])

    def path_rule_obtain(self):
        '''
        将替换规则存入 self.path_rule_list
        例如规则为/bank.asp，/icbc.asp,列表中存入元素为['/bank.asp','/icbc.asp']
        '''
        for path_rule in self.original_path_rules:
            if len(path_rule) == 1:
                continue
            self.path_rule_list.append(path_rule)

    def judge_host_exist(self, original_host_list, goal_Domain):
        '''
        检查待替换的goal_Domain是否包含域名规则左边
        '''
        for original_host in original_host_list:
            if re.search(original_host, goal_Domain) is None:
                return False
        return True

    def replace_top(self, goal_Domain):
        '''
        对原始域名的顶级域名进行替换，替换后URL结果存入 toped_Domain_list 返回
        '''
        toped_Domain_list = []
        for top_rule in self.top_rule_list:
            original_top_rule = top_rule[0]
            '''
            先获取后缀，对后缀替换，替换结束后更新成URL，继续操作
            '''
            for goal_top_rule in top_rule[1]:
                replaced_top = re.sub(
                    original_top_rule, goal_top_rule, self.url_top)  # 只对后缀找匹配子串
                replaced_url = self.url_protocol + self.url_server + \
                    self.url_host + replaced_top  # 对后缀替换后重新拼接成完整URL
                if replaced_url != goal_Domain:
                    toped_Domain_list.append(replaced_url)
        toped_Domain_list.append(goal_Domain)
        return toped_Domain_list

    def dash_host_obtain(self, goal_host):
        '''
        对域名变换规则中含有 破折号:"--" 的进行解析，破折号可有多个，解析结果存入 dash_host
        例如：a--z，即从字母a到字母z依次替换一遍
        实例：zjstvabc.com 替换规则为：      zj(/w+)=zj(a--z)(e--h)abc(1--9)
        goal_host = zj(a--z)(e--h)abc(1--9)
        k = ['zj(a', 'z)(e', 'h)abc(1', '9)']
        处理后dash_host=['zj','a','z',' ','e','h','abc','1','9',' ']
        k[0][-1]--k[1][0]
        k[1][-1]--k[2][0]
        k[2][-1]--k[3][0]
        设 -- 数量为n，len（k）= n-1
        '''
        goal_host_splited = goal_host.split('--')
        dash_host = []
        m = len(goal_host_splited)
        n = 0
        while True:
            if n == m:
                break
            if n == 0:
                dash_host.append(goal_host_splited[n][:-2])
                dash_host.append(goal_host_splited[n][-1])
                n += 1
                continue
            if n == m - 1:
                dash_host.append(goal_host_splited[n][0])
                dash_host.append(goal_host_splited[n][2:])
                n += 1
                continue
            dash_host.append(goal_host_splited[n][0])
            dash_host.append(goal_host_splited[n][2:-2])
            dash_host.append(goal_host_splited[n][-1])
            n += 1
        return dash_host

    def dns_check(self, goal_url_list):
        '''
        对列表中的所有URL检测，返回IP存在的URL列表
        '''
        temp_url_list = []
        for goal_url in goal_url_list:
            ip = ""
            if goal_url.find("//") != -1:
                path = goal_url[goal_url.find("//") + 2:]
            else:
                path = goal_url
            try:
                ip = socket.gethostbyname(path)
            except:  # Exception as e:
                ip = "Fail"
            if ip != "Fail" and ip not in self.filter_IP:
                temp_url_list.append(goal_url)
        return temp_url_list

    def dash_replace(self, original_host, dash_host, goal_Domain):
        '''
        对含有破折号的域名变换规则进行变换
        将goal_Domain的域名original_host，替换为dash_host中的每一个域名，并存入 replaced_Domain
        '''
        m = len(dash_host)
        n = 0
        temp_domainlist_1 = ['']  # 为了第一次能进入循环
        temp_domainlist_2 = []
        while n + 1 != m:
            for x in temp_domainlist_1:
                temporary = ord(dash_host[n + 1])  # 取ascll码
                while True:
                    if temporary is None:
                        break
                    temp_h_domain = x + dash_host[n] + chr(temporary)
                    temp_domainlist_2.append(temp_h_domain)
                    if temporary == ord(dash_host[n + 2]):
                        temporary = None
                    else:
                        temporary = temporary + 1
            n += 3
            temp_domainlist_1 = temp_domainlist_2
            temp_domainlist_2 = []
        for x in temp_domainlist_1:
            temp_h_domain = x + dash_host[n]
            temp_domainlist_2.append(temp_h_domain)
            replaced_Domain = []
        for y in temp_domainlist_2:
            '''
            只对主机名替换，替换后再对URL进行拼接
            '''
            dash_replaced_host = re.sub(original_host, y, self.url_host)
            dash_replaced_Domain = self.url_protocol + \
                self.url_server + dash_replaced_host + self.url_top
            replaced_Domain.append(dash_replaced_Domain)
        return replaced_Domain  # 对含破折号替换后的域名，一个列表，含有多条域名

    def once_replace(self, original_host, goal_host, goal_Domain):
        '''
        对goal_Domain的域名original_host，替换为goal_host指定的域名
        结果存入 replaced_Domain，若没有发生替换，例如规则为:a=a,则返回[]
        '''
        replaced_Domain = []
        m = re.search('--', goal_host)
        if m is not None:

            dash_host = self.dash_host_obtain(goal_host)
            replaced_Domain = self.dash_replace(
                original_host, dash_host, goal_Domain)
        else:
            replaced_host = re.sub(original_host, goal_host, self.url_host)
            replaced_Domain = [
                self.url_protocol + self.url_server + replaced_host + self.url_top]  # 只含有一条URL
            if replaced_Domain[0] == goal_Domain:
                replaced_Domain = []
        return replaced_Domain

    def Domain_change(self, original_Domain):
        '''
        进行域名替换
        输入一条目标域名，替换结果通过yield返回到调用程序
        '''
        # replaced_Domain = []  # 存放替换后的域名
        if original_Domain is None:
            return  # 使用yield不能和return none一起，但可以直接用return
        toped_Domain_list = self.replace_top(original_Domain)
        for goal_Domain in toped_Domain_list:  # 对后缀替换结束
            self.url_analysis(goal_Domain)
            for host_rule in self.host_rule_list:
                original_host_list = host_rule[0]
                goal_host_list = host_rule[1]
                if not self.judge_host_exist(original_host_list, goal_Domain):
                    continue  # 左边域名规则不匹配
                rule_num = len(original_host_list)
                if rule_num == 1:  # 处理 a=b or a=b,c,d 这两种规则
                    original_host = original_host_list[0]
                    for goal_host in goal_host_list:
                        '''
                        经过替换的url列表暂存在end_replace_Domain中，
                        对它们进行IP检测，并对返回的ip存在URL列表循环yield
                        '''
                        end_replace_Domain = self.once_replace(
                            original_host, goal_host, goal_Domain)
                        self.all_change_num += len(end_replace_Domain)
                        end_replace_Domain = self.dns_check(end_replace_Domain)
                        if end_replace_Domain != []:
                            self.exist_change_domain.extend(end_replace_Domain)
                            for temp_replace_Domain in end_replace_Domain:
                                yield temp_replace_Domain

                else:  # 处理 a,b=c,d 这种规则，需迭代处理，即对a替换c之后的结果进行b替换d
                    iter_replaced_list = [goal_Domain]
                    for i in range(rule_num):
                        temp_result_list = []
                        for iter_Domain in iter_replaced_list:
                            temp_result_list += self.once_replace(
                                original_host_list[i], goal_host_list[i], iter_Domain)
                        iter_replaced_list = temp_result_list
                    self.all_change_num += len(end_replace_Domain)
                    end_replace_Domain = self.dns_check(iter_replaced_list)
                    if end_replace_Domain != []:
                        self.exist_change_domain.extend(end_replace_Domain)
                        for temp_replace_Domain in end_replace_Domain:
                            yield temp_replace_Domain
            # 对顶级域名变换后，没有进行主机域名变换的URL进行DNS检测，存在则返回
            self.all_change_num += 1
            end_replace_Domain = self.dns_check([goal_Domain])
            # 无效域名
            if end_replace_Domain == [] or end_replace_Domain == [original_Domain]:
                continue
            else:
                self.exist_change_domain.append(goal_Domain)
                temp_replace_Domain = end_replace_Domain[0]
            yield temp_replace_Domain

    def url_analysis(self, url):
        '''
        url解析函数
        例如对于url如"http://www.baidu.api.com.cn"
        url_protocol='http://'
        url_server='www.'
        url_host = 'baidu.api'
        url_top = '.com.cn'
        '''
        if not url.startswith('http'):
            url = 'http://' + url
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
        parts = urlparse.urlparse(url)
        host = parts.netloc
        self.url_protocol = parts.scheme + '://'
        temp_host = host.split('.')
        #print temp_host
        if ('.' + temp_host[-2] + '.' + temp_host[-1]) in topHostPostfix:
            self.url_top = '.' + temp_host[-2] + '.' + temp_host[-1]
            self.url_host = temp_host[-3]
            if len(temp_host) > 3 and temp_host[:-3] != '':
                i = temp_host[0]
                for j in temp_host[1:-3]:
                    i = i + '.' + j
                self.url_server = i + '.'
        else:
            self.url_top = '.' + temp_host[-1]
            self.url_host = temp_host[-2]
            if len(temp_host) > 2 and temp_host[:-2] != '':
                i = temp_host[0]
                for j in temp_host[1:-2]:
                    i = i + '.' + j
                self.url_server = i + '.'

    def URL_splice(self, original_domain, end_replace_Domain):
        '''
        URL拼接函数，对于传进来的一条域名，拼接上所有config文件中的路径，返回一个列表
        '''
        # 还原真实URL格式
        splice_url_list = [original_domain + '/', end_replace_Domain + '/']
        for path_rule in self.path_rule_list:
            goal_url = end_replace_Domain + path_rule
            splice_url_list.append(goal_url)
        return splice_url_list

    def exist_url_wipe_repeat(self, url_list):
        '''
        基于Hash目录树的URL去重，对变换后存在的域名去重
        接收URL列表，输出不存在的URL列表
        '''
        url_exist_list = []  # 储存hash目录树中不存在的url
        for url in url_list:
            # md5_path is like adcf4789/aedcb874/.../...
            hash_path = get_hash_path(url)
            folder_list = hash_path.split('/')
            exist_flag = 1
            current_path = self.hash_root_path
            for folder_name in folder_list:
                current_path = current_path + '/' + folder_name
                if os.path.exists(current_path):
                    continue
                else:
                    os.mkdir(current_path)
                    exist_flag = 0  # 目录不存在 标志位置为零
            if exist_flag == 0:
                url_exist_list.append(url)
        return url_exist_list

    def URL_Generator(self):
        '''
        框架实例化类的一个对象后调用的函数，这个函数自动读取原始URL文件，
        返回一个含有相同域名不同路径的可疑URL列表，下次调用，继续返回
        '''
        for original_domain in self.wait_change_url_list:
            print original_domain
            #self.all_change_domain = []
            self.exist_change_domain = []
            if original_domain[-1] == '/':
                original_domain = original_domain[:-1]
            elif original_domain[-2:] == '/\n':
                original_domain = original_domain[:-2]
            elif original_domain[-1] == '\n':
                original_domain = original_domain[:-1]
            self.url_analysis(original_domain)
            self.changed_num += 1
            for end_replace_Domain in self.Domain_change(original_domain):
                # 每次返回一组[原始域名, 变换后存在的域名, 该路径拼接后的URL]
                # restore real url format
                # example: http://www.baidu.com/ from http://www.baidu.com
                #print original_domain, end_replace_Domain
                yield self.URL_splice(original_domain, end_replace_Domain)
            self.all_exist_change_num += len(self.exist_change_domain)
            real_domain_format = []
            for exist_domain in self.exist_change_domain:
                real_domain_format.append(exist_domain + '/')
            self.exist_change_domain = real_domain_format
            new_exist_domain = self.exist_url_wipe_repeat(
                self.exist_change_domain)
            self.mongo_operate.add_changed_domain(
                original_domain +
                '/', new_exist_domain, self.exist_change_domain,
                self.task_id, self.original_host_rules, self.original_top_rules,
                self.original_path_rules, self.all_change_num)
            self.update_running_state(self.all_change_num, self.all_exist_change_num,
                                      self.changed_num, 0, 0)

if __name__ == '__main__':
    url_gen = URLGenerator(task_id=3, task_start_time='2015-04-25 16:40:40', mysql_host='172.31.159.248', mysql_user='root', mysql_password='', mysql_db='phishing_check',  mongo_db='domain_test',
                           mongo_host='172.31.159.248', mongo_port=27017, mongo_user='root', mongo_password='', protected_list_id=[3, 9, 14], host_rule_id=[1, 2, 6, 8, 10], top_rule_id=[1, 3], path_rule_id=[1, 4, 6])
    domain_change_url = url_gen.URL_Generator()  # 创建生成器
    while 1:
        try:
            url_list = domain_change_url.next()
        except StopIteration:
            break
        print url_list
    print 'program over'
