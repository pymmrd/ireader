# -*- coding:utf-8 -*-

from book.utils import category_feature_books, category_books, category_hot_books, get_book_chapters, get_bookitem, process_index_items

def handler_index(page=1):
	(feature_list, magic_books,
		sord_books, dushi_books,
		lover_books, time_travel_books,
		game_books, mnst_books,
		scnc_books, other_books, 
		result_list, paginator, 
		page, hot_books) = process_index_items(page=1)
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

def handler_show_content(pk):
	book, object_list, partition, recom_list = get_book_chapters(pk)
	return book, object_list, partition, recom_list

def handler_show_category(pk, page=1):
	# category feature books
	feature_list = category_feature_books(pk)
	# category books
	object_list, paginator, page, name = category_books(pk, page)
	# hot books 
	hot_list = category_hot_books(pk)
	return feature_list, object_list, hot_list, paginator, name

def handler_show_detail(partition, pk):
	(item,
		has_next, 
		has_previous, 
		next_to, 
		previous_to,
		recom_list) = get_bookitem(partition, pk)
	return item, has_next, has_previous, next_to, previous_to

def handler_search(keyword, page):
	result_list, paginator, page = get_search_result(keyword, page)
	return result_list, paginator, page
	
