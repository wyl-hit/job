# -*-coding:utf-8-*-
from lxml import etree
import codecs
import urllib2
import sys
import chardet
reload(sys)
sys.setdefaultencoding('utf-8')
import re

f=codecs.open("6.html","r","utf-8")
content=f.read()
f.close()
tree=etree.HTML(content)

'''
daohang1 = tree.xpath('//ul[@id="siteNavPart1"]/li/a/@href')
daohang2 = tree.xpath('//ul[@id="siteNavPart2"]/li/a/@href')

print daohang1[2:]
print daohang2[1:-1]

roll = tree.xpath('//ul[@id="channelNavPart"]/li/a/@href')
print roll


#basic content

head = tree.xpath('//div[@class="slist"]//li/a/@href')
print head

content = tree.xpath('//div[contains(@class, "pList")]/div/div[@class="text"]/em/a/@href')
print len(content)

# fenye   content
'''
'''content = tree.xpath('//div[contains(@class, "pList")]/div/div//h3/a/@href | //div[contains(@class, "pList")]/div//em/a/@href')
for i in content:
    print i'''


'''#qiche 

content = tree.xpath('//div[contains(@bosszone, "yw")]/ul/li/a/@href')
for i in content:
    print i'''
 
#www.qq.com  contentRight contentRightNba
'''content = tree.xpath('//div[@class="txtArea"]/h3/a/@href  | //div[@class="contentLeft"]/ul/li/a/@href | //div[contains(@class, "contentRight")]/ul/li/a/@href')

content = tree.xpath('//*[contains(@id, "newsContent")]/ul/li/a/@href  | //*[contains(@id, "newsContent")]/div/h3/a/@href ')
print len(content)
for i in content:
    print i

content = tree.xpath('//div[@class="ft"]/ul/li/a/text() | //div[@class="ft"]/h3/a/text()')
'''

'''content = tree.xpath('//span[@class="a_time"]/text()')
print len(content)
for i in content:
    print i'''



'''content = tree.xpath('//*[@id="cmtNum"]/text()') 
#print ''.join(content)

content = tree.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()') 
#print ''.join(content)'''

title = tree.xpath('//div[@class="qq_article"]/div[1]/h1/text() | //div[@class="LEFT"]/h1/text() | //*[@id="C-Main-Article-QQ"]/div[1]/h1/text() | //p[@class="title"]/text() ') 
print ''.join(title).strip()
'''
listp = re.findall(r'pubtime:(.*?[^,]),', content, re.S)
print listp[0].replace(u'年' ,'-').replace(u'月' ,'-').replace(u'日' ,' ')


content = tree.xpath('//*[@id="cmtNum"]/text()') 
print content'''

import time
import requests
'''cmt_id = '2273295119'
payload = {'targetid':cmt_id, 'callback': '_cbSum', '_': str(long(time.time()))}
ajax_url = 'http://openapi.inews.qq.com/getQQNewsNormalContent?id=20171205C0ZFKR00&chlid=news_rss&refer=mobilewwwqqcom&otype=jsonp&callback=getNewsContentOnlyOutput'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
r = requests.get(ajax_url, headers=headers, params=payload)
print r.text'''

