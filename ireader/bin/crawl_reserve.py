# -*- coding:utf-8 -*-

import os
import re
import time
import sys
import threadpool
from datetime import datetime
from lxml import html

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

def get_book():
	for name in os.listdir(BOOK_PATH):
		path = os.path.join(BOOK_PATH, name)
		crawled =  
		book = Book.objects.get(name=name)
		pk = book.pk
		cls = get_bookitem_model(pk)
		items = cls.objects.values_list('content', flat=True).filter(book__id=pk).order_by('pk')
		raws = map(lambda x : x.rsplit('/', 1)[-1], items)

if __name__ == '__main__':
	get_book()
