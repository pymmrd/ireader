# -*- coding:utf-8 -*-
from django import template

import urllib
register = template.Library()

DOT = '.'

def smart_page_range(pages, page_num, show_all_pages=10, on_each_side=3, on_ends=2):
    page_num = page_num -1
    if pages <= show_all_pages:
        page_range = range(pages)
    else:
        page_range = []
        if page_num > (on_each_side * on_ends):
            page_range.extend(range(0, on_each_side -1))
            page_range.append(DOT)
            page_range.extend(range(page_num - on_each_side, page_num+1))
        else:
            page_range.extend(range(0, page_num+1))
        if page_num < (pages - on_each_side - on_ends - 1):
            page_range.extend(range(page_num + 1, page_num + on_each_side + 1))
            page_range.append(DOT)
            page_range.extend(range(pages - on_ends, pages))
        else:
            page_range.extend(range(page_num + 1, pages))
    fun = lambda x : x!= DOT and x + 1 or x
    return [fun(i) for i in page_range]

@register.inclusion_tag("tags/pagination_template.html")
def paginate(request, paginator):
    path = request.path
    raw_params = request.GET.copy()
    keyword = raw_params.get('keyword', '')
    current_page = int(raw_params.get('page', u'1'))

    current_page = 1 if current_page > paginator.num_pages else current_page
    paginator_info = paginator.page(current_page)
    page_range = smart_page_range(paginator.num_pages, current_page)
    return {
        'keyword': keyword,
        'page_range': page_range,
        'current_page': current_page,
        'paginator_info': paginator_info,
    }

@register.inclusion_tag("tags/smart_paginator.html")
def smart_paginator(request, page, num_pages):
    sub_path = request.path.rsplit('/', 2)[0]
    raw_params = request.GET.copy()
    if num_pages == 1:
        page = 1
        has_other_pages = False
        has_previous = False
        has_next = False
    else:
        has_other_pages = True
        if page > num_pages:
            page = 1
            has_previous = False
            has_next = True
            next_page_number = page + 1
        elif page == num_pages:
            has_previous = True
            has_next = False
            previous_page_number = page - 1
        else:
            has_next = True
            has_previous = True
            previous_page_number = page - 1
            next_page_number = page + 1
    page_range = smart_page_range(num_pages, page)
    params = urllib.urlencode(raw_params)
    return locals()
