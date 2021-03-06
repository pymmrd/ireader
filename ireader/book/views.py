# -*- coding:utf-8 -*-
# Create your views here.

#from django
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

#from project
from book.handlers import (handler_index, handler_show_content,
                           handler_show_detail, handler_search,
                           handler_show_category)
from commons.smart_convert import convert_int

def index(request, page=1, tmpl='index.html'):
    (feature_list, magic_books, sord_books,
     dushi_books, lover_books, time_travel_books,
     game_books, mnst_books, scnc_books,
     other_books, result_list, paginator,
     page, hot_books) = handler_index(page)
    return render_to_response(tmpl,
        context_instance=RequestContext(request, {
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
    pk = convert_int(pk, exct=True)
    book, object_list, partition, recom_list= handler_show_content(pk)
    book['book__id'] = pk
    return render_to_response(tmpl, context_instance=RequestContext(request, {
        'book': book,
        'object_list': object_list,
        'partition': partition,
        'recom_list': recom_list,
    }))

def show_detail(request, partition, pk, tmpl="book/detail.html"):
    pk = convert_int(pk, exct=True)
    partition = convert_int(partition, exct=True)
    (item, has_next, has_previous,
     next_to, previous_to, recom_list,
     book) = handler_show_detail(partition, pk)
    return render_to_response(
        tmpl,
        context_instance=RequestContext(request, {
            'book': book,
            'object': item,
            'next_to': next_to,
            'has_next': has_next,
            'partition': partition,
            'recom_list': recom_list,
            'previous_to': previous_to,
            'has_previous': has_previous,
        })
    )

def show_category(request, pk, page=1, tmpl="book/category.html"):
    pk = convert_int(pk)
    page = convert_int(page)
    feature_list, object_list, hot_list, paginator, name = handler_show_category(pk, page)
    return render_to_response(
        tmpl,
        context_instance=RequestContext(request, {
            'name': name,
            'hot_list': hot_list,
            'paginator': paginator,
            'object_list': object_list,
            'feature_list': feature_list,
        })
    )

def search(request, tmpl="book/search.html"):
    result_list = []
    paginator = None
    keyword = request.GET.get('keyword', '')
    page = request.GET.get('page', 1)
    page = convert_int(page)
    if keyword:
        result_list, paginator, page = handler_search(keyword, page)
    return render_to_response(tmpl, context_instance=RequestContext(request, {
        'result_list': result_list,
        'paginator': paginator
    }))

def page_not_found(request, tmpl='404.html'):
    content = u'没有这个页面，换个URL试一试！'
    return render_to_response(tmpl, context_instance=RequestContext(request, {
        'content': content,
        }))

def server_error(request, tmpl='500.html'):
    content = u'后台出现一个小小的意外，请耐心等待！'
    return render_to_response(tmpl, context_instance=RequestContext(request, {
        'content': content,
        }))



