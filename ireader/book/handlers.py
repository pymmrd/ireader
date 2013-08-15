# -*- coding:utf-8 -*-

from book.utils import category_feature_books, category_books, category_hot_books 


def handler_index():
	pass

def handler_show_content():
	pass

def handler_show_detail():
	pass

def handler_show_category(pk, page=1):
	# category feature books
	feature_list = category_feature_books(pk)
	# category books
	object_list, paginator, page = category_books(pk, page)
	# hot books 
	hot_list = category_hot_books(pk)
	return feature_list, object_list, hot_list
