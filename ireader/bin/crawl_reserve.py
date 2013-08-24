# -*- coding:utf-8 -*-

import gevent.monkey
gevent.monkey.patch_all()
import os
import os
import re
import sys
import json
import time
import urllib2
import urlparse
import random

from lxml import html
from hashlib import md5
from gevent.queue import Queue, Empty
from gevent.pool import Pool

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
BOOK_PATH = '/home/zg163/data/book1'
DEST_PATH = '/home/zg163/data/book2'

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

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

def get_detail(url):
	detail = ''
	content = ''
	try:
		content = get_content(url)
	except:
		with open('miss.txt', 'a') as f:
			f.write('%s%s' % (url, os.linesep))
	if content:
		dom = html.fromstring(content)
		ct = dom.xpath("//div[@id='content']")[0]
		ct_str = html.tostring(ct, encoding='utf-8')
		regx = re.compile('<div\sid="content">(?P<detail>.+)</div>')
		detail = regx.match(ct_str).group('detail')
	return detail

def save_detail(title, url, pk):
	detail = get_detail(url)
	book_dir = u'%s/%s' % ('book', title)
	sub_path = os.path.join(DEST_PATH, book_dir)
	if not os.path.exists(sub_path):
		os.makedirs(sub_path)
	book_url = '%s/%s' % (title, pk) 
	book_path = os.path.join(sub_path, str(pk))
	with open(book_path, 'w') as f:
		f.write(detail)

def get_book():
	for name in os.listdir(BOOK_PATH):
		path = os.path.join(BOOK_PATH, name)
		crawled = set(os.listdir(path))
		book = Book.objects.get(name=name)
		pk = book.pk
		cls = get_bookitem_model(pk)
		items = cls.objects.values_list('content', flat=True).filter(book__id=pk).order_by('pk')
		raws = set(map(lambda x : x.rsplit('/', 1)[-1], items))
		reserved = raws.difference(crawled)
		if reserved:
			s = '%s%s' % (book.name, book.author) 
			key = md5(s.encode('utf-8')).hexdigest()
			yield (book.name, book.author, reserved)

def get_task():
	adict = {}
	queue = Queue()
	with open('full.json', 'r') as f:
		adict = json.load(f)
	for name, author,  reserved in get_book():
		s = '%s%s' % (name, author) 
		key = md5(s.encode('utf-8')).hexdigest()
		prefix = adict.get(key)
		for pk in reserved:
			suffix = '%s.html' % pk  
			url = urlparse.urljoin(prefix, suffix) 
			queue.put((name, url, pk))
	return queue

def worker():
	queue = get_task()
	while True:
		try:
			name, url, pk = queue.get(timeout=1) 
		except Empty:
			break
		else:
			save_detail(name, url, pk)

if __name__ == "__main__":
	pool = Pool(7)
	for x in range(7):
		pool.spawn(worker())
	pool.join()
