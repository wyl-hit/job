#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib2

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from util import Message
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *


class Crawler(QWebView):
	"""docstring for Crawler"""
	def __init__(self, url_list, queue, message_type):
		super(Crawler, self).__init__()
		print "Crawler __init__ start"
		self.url_list = url_list
		self.queue = queue
		title = ""
		self.url = ""
		self.message_type = message_type
		self.pjs = PythonJavascript(self)
		file_read = open(sys.argv[2],"r")
		self.script = file_read.read()
		file_read.close()
		self.page().mainFrame().javaScriptWindowObjectCleared.connect(self.addpjs)
		self.page().mainFrame().loadFinished.connect(self.evaluate_script)


	def addpjs(self):
		print "addpjs start"
		self.page().mainFrame().addToJavaScriptWindowObject("python",self.pjs)

	def crawler_start(self):
		print "crawler_start start"
		if 0==len(self.url_list):
			self.close()
		else:
			self.url = self.url_list.pop()
			print "self.url:",self.url
			self.load(QUrl(self.url))
			#self.page().mainFrame().load(QUrl(self.url))
			#file('2','w').write(unicode(self.mainFrame().load(QUrl(self.url)).encode('utf8'))
			# file_in = open(self.url)
			# self.setHtml(QString(file_in.read()))
			# file_in.close()
	# def crawler_start(self):
	# 	print "crawler_start start"
	# 	data = ""
	# 	while 1:
	# 		if 0==len(self.url_list):
	# 			break
	# 		self.url = self.url_list.pop()
	# 		try:
	# 			request = urllib2.Request(self.url)
	# 			data = urllib2.urlopen(request,timeout=2).read()
	# 		except Exception, ex:
	# 			print Exception,":",ex
	# 			continue
	# 		else:
	# 			break
	# 	if 0==len(self.url_list):
	# 		self.close()
	# 	self.setHtml(QString(data))

	def evaluate_script(self):
		print "evaluate_script start"
		title = self.page().mainFrame().title()
		print title
		file_name = self.url.replace("/","_")
		file_object = open(sys.argv[3], 'w')
		file_object.write(title)
		file_object.close()
		self.page().mainFrame().evaluateJavaScript(self.script)


# class PythonJavascript(QWebView):
class PythonJavascript(QObject):
	"""docstring for PythonJavascript"""
	def __init__(self, crawler):
		super(PythonJavascript, self).__init__()
		print "PythonJavascript __init__ start"
		self.crawler = crawler
		self.message = Message(self.crawler.message_type,{"url":"","vectors":[]}).message
		
	@pyqtSlot("QString","QString")
	def script_call(self,vectors,url):
		print "script_call start"
		#print url
		#self.crawler.show()
		u_url    = unicode(str(url))
		u_vector = unicode(str(vectors))[:-1].split(";")
		print "u_url:",u_url
		#print "u_vector:",u_vector
		self.message["message_param"]["url"] = u_url
		self.message["message_param"]["vectors"] = u_vector
		self.crawler.queue.put(self.message)
		print len(self.crawler.url_list)
		if 0==len(self.crawler.url_list):
			self.message["message_type"] = "over"
			self.crawler.queue.put(self.message)
			self.crawler.close()
		else:
			self.crawler.crawler_start()

def main(data):
	import sys
	from multiprocessing.queues import SimpleQueue
	url_list = []
	try:
		req = urllib2.Request(data[1])
		#res_data = urllib2.urlopen(req)
		kk = 1
	except:
		kk=0
	if kk == 1:
		url_list.append(data[1])
		queue = SimpleQueue()
		message_type = "test"
		app = QApplication(sys.argv)
		crawler = Crawler(url_list,queue,message_type)
		crawler.crawler_start()
		
		sys.exit(app.exec_())
		print crawler.title
	else:
		file_name = data[1].replace("/","_")
		file_object = open(file_name, 'w')
		file_object.write("/*/")
		file_object.close()
	


if __name__ == '__main__':	
	main(sys.argv)
