# -*- coding:utf-8 -*-

import os
import time
import sys
import json
import glob
import threadpool
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/detail/*.json"

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

CATEGORY_MAP = {
    'magic': 1,
    'sord': 2,
    'dushi': 3,
    'lover': 4,
    'time_travel': 5,
    'game': 6,
    'monster': 7,
    'science': 8,
    'other': 9,
}

CATEGORY_LIST = [Category.objects.get(pk=pk) for pk in xrange(1,10)] 
BOOK_DIR = 'book1'

def get_category(data_path):
	category = None
	file_name = data_path.rsplit('/', 1)[-1] 
	prefix_name = file_name.rsplit('_', 2)[0]
	try:
		index = CATEGORY_MAP.get(prefix_name)
	except KeyError:
		print 'error:', data_path
	else:
		category = CATEGORY_LIST[index-1] 
	return category

def get_data(data_path):
	datas = []
	with open(data_path, 'r') as f:
		try:
			datas = json.load(f)
		except:
			print "jsonerror", data_path
	return datas
	
def process_has_part(content, cls, book):
	#sort value
	sort_ref = {}
	tmp_dict = {}
	result = []
	for k in content:
		if k != 'A':
			sort_value = sorted(content[k], key=lambda a:a['id']) 
			if sort_value:
				first = sort_value[0].get('id')
				sort_ref[first] = k
				tmp_dict[k] = sort_value
	keys = [sort_ref[i] for i in sorted(sort_ref.keys())]
	for k in keys:
		result.append({k: tmp_dict[k]}) 
	for elem in result:
		count = 0
		for key, value in elem.iteritems():
			if count > 0 and count % 10  == 0:
				time.sleep(0.1)
			if key != "A":
				bp = BookPart()
				bp.book = book
				bp.name = key
				bp.save()
				for item in value:
					ins = cls()
					book_url = item.get('book_url')
					ct = '%s/%s' % (BOOK_DIR, book_url)
					name = item.get('title')
					if name is None:
						name = ''
					ins.content = ct
					ins.name = name
					ins.book = book
					ins.part = bp
					ins.save()

def process_null_part(content, cls, book):
	chapters = content.get('A')
	count = 0
	for item in sorted(chapters, key=lambda a:a['id']):
		if count > 0 and count % 10 == 0:
			time.sleep(0.1)
		ins = cls()
		book_url = item.get('book_url')
		ct = '%s/%s' % (BOOK_DIR, book_url)
		name = item.get('title')
		if name is None:
			name = ''
		ins.content = ct
		ins.book = book
		ins.name = name
		ins.save()

def load_full_detail(data_path):
	has_part = False 
	item = get_data(data_path) 
	count = 0
	name = item.get('name', '')
	book = Book.objects.get(name=name)
	cls = get_bookitem_model(book.pk)
	intro = item.get('intro', '')
	book.intro = intro
	content = item.get('content', '')
	keys = content.keys()
	if len(keys) > 1:
		has_part = True
		process_has_part(content, cls, book)
	else:
		process_null_part(content, cls, book)
	book.has_part = has_part
	book.save()
	count += 1

if __name__ == "__main__":
	from django.db import connection
	for item in glob.iglob(DATA_PATTERN):
		time.sleep(2)
		load_full_detail(item)
	#import sys
	#load_full_detail(sys.argv[1])
	#pool = threadpool.ThreadPool(10)
	#requests = threadpool.makeRequests(load_json, glob.glob(DATA_PATTERN))
	#for req in requests:
	#    pool.putRequest(req)
	#pool.wait()
	#import pprint
	#pprint.pprint(connection.queries)