'''data = 'getNewsContentOnlyOutput({"ret":0,"is_deleted":0,"id":"20171205C0ZFKR00","title":"\u6cb3\u5317\u88ab\u66dd\u591a\u6240\u5c0f\u5b66\u672a\u4f9b\u6696 \u7701\u6559\u80b2\u5385\uff1a\u4e25\u8083\u67e5\u5904\u56e0\u53d6\u6696\u9020\u6210\u4e25\u91cd\u95ee\u9898\u7684\u5b66\u6821","url":"http:\/\/kuaibao.qq.com\/s\/20171205C0ZFKR00","kurl":null,"atype":"0","img":{"imgurl":"","imgurl_small":null,"qqnews_thu_big":null,"qqnews_thu":null},"cid":"2274824699","src":"\u65b0\u4eac\u62a5","time":1512485943,"pubtime":"2017-12-05 10:59:03","topic":"","surl":"http:\/\/kuaibao.qq.com\/s\/20171205C0ZFKR00?refer=","content":[{"type":1,"value":"\u3000\u3000\u65b0\u4eac\u62a5\u5feb\u8baf(\u8bb0\u8005 \u738b\u4fca)\u8fd1\u65e5\uff0c\u6cb3\u5317\u591a\u6240\u4e61\u6751\u5c0f\u5b66\u88ab\u66dd\u81f3\u4eca\u6ca1\u6709\u4f9b\u6696\uff0c\u5b66\u751f\u53bb\u64cd\u573a\u8dd1\u6b65\u53d6\u6696\uff0c\u6709\u5c0f\u5b66\u751f\u51fa\u73b0\u51bb\u4f24\u72b6\u51b5\u3002\u5bf9\u6b64\uff0c\u4eca\u65e5\u6cb3\u5317\u7701\u6559\u80b2\u5385\u53d1\u5e03\u300a\u5173\u4e8e\u8fdb\u4e00\u6b65\u505a\u597d\u4e2d\u5c0f\u5b66\u51ac\u5b63\u53d6\u6696\u5de5\u4f5c\u7684\u901a\u77e5\u300b\uff0c\u63d0\u51fa\u5bf9\u4e8e\u56e0\u51ac\u5b63\u53d6\u6696\u9020\u6210\u4e25\u91cd\u95ee\u9898\u7684\uff0c\u8981\u4e25\u8083\u67e5\u5904\uff0c\u5e76\u8ffd\u7a76\u6709\u5173\u5355\u4f4d\u548c\u4eba\u5458\u7684\u8d23\u4efb\u3002"},{"type":1,"value":"\u3000\u3000\u6700\u8fd1\u6709\u5a92\u4f53\u62a5\u9053\u6cb3\u5317\u7701\u4fdd\u5b9a\u5e02\u66f2\u9633\u53bf\u591a\u6240\u5c0f\u5b66\u81f3\u4eca\u672a\u53d6\u6696\uff0c\u56e0\u4e3a\u592a\u51b7\uff0c\u6709\u8001\u5e08\u5e26\u7740\u5b66\u751f\u53bb\u64cd\u573a\u8dd1\u6b65\u53d6\u6696\uff0c\u751a\u81f3\u4e00\u4e9b\u5b66\u751f\u51fa\u73b0\u4e86\u51bb\u4f24\u60c5\u51b5\u3002"},{"type":1,"value":"\u3000\u3000\u5bf9\u4e8e\u4e3a\u4f55\u8fdf\u8fdf\u6ca1\u6709\u4f9b\u6696\uff0c\u66f2\u9633\u53bf\u6559\u80b2\u5c40\u4e00\u4f4d\u76f8\u5173\u8d1f\u8d23\u4eba\u63a5\u53d7\u91c7\u8bbf\u65f6\u8868\u793a\uff0c\u56e0\u4e3a\u4eca\u5e74\u66f2\u9633\u53bf\u6240\u6709\u5b66\u6821\u7684\u4f9b\u6696\u8fdb\u884c\u201c\u7164\u6539\u7535\u201d\u6539\u9020\uff0c\u4f46\u5de5\u7a0b\u6ca1\u6709\u6309\u65f6\u5b8c\u5de5\uff0c\u6240\u4ee5\u5c31\u51fa\u73b0\u4e86\u90e8\u5206\u5c0f\u5b66\u672a\u80fd\u4f9b\u6696\u7684\u72b6\u51b5\u3002"},{"type":1,"value":"\u3000\u3000\u4eca\u5929\uff0c\u6cb3\u5317\u7701\u6559\u80b2\u5385\u4e0b\u53d1\u4e86\u300a\u5173\u4e8e\u8fdb\u4e00\u6b65\u505a\u597d\u4e2d\u5c0f\u5b66\u51ac\u5b63\u53d6\u6696\u5de5\u4f5c\u7684\u901a\u77e5\u300b\u3002"},{"type":1,"value":"\u3000\u3000\u300a\u901a\u77e5\u300b\u8868\u793a\uff0c\u5404\u5e02\u6559\u80b2\u884c\u653f\u90e8\u95e8\u8981\u5bf9\u6240\u8f96\u5404\u53bf(\u5e02\u3001\u533a)\u4e2d\u5c0f\u5b66\u51ac\u5b63\u53d6\u6696\u5de5\u4f5c\u8fdb\u884c\u5168\u9762\u68c0\u67e5\u3002\u5404\u53bf(\u5e02\u3001\u533a)\u8981\u7531\u53bf\u6559\u80b2\u884c\u653f\u90e8\u95e8\u9886\u5bfc\u5e26\u961f\uff0c\u7ec4\u6210\u68c0\u67e5\u7ec4\uff0c\u6df1\u5165\u6240\u5c5e\u5b66\u6821\u5f00\u5c55\u5b9e\u5730\u68c0\u67e5\u3002\u68c0\u67e5\u5185\u5bb9\u5305\u62ec\uff1a\u4e2d\u5c0f\u5b66\u6821\u51ac\u5b63\u53d6\u6696\u8bbe\u65bd\u8fd0\u8f6c\u3001\u66f4\u65b0\u7ef4\u62a4\uff0c\u5efa\u7acb\u5e94\u5bf9\u7a81\u53d1\u4e8b\u4ef6\u548c\u6781\u7aef\u6076\u52a3\u5929\u6c14\u5e94\u6025\u54cd\u5e94\u673a\u5236\u60c5\u51b5\u7b49\u60c5\u51b5\u3002\u662f\u5426\u5168\u9762\u843d\u5b9e\u6e05\u6d01\u80fd\u6e90\u53d6\u6696\uff0c\u4f7f\u7528\u7a7a\u8c03\u6216\u7535\u6696\u6c14\u53d6\u6696\u7684\u5b66\u6821\uff0c\u662f\u5426\u53ca\u65f6\u7535\u8def\u68c0\u4fee\u548c\u6539\u9020\u3002\u519c\u6751\u4e2d\u5c0f\u5b66\u6821\u5c24\u5176\u662f\u5bc4\u5bbf\u5236\u5b66\u6821\uff0c\u662f\u5426\u6709\u4e13\u4eba\u8d1f\u8d23\u53d6\u6696\u5b89\u5168\u5de5\u4f5c;\u662f\u5426\u5efa\u7acb\u5065\u5168\u4e86\u5404\u9879\u89c4\u7ae0\u5236\u5ea6\u3002\u662f\u5426\u5b58\u5728\u56e0\u8bbe\u65bd\u7ef4\u62a4\u4e0d\u53ca\u65f6\u3001\u8d44\u91d1\u62e8\u4ed8\u4e0d\u5230\u4f4d\u548c\u5b89\u5168\u8d23\u4efb\u5236\u672a\u843d\u5b9e\u7b49\u539f\u56e0\uff0c\u9020\u6210\u5b66\u6821\u4e0d\u80fd\u6b63\u5e38\u53d6\u6696\u6216\u53d6\u6696\u6e29\u5ea6\u8fbe\u4e0d\u5230\u8981\u6c42\u7684\u73b0\u8c61\u3002"},{"type":1,"value":"\u3000\u3000\u300a\u901a\u77e5\u300b\u8fd8\u6307\u51fa\uff0c\u5404\u7ea7\u5bf9\u4e8e\u68c0\u67e5\u4e2d\u53d1\u73b0\u7684\u672a\u6b63\u5e38\u4f9b\u6696\u3001\u968f\u610f\u7f29\u77ed\u4f9b\u6696\u65f6\u95f4\u3001\u964d\u4f4e\u4f9b\u6696\u6807\u51c6\u3001\u5b58\u5728\u53d6\u6696\u5b89\u5168\u9690\u60a3\u7684\u5b66\u6821\uff0c\u8981\u53d1\u73b0\u4e00\u6240\uff0c\u6574\u6539\u4e00\u6240\u3002\u5404\u5b66\u6821\u8981\u52a0\u5f3a\u5bf9\u5b66\u751f\u7684\u53d6\u6696\u5b89\u5168\u6559\u80b2\uff0c\u5c06\u53d6\u6696\u5de5\u4f5c\u6293\u7ec6\u3001\u6293\u5b9e\uff0c\u6293\u5230\u6bcf\u4e00\u95f4\u6559\u5ba4\u3001\u6bcf\u4e00\u95f4\u5bbf\u820d\uff0c\u786e\u4fdd\u4e0d\u7559\u6f0f\u6d1e\uff0c\u4e0d\u843d\u6b7b\u89d2\u3002\u5bf9\u4e8e\u56e0\u51ac\u5b63\u53d6\u6696\u9020\u6210\u4e25\u91cd\u95ee\u9898\u7684\uff0c\u8981\u4e25\u8083\u67e5\u5904\uff0c\u5e76\u8ffd\u7a76\u6709\u5173\u5355\u4f4d\u548c\u4eba\u5458\u7684\u8d23\u4efb\u3002"},{"type":1,"value":"\u3000\u3000\u7f16\u8f91\uff1a\u674e\u4e30"}],"voteId":0,"relate_news_list":[]})'
pubtime = re.findall(r'pubtime":"(.*?[^"])"', data, re.S)
print pubtime[0]

cmt_id = re.findall(r'cid":"(\d*?)",', data, re.S)
print cmt_id[0]

title = ''.join(re.findall(r'title":"(.*?[^"])"', data, re.S))
#print title[0].decode('unicode_escape')
print title
text_list = re.findall(r'value":"(.*?[^"])"', data, re.S)
print ''.join(text_list).decode('unicode_escape')

listp = re.findall(r'commentnum":"(\d*?)"' ,data, re.S)
print listp'''


'''url = 'https://www.sogou.com/suggnew/ajajjson?key=%E7%BA%A2%E9%BB%84%E8%93%9D%20&type=web&ori=yes&pr=web&abtestid=7&ipn=&t=1512574165060&suguuid=82159460-a285-4424-921f-9dfa74535f7c&ip=202.118.236.150&iploc=2301&suid=BDEC76CA556C860A58009DDA00055B69&yyid=null&pid=sogou&policyno=null&mfp=null&hs=https&mp=1&prereq_a=&sugsuv=1479972007941752&sugtime=1512574206632%20Request%20Method:GET'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}
r = requests.get(url, headers=headers)
print r.text'''