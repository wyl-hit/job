#!/usr/bin/python
# -*- coding: UTF-8 -*-

from jeba_call import *
import sys
from create_index import CreateIndex
from define_decorator import autoInitClass

current_path = sys.path[0]


@autoInitClass
class TitleMain(object):

    def __init__(self, task_id, task_start_time, protected_title_dict, protected_text_dict,
                 mongo_operate, mysql_handle, url_type='protect'):
        self.task_id = task_id
        self.task_start_time = task_start_time
        self.title_index_path = current_path + '/index'
        self.conf = CreateIndex(
            protected_title_dict, protected_text_dict, self.title_index_path)
        self.list = []
        self.protected_title_dict = protected_title_dict
        self.mongo_operate = mongo_operate  # mongo对象
        self.mysql_handle = mysql_handle
        self.type = url_type

    def title_run(self, gray_url):
        '''
        程序入口
        '''
        results = 0
        char = ""
        try:
            title = self.mongo_operate.get_web_title(
                gray_url, 'gray')  # 获取title
            keyword = self.mongo_operate.get_web_text(gray_url, 'gray')
            if title is False and keyword is False:
                return results
            if keyword:
                keyword_list = keyword.split('/')

        except:
            return results
        words = cut_all(title)
        for w in words:
            char += w + " "
        for key in keyword_list:
            char += key + " "
        check_result = self.checkTitle(gray_url, char)
        return check_result

    def checkTitle(self, gray_url, title):
        """
        查询title并记录
        """
        import whoosh.index as index
        from whoosh.qparser import QueryParser
        d2 = {}
        d1 = {}
        d4 = {}
        ix = index.open_dir(self.title_index_path)
        with ix.searcher() as searcher:
            for i in range(len(title.split(' '))):  # 将字符串转化为列表
                query = QueryParser("content", ix.schema).parse(
                    unicode(title.split(' ')[i]))
                results = searcher.search(query)  # 返回的是一个字典
                for r in results:
                    k = r['title']
                    if k in d1.keys():
                        d1[k] = d1[k] + 1
                    else:
                        d1[k] = 1
        if len(d1.items()) == 0:
            d4['gurl'] = gray_url
            d4['surl'] = "null"
            d4['status'] = "no phishing website"
            self.list.append(d4)
        check_result = 0
        for k, v in d1.items():
            if v < 12:  # 加入阈值，测试时不用
                d4['gurl'] = gray_url
                d4['surl'] = "null"
                d4['status'] = "no phishing website"
                self.list.append(d4)
            else:
                d2['gurl'] = gray_url
                d2['surl'] = k
                d2['status'] = "phishing website"
                self.list.append(d2)
                if self.type is 'protect':
                    self.mysql_handle.undate_gray_list_check_result(
                        gray_url, 'title', source_url=k)  # 保存 钓鱼url

                elif self.type is 'counterfeit':
                    self.mysql_handle.undate_gray_list_check_result(
                        gray_url, 'title', counterfeit_url=k)  # 保存 钓鱼url
                self.mysql_handle.undate_task_result_check_result(
                    self.task_id, self.task_start_time, gray_url, 'title')
                check_result += 1
        return check_result
