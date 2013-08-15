# -*- coding:utf-8 -*-

#from py
import random

#from project
from django.conf import settings
from commons.paginate import paginate_util
from book.models import Book, BookPart, Category, FeatureBook

def category_feature_books(pk):
	values = (	'book__name', 'book__cover', 
				'book__id', 'book__intro', 
				'book__author',)
	feature_list = FeatureBook.objects.values(*values).filter(pk=pk)
	return feature_list

def category_books(pk, page=1):
	page_size = settings.CATEGORY_BOOKS_PER_PAGE
	values = ('id',  'name', 'update_date', 'author', 'status')
	object_list = Book.objects.values(*values).filter(
							category__pk=pk,
				  )
	result_list, paginator, page = paginate_util(object_list,
												 page,
												 page_size
												 )
	return result_list, paginator, page

def category_hot_books(pk):
	values = ('id', 'name', 'author')
	page_size = settings.CATEGORY_BOOKS_PER_PAGE
	object_list = Book.objects.values_list('id', 
						flat=True).filter(category__pk=pk)
	object_ids = randomn.choice(object_list, page_size) 
	object_list = Book.objects.values(*values).filter(pk__in=object_ids)
	return object_list
