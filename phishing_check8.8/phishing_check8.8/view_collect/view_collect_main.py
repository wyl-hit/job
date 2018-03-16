#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from view_get_feature import ViewPageBlock
from web_save_path import WebSavePath


class ViewCollectMain():

    def __init__(self, mongo_operate, current_path):

        self.mongo_operate = mongo_operate
        self.vtree = []
        self.current_path = current_path

    def view_work(self, url, web_type):

        self.vtree = []
        h = WebSavePath()
        filename, path = h.get_html_path_abs(url, web_type)
        if path is not None:
            self.vtree = self.mongo_operate.get_web_tree(
                url, web_type)  # 根据url 获取网页视觉块信息
            if self.vtree is False or self.vtree == []:
                    return None
            p = ViewPageBlock(
                path, self.vtree, self.current_path, url, self.mongo_operate, web_type)
            p.gather_vips_pic()  # 获取网页图像特征
            p.save_feature()     # 格式化图像特征，存入mongo
        else:
            sys.stderr.write(' view_work:no this path')
            return None


if __name__ == '__main__':

    url = 'http://www.amazon.cn/'
    br = ViewCollectMain()
    br.view_work(url)
