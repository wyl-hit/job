#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from whoosh.fields import Schema, KEYWORD, TEXT
from whoosh.index import create_in
from jeba_call import *
import sys


class CreateIndex(object):

    def __init__(self, protected_title_dict, protected_text_dict, title_index):
        self.protected_title_dict = protected_title_dict
        self.protected_text_dict = protected_text_dict
        self.title_index = title_index
        self.mkindex()  # 对白名单建立倒排索引

    def mkindex(self):
        '''
        都取配置文件，建立倒排索引
        '''
        D = {}
        for url in self.protected_title_dict.keys():
            key_title_data = ""
            if 1 == 1:
                title = self.protected_title_dict[url]
                keyword = self.protected_text_dict[url]
                if title == '' and keyword == '':
                    continue
                print title, keyword
                keyword_list = keyword.split('/')

                #char = ulist + " " + title + "\n"
            reload(sys)
            sys.setdefaultencoding('utf-8')
            words = cut_all(title)
            for w in words:
                key_title_data += w + " "
            for w in keyword_list:
                key_title_data += w + " "
            D[url] = key_title_data

            if not os.path.exists(self.title_index):
                os.mkdir(self.title_index)
                # 选择合适的schema属性,title使用TEXT不合适,会被分割开
            schema = Schema(
                title=KEYWORD(stored=True), content=TEXT(stored=True))
            ix = create_in(self.title_index, schema)
            writer = ix.writer()
            # 索引对象的writer()方法返回一个能够让你给索引添加文本的IndexWriter对象
            for k, v in D.items():
                writer.add_document(title=unicode(k), content=unicode(v))
                # 被索引的文本域必须是unicode值
            writer.commit()  # commit()方法让IndexWriter对象将添加的文本保存到索引
