# -*- coding:utf-8 -*-

#from py
import os
import random
import bisect

#from project
from django.conf import settings
from commons.paginate import paginate_util
from book import models
from book.models import Book, BookPart, Category, FeatureBook
from book.klass import get_bookitem_model 

def category_feature_books(pk):
	values = (	'book__name', 'book__cover', 
				'book__id', 'book__intro', 
				'book__author',
	)
	feature_list = FeatureBook.objects.values(*values).filter(page=pk)
	return feature_list

def category_books(pk, page=1):
	page_size = settings.CATEGORY_BOOKS_PER_PAGE
	values = ('id',  'name', 'update_date', 'author', 'status')
	object_list = Book.objects.values(
				      *values
				  ).filter(
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
	object_list = Book.objects.values_list(
					  'id', flat=True
				  ).filter(category__pk=pk)
	object_ids = random.sample(object_list, page_size) 
	object_list = Book.objects.values(*values).filter(pk__in=object_ids)
	return object_list

def get_single_book(pk):
	values = (	'id', 'name', 
				'author', 'category__name',
				'category__pk', 'status', 
				'cover', 'update_date',
				'has_part',
	)
	book = Book.objects.values(*values).get(pk=pk)
	return book

def get_book_chapters(pk):
	object_list = []
	values = ('id', 'name')
	book = get_single_book(pk)
	has_part = book.get('has_part', False)
	partition = pk % settings.BOOKITEM_PARTITION
	itemcls = get_bookitem_model(pk) 
	if has_part:
		bookparts = BookPart.objects.filter(
						book__id=pk
					).order_by('pk')
		for bp in bookparts:
			chapters = itemcls.objects.values(
						   *values
					   ).filter(
							part__id=bp.pk
					   ).order_by('pk')
			object_list.append({bp.name: chapters})
	else:
		chapters = itemcls.objects.values(*values).filter(book__id=pk)
		object_list.append({'A': chapters})
	return book, object_list, partition

def get_next_and_previous(cls, book_id, pk):
	next_to = None
	previous_to = None
	has_next = False
	has_previous = False
	chapters = list(cls.objects.values_list(
						'id', flat=True
					).filter(
						book__id=book_id
					).order_by('id')
				)
	length = len(chapters)
	minus_len = length - 1
	index = bisect.bisect_left(chapters, pk) 
	if 0 < index < minus_len:
		has_next = True
		has_previous = True
	elif index == minus_len and length >= 2 :
		has_previous = True
	elif index == 0 and length >= 2:
		has_next = True
	if has_next:
		next_to = pk + 1
	if has_previous:
		previous_to = pk - 1
	return has_next, has_previous, next_to, previous_to

def get_bookitem(partition, pk):
	values = (
			  'name',
			  'content', 
			  'book__id', 
			  'book__name', 
			  'book__category__name', 
			  'book__category__id', 
	)
	base = models.BookItem
	name = '%s%s' % (base.__name__, partition)
	itemcls = getattr(models, name)
	item = itemcls.objects.values(*values).get(pk=pk)
	book_id = item.get('book__id', '')
	(has_next, 
		has_previous, 
		next_to, 
		previous_to) = get_next_and_previous(itemcls, book_id, pk)
	return item, has_next, has_previous, next_to, previous_to

def get_index_feature_books(page):
	values = ('book__name', 'book__intro', 'book__author', 'book__cover', 'book__id')
	return FeatureBook.objects.values(*values).filter(page=page).order_by('pk')

def process_index_items():
	#index feature
	feature_list = get_index_feature_books(FeatureBook.INDEX)
	magic_books = get_index_feature_books(FeatureBook.MAGIC)
	sord_books = get_index_feature_books(FeatureBook.SORD)
	dushi_books = get_index_feature_books(FeatureBook.DUSHI)
	lover_books = get_index_feature_books(FeatureBook.LOVER)
	time_travel_books = get_index_feature_books(FeatureBook.TIME_TRAVEL)
	game_books = get_index_feature_books(FeatureBook.GAME)
	mnst_books = get_index_feature_books(FeatureBook.MONSTER)
	scnc_books = get_index_feature_books(FeatureBook.SCIENCE)
	books = Book.objects.values(*values).all().order_by('-update_date')
	result_list, paginator, page = paginate_util(books,
												 page,
												 page_size
												 )
	return result_list, paginator, page
