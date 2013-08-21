# -*- coding:utf-8 -*-
# Create your views here.

#from django
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

#from project
from book.handlers import handler_index, handler_show_content, \
						handler_show_detail, handler_show_category

def index(request, tmpl='index.html'):
	(feature_list, magic_books,
		sord_books, dushi_books,
		lover_books, time_travel_books,
		game_books, mnst_books,
		scnc_books, other_books, 
		result_list, paginator, 
		page, hot_books) = handler_index(page=1)
	return render_to_response(tmpl, context_instance=RequestContext(request, {
		'feature_list': feature_list,
		'magic_books': magic_books,
		'sord_books': sord_books,
		'dushi_books': dushi_books,
		'lover_books': lover_books,
		'time_travel_books': time_travel_books,
		'game_books': game_books,
		'mnst_books': mnst_books,
		'scnc_books': scnc_books,
		'other_books': other_books,
		'result_list': result_list,
		'paginator': paginator,
		'page': page,
		'hot_books': hot_books,
	}))

def show_content(request, pk, tmpl="book/content.html"):
	try:
		pk = int(pk)
	except (TypeError, ValueError):
		pk = 1
	book, object_list, partition = handler_show_content(pk)
	return render_to_response(tmpl, context_instance=RequestContext(request, {
		'book': book,
		'object_list': object_list,
		'partition': partition,
	}))

def show_detail(request, partition, pk, tmpl="book/detail.html"):
	try:
		partition = int(partition)
		pk = int(pk)
	except (TypeError, ValueError):
		raise Http404
	(item, 
		has_next, 
		has_previous, 
		next_to, 
		previous_to) = handler_show_detail(partition, pk)
	return render_to_response(tmpl, context_instance=RequestContext(request, {
		'object': item,
		'next_to': next_to,
		'has_next': has_next,
		'partition': partition,
		'previous_to': previous_to,
		'has_previous': has_previous,
	}))

def show_category(request, pk, tmpl="book/category.html"):
	try:
		pk = int(pk)
	except (TypeError, ValueError):
		pk = 1
	feature_list, object_list, hot_list = handler_show_category(pk, page=1)
	return render_to_response(tmpl, context_instance=RequestContext(request, {
		'hot_list': hot_list,
		'feature_list': feature_list,
		'object_list': object_list, 
	}))
