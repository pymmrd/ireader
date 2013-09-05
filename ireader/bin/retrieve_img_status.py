# -*- coding:utf-8 -*-

import os
import re
import sys
import json
import random
import urllib2
from hashlib import md5
from lxml import html

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DEST_PATH = '/home/zg163/data/images/'

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

adict = {}
with open('fulltext.json', 'r') as f:
	adict = json.load(f)

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

def get_link():
	for book in Book.objects.all():
		name = book.name
		author = book.author
		raw = '%s%s' % (name, author)
		raw = raw.encode('utf-8')
		key = md5(raw).hexdigest()
		link = adict.get(key, '')
		yield (name, key, link)

def get_item(name, key, link): 
	img_path = ''
	content = get_content(link)
	dom = html.fromstring(content)
	status = dom.xpath("//div[@id='content']/table/tr[1]/td/table/tr[3]/td[2]/text()")[0]
	img = dom.xpath("//div[@id='content']/table/tr[3]/td/table/tr[1]/td[2]/a/img")[0]
	status = status.split(u'：')[-1].strip()
	if status == u'已全本':
		status = True
	img_link = img.attrib['src']
	img_name = img_link.rsplit('/', 1)[-1]
	default_name = 'nocover.jpg'
	if img_name != default_name:
		img_path = save_image(img_link, key)
	return status, img_path
	
def save_image(url, key, sub_dir='img2'):
	default_ext = '.ext'
	p, filename = url.rsplit('/', 1)
	name, ext = os.path.splitext(filename)
	ext = ext if ext else default_ext 
	filename = '%s%s' % (key, ext) 
	sub_path = os.path.join(DEST_PATH, sub_dir)
	if not os.path.exists(sub_path):
		os.makedirs(sub_path)
	file_path = os.path.join(sub_path, filename)
	if not os.path.exists(file_path):
		content = get_content(url)
		with open(file_path, 'w') as f:
			f.write(content)
	return '%s/%s' % (sub_dir, filename)

def crawl():
	bdict = {}
	for book in Book.objects.all():
		try:
			name = book.name
			author = book.author
			raw = '%s%s' % (name, author)
			raw = raw.encode('utf-8')
			key = md5(raw).hexdigest()
			link = adict.get(key, '')
			status, img_path = get_item(name, key, link)
		except:
			print link
		else:
			bdict[key] = [ status, img_path]
	with open('status.json', 'a') as f:
		json.dump(bdict, f)

if __name__ == "__main__":
	crawl()
