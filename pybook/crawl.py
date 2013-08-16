# -*- coding:utf-8 -*-
import gevent.monkey
gevent.monkey.patch_all()

import gevent

import re
import os
import glob
import sys
import time
import json
import socket
import random
import chardet
import urllib2
from lxml import html

socket.setdefaulttimeout(30)

DEFAULT_ENCODE = 'utf-8'
MEDIA_ROOT = '/home/zg163/data/'
SAVE_JSON = '/home/zg163/data/detail'
DATA_PATH = '/home/zg163/djcode/ireader/pybook/new_data/*.json'

def get_content(url):
	content = ''
	user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
		'Opera/9.25 (Windows NT 5.1; U; en)',
		"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
	]
	headers = {'User-Agent':random.choice(user_agents)}
	req = urllib2.Request(url=url, headers=headers)
	try:
		content = urllib2.urlopen(req).read()
	except urllib2.HTTPError, e:
		if e.code == 503 : 
			time.sleep(30)
			content = tryAgain(req, 0)
	except :
		time.sleep(30)
		content = tryAgain(req, 0)
	return content

def tryAgain(url, retries=0):
	content = ''
	if retries < 4:
		try:
			time.sleep(30)
			content = urllib2.urlopen(req).read()
		except :
			retries += 1
			content = tryAgain(url, retries)
	return content

def parse(url):
	"""
	out = { 'name'; ''
			'intro': ''
			'content': {
				}
	}
	"""
	print 'url', url
	intro = ''
	detail = {}
	regx = re.compile('(?P<pk>\d+)\.html')
	intro_identy = u'内容简介：'
	content = get_content(url)
	doms = html.fromstring(content)
	title = doms.xpath("//h1/text()")[0][:-4]
	trs = doms.xpath("//table/child::tr")
	if trs: 
		items = trs[1:-1]
		intro_dom = trs[0].xpath("child::td/text()") 
		if intro_dom:
			intro = intro_dom[0].split(intro_identy)[-1].strip()
		part = 'A'
		detail[part] = []
		for tr in items:
			tds = tr.xpath("child::td")
			if len(tds) == 1:
				part = tds[0].text
				detail[part] = []
			links = tr.xpath("child::td/a")
			for link in links:
				tmp_dict = {}
				href = link.attrib['href'] 
				match = regx.match(href)
				pk = int(match.group('pk'))
				text = link.text
				book_url = '%s/%s' %(title, pk)
				detail_url = '%s/%s' % (url, href)
				tmp_dict['id'] = pk
				tmp_dict['title'] = text
				tmp_dict['book_url'] = book_url
				detail[part].append(tmp_dict)
	result = {'name': title, 
			  'intro': intro,
			  'content': detail,
	}
	filename = os.path.join(SAVE_JSON, '%s.json' % title.encode('utf-8'))
	with open(filename, 'w') as f:
		json.dump(result, f)

def crawler():
	while 1:
		try:
			url = queue.get(timeout=1)
			parse(url)
		except gevent.queue.Empty:
			break
		except:
			print url

if __name__ == "__main__":
	from gevent.queue import Queue
	from gevent.pool import Pool
	queue = Queue()
	pool = Pool(5)
	count = 0
	for item in glob.iglob(DATA_PATH):
		with open(item, 'r') as f:
			json_data = json.load(f)
			for item in json_data:
				index_link = item.get('index_link')
				queue.put(index_link)
				count += 1
	print 'count', count
	for i in xrange(5):
		pool.spawn(crawler())
	pool.join()
