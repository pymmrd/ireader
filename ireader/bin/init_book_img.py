# -*- coding:utf-8 -*-

import os
import sys
import json
from hashlib import md5

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

def get_img_status():
	with open('img.json', 'r') as f:
		data = json.load(f)
	books  = Book.objects.all()
	for book in books:
		key = md5('%s%s' % (book.name.encode('utf-8'), book.author.encode('utf-8'))).hexdigest()
		img, status = data.get('key', ('', 2))
		status = int(status)
		book.cover = img
		book.status = status
		book.save()
	

if __name__ == "__main__":
	get_img_status()
			
