# -*- coding:utf-8 -*-
# Create your views here.

#from django
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

#from project
from book.handlers import handler_index, handler_show_content, \
						handler_show_detail, handler_show_category

def index(request, tmpl='index.html'):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
	}))

def show_content(request, pk, tmpl="book/content.html"):
	try:
		pk = int(pk)
	except (TypeError, ValueError):
		pk = 1
	book, object_list = handler_show_content(pk)
	return render_to_response(tmpl, context_instance=RequestContext(request, {
		'book': book,
		'object_list': object_list,
	}))

def show_detail(request, pk, tmpl="book/detail.html"):
	return render_to_response(tmpl, context_instance=RequestContext(request, {
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
