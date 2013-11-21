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
from django.db.models import Q

CATEGORY_FEATURE_NUM = 8
INDEX_FEATURE_NUM = 6
INDEX_CATEGORY_NUM = 13

def feature_book():
	page = 0
	FeatureBook.objects.filter(page=page).delete()
	exclude = FeatureBook.objects.values_list('book__id', flat=True).all()
	books = Book.objects.values('id', 'cover').exclude(Q(id__in=exclude)|Q(intro='')) 
	object_list = get_img_object(books)
	books = random.sample(object_list, INDEX_FEATURE_NUM)
	gen_feature_books(books, page)

def gen_feature_books(ids, page):
	books = Book.objects.filter(id__in=ids)
	for b in books:
		fbook = FeatureBook()
		fbook.id = b.id
		fbook.book = b
		fbook.page = page
		fbook.save()
	
def get_img_object(books):
	object_list = []
	for book in books:
		cover = book.get("cover" ,'')
		if cover:
			pk = book.get('id')
			object_list.append(pk)
	return object_list
	

def init_feature(pk):
	#delete old recommand 
	FeatureBook.objects.filter(page=pk).delete()
	# init category page
	books = Book.objects.values('id', 'cover'
		   ).filter(category__id=pk).exclude(Q(intro=''))
	object_list = get_img_object(books)
	cat_features = random.sample(object_list, CATEGORY_FEATURE_NUM)
	gen_feature_books(cat_features, pk)
	# init index page
	index_pk = pk + 9
	FeatureBook.objects.filter(page=index_pk).delete()
	new_books = books.exclude(id__in=cat_features)
	object_list = get_img_object(new_books)
	index_features = random.sample(object_list, INDEX_CATEGORY_NUM)
	gen_feature_books(index_features, index_pk)

def init_hot_book(i):
	FeatureBook.objects.filter(page=i).delete()
	cat = i % 100
	init_ids = list(FeatureBook.objects.values_list('id', flat=True))
	books = Book.objects.values_list('id', flat=True).exclude(id__in=init_ids)
	if cat:
		books = list(books.filter(category__id=cat))
	new_books = random.sample(books, 25)
	gen_feature_books(new_books, i)


def get_hot_book():
	for i in xrange(100, 110):
		init_hot_book(i)


def init():
	for i in xrange(1, 10):
		init_feature(i)
	"""
	pool = threadpool.ThreadPool(5)
	requests = threadpool.makeRequests(init_feature, xrange(1, 10))
	for req in requests:
		pool.putRequest(req)
	pool.wait()
	"""
	feature_book()

if __name__ == "__main__":
    init()
    get_hot_book()


