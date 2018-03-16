# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import socket


class FormatUrl():

    def __init__(self):
        pass

    def match_url(self, url, web_urls):
        web_exist_relative_urls = []
        pose_1 = url.find('//') + 2
        host = url[pose_1:]
        pose_2 = host.find('/') + 1
        domain = url[: pose_1 + pose_2]

        if url.find('ieasy5.com') != -1:
            tmp_urls = []
            '''加拿大：http://ieasy5.com/bbs/thread.php?fid=6
                链接中为： read.php?tid=5695
                数据存储为：http://ieasy5.com/bbs/read.php?tid=5664
            '''
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = url[:url.rfind('/') + 1] + web_url
                tmp_urls.append(web_url)

            return tmp_urls, web_exist_relative_urls

        if url.find('forum.memehk.com') != -1:
            '''
                谜米：http://forum.memehk.com/forum.php?mod=forumdisplay&fid=62
                链接中为：forum.php?mod=viewthread&tid=180122&extra=page%3D1
                存储数据：http://forum.memehk.com/forum.php?mod=viewthread&tid=179998
            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = domain + web_url[:web_url.rfind('&')]
                tmp_urls.append(web_url)
            return tmp_urls, web_exist_relative_urls

        if url.find('forum.vanhi') != -1:

            ''' 温哥华巅峰网：http://forum.vanhi.com/forum-38-1.html
                链接中为： forum.php?mod=viewthread&tid=236078&extra=page%3D1
                数据存储为：http://forum.vanhi.com/forum.php?mod=viewthread&tid=236078
            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = 'http://forum.vanhi.com/' + \
                    web_url[:web_url.rfind('&')]
                tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('wailaike') != -1:
            '''
                外来客 http://www.wailaike.net/group_post?gid=1    外来客-大揭秘版块
                链接中为: /post?id=5248
                存储数据：http://www.wailaike.net/post?id=5211

            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                if web_url.find('/') != -1:
                    web_url = 'http://www.wailaike.net' + web_url
                else:
                    web_url = 'http://www.wailaike.net/' + web_url
                tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('bbs.onmoon.com') != -1:
            '''
                飞月网 ：http://bbs.onmoon.com/forum.php?mod=forumdisplay&fid=48      飞月网-博论天下
                飞月网 ：http://bbs.onmoon.com/forum.php?mod=forumdisplay&fid=56      飞月网-军事时政
                链接中为: forum.php?mod=viewthread&tid=11753&extra=page%3D1
                存储数据：http://bbs.onmoon.com/forum.php?mod=viewthread&tid=11053&extra=
            '''

            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = domain + web_url[:web_url.rfind('=') + 1]
                tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('enewstree') != -1:
            '''
                消息树 ：http://enewstree.com/discuz/portal.php             消息树主页
                链接中为: forum.php?mod=viewthread&tid=93710                消息树相对链接
                存储数据：http://enewstree.com/discuz/forum.php?mod=viewthread&tid=82388&extra=

                消息树 ：http://enewstree.com/discuz/forum.php?mod=forumdisplay&fid=47             消息树-论坛-时政杂谈
                链接中为: forum.php?mod=viewthread&tid=93710&extra=page%3D1                板块相对链接
            '''
            if url.find('portal') != -1:
                tmp_urls = []
                for web_url in web_urls:
                    if web_url.find('=') != -1:
                        web_exist_relative_urls.append(web_url)
                        tid = web_url.split('=')[-1]
                        web_url = domain + 'discuz/forum.php?mod=viewthread&tid=' + tid + '&extra='
                        tmp_urls.append(web_url)
                # print tmp_urls
                return tmp_urls
            else:
                tmp_urls = []
                for web_url in web_urls:
                    web_exist_relative_urls.append(web_url)
                    web_url = domain + 'discuz/' + \
                        web_url[:web_url.rfind('=') + 1]
                    tmp_urls.append(web_url)
                # print tmp_urls
                return tmp_urls, web_exist_relative_urls

        if url.find('bbs.creaders.net') != -1:
            '''
                万维读者 ： http://bbs.creaders.net/life/
                链接中为:bbsviewer.php?btrd_id=4131820&btrd_trd_id=1109373
                存储数据：http://bbs.creaders.net/life/bbsviewer.php?trd_id=1109217
            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = url + web_url
                tmp_urls.append(web_url)
            return tmp_urls, web_exist_relative_urls

        if url.find('qidian.ca') != -1:
            '''
                起点网板块：http://bbs.qidian.ca/forum-7-1.html
                链接中为: thread-14578-1-1.html
                存储数据：http://bbs.qidian.ca/viewthread.php?tid=13981&extra=
            '''
            tmp_urls = []
            for web_url in web_urls:
                if web_url.find('-') != -1:
                    if len(web_url.split('-')) == 4:
                        web_exist_relative_urls.append(web_url)
                        url_s = web_url.split('-')
                        tid = url_s[1]
                        web_url = domain + 'viewthread.php?tid=' + tid + '&extra='
                        tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('mingjingnews') != -1:
            '''
                明镜网 ：http://www.mingjingnews.com/MIB/index.aspx
                链接中为: /MIB/blog/blog_contents.aspx?ID=0000690000000844
                存储数据：http://www.mingjingnews.com/MIB/blog/blog_contents.aspx?ID=0000700900000013
            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                if web_url[0] != '/':
                    web_url = domain + web_url
                else:
                    web_url = web_url[1:]
                    web_url = domain + web_url
                    tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('backchina') != -1:
            '''
                倍可亲论坛 ：http://www.backchina.com/forum/37/index-1.html    倍可亲-时事热点-时事述评   板块
                链接中为: forum/20151212/info-1338125-1-1.html                 
                存储数据：http://www.backchina.com/forum.php?mod=viewthread&tid=1333357&extra=
            '''
            '''
                倍可亲博客 ：http://www.backchina.com/blog/hot/cat-8/    倍可亲博客-政经军事   板块
                链接中为: http://www.backchina.com/blog/173958/article-239131.html           相对链接       
                存储数据：http://www.backchina.com/home.php?mod=space&uid=357583&do=blog&quickforward=1&id=239376
            '''
            if url.find('forum/37/index-1') != -1:
                tmp_urls = []
                for web_url in web_urls:
                    if web_url.find('-') != -1:
                        if len(web_url.split('/')) == 3:
                            web_exist_relative_urls.append(web_url)
                            tid = web_url.split('-')[1]
                            web_url = domain + 'forum.php?mod=viewthread&tid=' + tid + '&extra='
                            tmp_urls.append(web_url)

            elif url.find('hot/cat-8') != -1:
                tmp_urls = []
                for web_url in web_urls:
                    if web_url.find('-') != -1:
                        if web_url.find('article') != -1:
                            if len(web_url.split('/')) == 6:
                                web_exist_relative_urls.append(web_url)
                                uid = web_url.split('/')[4]
                                tid = web_url.split('-')[1].split('.')[0]
                                web_url = domain + 'home.php?mod=space&uid=' + \
                                    uid + '&do=blog&quickforward=1&id=' + tid
                                tmp_urls.append(web_url)

            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        if url.find('chinesenewsgroup') != -1:
            '''
                大中资讯网 ：http://chinesenewsgroup.com/forum/436        论坛-学习工作  板块
                链接中为: /forum/thread/624297                            相对链接
                存储数据：http://chinesenewsgroup.com/forum/thread/624287
            '''
            tmp_urls = []
            for web_url in web_urls:
                web_exist_relative_urls.append(web_url)
                web_url = web_url[1:]
                web_url = domain + web_url
                tmp_urls.append(web_url)
            # print tmp_urls
            return tmp_urls, web_exist_relative_urls

        else:
            return web_urls, web_urls


if __name__ == '__main__':
    r = FormatUrl()
    web_urls = ['forum/20160117/info-1346803-1-1.html']
    r.match_url(
        'http://www.backchina.com/forum/37/index-1.html', web_urls)
    # http://enewstree.com/discuz/forum.php?mod=viewthread&tid=93313&extra=

    # 我在这里重新写了按照这个顺序
