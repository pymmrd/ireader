# -*- coding:utf-8 -*-

import os
import sys

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

def record(pk):
	part = pk % 10
	name = '%s.part' % part
	with open(name, 'a') as f:
		f.write('%s%s'% (pk, os.linesep))
		f.flush()

def record_partition():
	for book in Book.objects.values_list('pk', flat=True).all():
		record(book)

if __name__ == "__main__":
	record_partition()



