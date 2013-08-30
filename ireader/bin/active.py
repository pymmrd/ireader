# -*- coding:utf-8 -*-

import os
import os
import re
import sys
import json
import time
import random
import urllib2
import urlparse
import linecache

from lxml import html
from hashlib import md5

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
BOOK_PATH = '/home/zg163/data/book1'

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

def active_book():
	for name in os.listdir(BOOK_PATH):
		book = Book.objects.get(name=name)
		book.is_active = True
		book.save()

if __name__ == '__main__':
	active_book()

