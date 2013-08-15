# -*- coding:utf-8 -*-

#from py
import random

#from project
from django.conf import settings
from commons.paginate import paginate_util
from book.models import Book, BookPart, Category, FeatureBook
from book.klass import get_bookitem_model 

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
	page_size = settings.CATEGORY_BOOKS_PER_PAGE + 1
	object_list = Book.objects.values_list('id', 
						flat=True).filter(category__pk=pk)
	object_ids = random.sample(object_list, page_size) 
	object_list = Book.objects.values(*values).filter(pk__in=object_ids)
	return object_list

def get_single_book(pk):
	values = ('id', 'name', 'author', 'category__name',
			   'category__pk', 'status', 'cover',
			   'update_date','has_part',
	)
	book = Book.objects.values(*values).get(pk=pk)
	return book

def get_book_chapters(pk):
	object_list = []
	values = ('id', 'name')
	book = get_single_book(pk)
	has_part = book.get('has_part', False)
	itemcls = get_bookitem_model(pk) 
	if has_part:
		bookparts = BookPart.objects.filter(book__id=pk).order_by('pk')
		for bp in bookparts:
			chapters = itemcls.objects.values(*values).filter(part__id=bp.pk).order_by('pk')
			object_list.append({bp.name: chapters})
	else:
		chapters = itemcls.objects.values(*values).filter(book__id=pk)
		object_list.append({'A': chapters})
	print object_list
	return book, object_list
