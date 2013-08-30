# -*- coding:utf-8 -*-

import os
import re
import time
import sys
import urllib2
import threadpool
from hashlib import md5
from lxml import html

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/detail/*.json"

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

URL = "http://search.17k.com/search.xhtml?c.st=0&c.q=%s"

def get_content(url):
	content = ''
	user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
		'Opera/9.25 (Windows NT 5.1; U; en)',
		"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
	]
	headers = {'User-Agent':random.choice(user_agents)}
	req = urllib2.Request(url=url, headers=headers,)
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

def get_name_author():
	for i in glob.iglob(DATA_PATTERN):
		with open(i, 'r') as f:
			try:
				data = json.load(f)
			except:
				pass
			else:
				for item in data:
					author = item.get('author')
					name = item.get('name')[:-4]
					index_link = item.get('index_link', '')
					raw = '%s%s' % (name, author)
					raw = raw.encode('utf-8')
					key = md5(raw).hexdigest()
					yield (name, author)

def get_name_url_author():
	for name, author get_name_author(): 
		url = URL % name
		yield (name, url, author)

def crawl_image():
	for name, url, author in get_name_author():
		content = get_content(url)
		if content:
			dom = html.fromstring(content)
			boxes = dom.xpath("//div[@class='textlist']")
			if boxes:
			for item in boxes:
				title = item.xpath("child::div[@class='textmiddle']/dl/dt/a")
				if title:
					title = title[0].text_content()
					if name != title:
						continue
					else:
						#author

						
