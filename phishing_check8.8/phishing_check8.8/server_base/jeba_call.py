# -*- coding: utf-8 -*-

import jieba.analyse
import jieba


def cut_all(data):
    '''
    采用全模式分词，即把句子中所有的可以成词的词语都扫描出来
    来到北京大学-->来到/北京/北京大学/大学
    '''
    temp_result = jieba.cut(data, cut_all=True)
    temp_result = '/'.join(temp_result)
    return temp_result


def cut_accurate(data):
    '''
    采用精准模式分词，试图把句子精确切开
    来到北京大学-->来到/北京大学
    '''
    temp_result = jieba.cut(data, cut_all=False)
    temp_result = '/'.join(temp_result)
    return temp_result


def cut_search(data):
    '''
    采用搜索引擎模式分词，在精确模式的基础上，对长词再次切分，
    来到北京大学-->来到/北京/大学/北京大学
    '''
    temp_result = jieba.cut_for_search(data)
    temp_result = '/'.join(temp_result)
    return temp_result


def add_word_dict(word, freq=None, tag=None):
    '''
    向词典中添加新单词
    '''
    jieba.add_word(word, freq=None, tag=None)


def del_word_dict(word):
    '''
    向词典中删除单词
    '''
    jieba.del_word(word)


def get_keyword(data, topK=20, withWeight=False):
    '''
    获取文本的关键词，topK设置为返回的关键词个数，默认为20个
    '''
    temp_result = jieba.analyse.extract_tags(
        data, topK=20, withWeight=False, allowPOS=())
    temp_result = '/'.join(temp_result)
    return temp_result

if __name__ == '__main__':
    # print cut_all('来到北京大学')
    # print cut_search('来到北京大学')
    # print cut_accurate('来到北京大学')
    # print get_keyword('来到北京大学', topK=2, withWeight=True)
    print cut_all('淘宝网 - 淘！我喜欢')
