# -*- coding:utf-8 -*-

import os
import sys
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

def print_miss():
	book = Book.objects.values_list('id', flat=True).all()
	for b in book:
		cls = get_bookitem_model(b)
		count = cls.objects.filter(book__id=b).count()
		if count == 0:
			print b

if __name__ == "__main__":
	print_miss()


