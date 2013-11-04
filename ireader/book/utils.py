# -*- coding:utf-8 -*-

#from py
import os
import random
import bisect

#from django
from django.conf import settings
from django.db.models import Q

#from project
from commons.paginate import paginate_util
from book import models
from book.models import Book, BookPart, Category, FeatureBook
from book.klass import get_bookitem_model 

CATEGORY_NAME = {
	1: u'玄幻',
	2: u'武侠',
	3: u'都市',
	4: u'言情',
	5: u'穿越',
	6: u'网游',
	7: u'惊恐',
	8: u'科幻',
	9: u'其它'
}

def category_feature_books(pk):
	values = (	'book__name', 'book__cover', 
				'book__id', 'book__intro', 
				'book__author',
	)
	feature_list = FeatureBook.objects.values(*values).filter(page=pk)
	return feature_list

def category_books(pk, page=1):
	name = CATEGORY_NAME.get(pk, u'玄幻') 
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
	return result_list, paginator, page, name

"""
def category_hot_books(pk=None):
	object_list = []
	values = ('id', 'name', 'author')
	page_size = settings.CATEGORY_BOOKS_PER_PAGE + 1
	book_list = Book.objects.values_list(
					  'id', flat=True
				  )
	if pk:
		book_list = book_list.filter(category__pk=pk)
	count = book_list.count()
	if count:
		page_size = page_size if count > page_size else count
		book_ids = random.sample(book_list, page_size) 
		object_list = Book.objects.values(*values).filter(pk__in=book_ids)
	return object_list
"""
def category_hot_books(page):
	object_list = FeatureBook.objects.values('id', 'book__name', 'book__author').filter(page=page)
	return object_list

def get_single_book(pk):
	values = (	'id', 'name', 
				'author', 'category__name',
				'category__pk', 'status', 
				'cover', 'update_date',
				'has_part', 'word_num',
				'intro',
	)
	book = Book.objects.values(*values).get(pk=pk)
	return book

def get_recommand_books(object_id):
	page_size = 14
	values = ('id', 'name', 'status')
	book_list = Book.objects.values_list('id', flat=True).exclude(pk=object_id)
	book_ids = random.sample(book_list, page_size) 
	object_list = Book.objects.values(*values).filter(pk__in=book_ids)
	return object_list

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
		chapters = itemcls.objects.values(*values).filter(book__id=pk).order_by('pk')
		object_list.append({'A': chapters})
	recom_list = get_recommand_books(pk)
	return book, object_list, partition, recom_list

def get_next_and_previous(cls, book_id, pk):
	next_to = None
	previous_to = None
	has_next = False
	has_previous = False
	previous = cls.objects.values_list('id', flat=True).filter(book__pk=book_id, pk__lt=pk).order_by('-pk')
	nexts = cls.objects.values_list('id', flat=True).filter(book__pk=book_id, pk__gt=pk).order_by('pk')
	if previous:
		has_previous = True
		previous_to = previous[0]
	if nexts:
		has_next = True
		next_to = nexts[0]
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
	book = get_single_book(book_id)
	recom_list = get_recommand_books(book_id)
	(has_next, 
		has_previous, 
		next_to, 
		previous_to) = get_next_and_previous(itemcls, book_id, pk)
	return item, has_next, has_previous, next_to, previous_to, recom_list, book

def get_index_feature_books(page):
	values = ('book__name', 'book__intro', 'book__author', 'book__cover', 'book__id')
	return FeatureBook.objects.values(*values).filter(page=page).order_by('pk')

def process_index_items(page=1):
	page_size = 24
	values = ('id',  'name', 'update_date', 'author', 'status', 'category__name', 'category__id')
	#index feature
	feature_list = get_index_feature_books(FeatureBook.INDEX)
	magic_books = get_index_feature_books(FeatureBook.INDEX_MAGIC)
	sord_books = get_index_feature_books(FeatureBook.INDEX_SORD)
	dushi_books = get_index_feature_books(FeatureBook.INDEX_DUSHI)
	lover_books = get_index_feature_books(FeatureBook.INDEX_LOVER)
	time_travel_books = get_index_feature_books(FeatureBook.INDEX_TIME_TRAVEL)
	game_books = get_index_feature_books(FeatureBook.INDEX_GAME)
	mnst_books = get_index_feature_books(FeatureBook.INDEX_MONSTER)
	scnc_books = get_index_feature_books(FeatureBook.INDEX_SCIENCE)
	other_books = get_index_feature_books(FeatureBook.INDEX_OTHER)
	books = Book.objects.values(*values).all().order_by('-update_date')
	hot_books = category_hot_books()
	result_list, paginator, page = paginate_util(books,
												 page,
												 page_size
												 )
	return (feature_list, 
			magic_books,
			sord_books,
			dushi_books,
			lover_books,
			time_travel_books,
			game_books,
			mnst_books,
			scnc_books,
			other_books,
			result_list, 
			paginator, 
			page,
			hot_books,
			)

def get_search_result(keyword, page):
	page_size = settings.SEARCH_PER_PAGE
	object_list = Book.objects.filter(Q(name__icontains=keyword)|Q(author__icontains=keyword))
	result_list, paginator, page = paginate_util(object_list,
												 page,
												 page_size
												 )
	return result_list, paginator, page
