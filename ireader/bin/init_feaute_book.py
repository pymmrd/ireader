# -*- coding:utf-8 -*-

import os
import sys
import time
import random
import threadpool

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, FeatureBook

CATEGORY_FEATURE_NUM = 6
INDEX_FEATURE_NUM = 6
INDEX_CATEGORY_NUM = 13

def feature_book():
	page = 0
	FeatureBook.objects.filter(page=page).delete()
	exclude = FeatureBook.objects.values_list('book__id', flat=True).all()
	books = Book.objects.values_list('id', flat=True).exclude(id__in=exclude) 
	books = random.sample(books, INDEX_FEATURE_NUM)
	gen_feature_books(books, page)

def gen_feature_books(ids, page):
	books = Book.objects.filter(id__in=ids)
	for b in books:
		fbook = FeatureBook()
		fbook.book = b
		fbook.page = page
		fbook.save()

def init_feature(pk):
	#delete old recommand 
	FeatureBook.objects.filter(page=pk).delete()
	# init category page
	books = Book.objects.values_list(
			   'id', flat=True
		   ).filter(category__id=pk)
	cat_features = random.sample(books, CATEGORY_FEATURE_NUM)
	gen_feature_books(cat_features, pk)
	# init index page
	index_pk = pk + 9
	FeatureBook.objects.filter(page=index_pk).delete()
	new_books = books.exclude(id__in=cat_features)
	index_features = random.sample(new_books, INDEX_CATEGORY_NUM)
	gen_feature_books(index_features, index_pk)

def init():
	pool = threadpool.ThreadPool(5)
	requests = threadpool.makeRequests(init_feature, xrange(1, 10))
	for req in requests:
		pool.putRequest(req)
	pool.wait()
	feature_book()

if __name__ == "__main__":
	init()
	

