# -*- coding:utf-8 -*-

#import gevent.monkey
#gevent.monkey.patch_all()
import os
import re
import time
import json
import sys
import glob
import random
import urllib
import urllib2
from hashlib import md5
from lxml import html

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/new_data/%s*"
DEST_PATH = '/home/zg163/data/images/'

if not  os.path.exists(DEST_PATH):
	os.makedirs(DEST_PATH)

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

#URL = "http://search.17k.com/search.xhtml?c.st=0&c.q=%s"
URL = "http://www.geiliwx.com/Book/Search.aspx"

def get_content(url, data=None):
	content = ''
	user_agents = [
		'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
		'Opera/9.25 (Windows NT 5.1; U; en)',
		"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
	]
	headers = {'User-Agent':random.choice(user_agents)}
	req = urllib2.Request(url=url, headers=headers, data=data)
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

def get_name_author(pat):
	pattern = DATA_PATTERN % (pat)
	for i in glob.iglob(pattern):
		with open(i, 'r') as f:
			try:
				data = json.load(f)
			except:
				pass
			else:
				for item  in data:
					author = item.get('author')
					name = item.get('name')[:-4]
					yield (name, author)

def send_search_request(pat):
	data = {}
	data['SearchClass'] = 1
	data['SeaButton.x'] = 39
	data['SeaButton.y'] = 10
	prefix = "http://www.geiliwx.com"
	for name, author in get_name_author(pat):
		data['SearchKey'] = name.encode('gbk')
		param = urllib.urlencode(data)
		content = get_content(URL, param)
		try:
			if content:
				content = content.decode('gbk')
				dom = html.fromstring(content)
				uls = dom.xpath("//div[@class='rights']/div[@class='block']/div[@class='blockcontent']/ul")
				for ul in uls:
					li = ul.xpath("child::li[1]")[0]
					book_link = li.xpath("child::a[1]")[0]
					link = "%s%s" % ( prefix, book_link.attrib.get('href')) 
					book_name = book_link.text_content()
					book_author = li.xpath("child::a[2]")[0].text_content()
					if book_name == name and book_author == author:
						yield (name, link, author)
		except:
			pass

def save_image(url, key, sub_dir='img1'):
	default_ext = '.ext'
	p, filename = url.rsplit('/', 1)
	name, ext = os.path.splitext(filename)
	ext = ext if ext else default_ext 
	filename = '%s%s' % (key, ext) 
	content = get_content(url)
	sub_path = os.path.join(DEST_PATH, sub_dir)
	if not os.path.exists(sub_path):
		os.makedirs(sub_path)
	file_path = os.path.join(sub_path, filename)
	with open(file_path, 'w') as f:
		f.write(content)
	return '%s/%s' % ( sub_dir, filename)

def crawl_image(pat):
	prefix = "http://www.geiliwx.com"
	for name, link, author in send_search_request(pat):
		try:
			content = get_content(link)
			if content:
				raw = '%s%s' % ( name, author)
				raw = raw.encode('utf-8')
				key = md5(raw).hexdigest() 
				content = content.decode('gbk')
				dom = html.fromstring(content)
				#img = dom.xpath("//div[@class='bookimg']/img")[0]
				img = dom.xpath("//div[@class='ClBookText']/div[1]/img[1]")[0]
				url = "%s%s" % (prefix, img.attrib.get('src'))
				img_path = save_image(url, key)
				stat_block = dom.xpath("//div[@class='ClBookText']/div[2]")[0]
				cls, fl = stat_block.attrib.get('class', '').split(' ')
				status = 2
				if cls == 'booktexts':
					status = 1 
				with open('img.txt', 'a') as f:
					print >>f, '%s\t%s\t%s\t%s' % (name.encode('utf-8'), author.encode('utf-8'), img_path, status)
		except:
			pass

if __name__ == "__main__":
	import sys
	pat = sys.argv[1]
	crawl_image(pat)
	
						
