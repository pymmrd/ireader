# -*- coding:utf-8 -*-
from django.core.paginator import Paginator,\
                            InvalidPage, EmptyPage

def paginate_util(obj_list, page, page_size):
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1 
    #generate the paginator object
    paginator = Paginator(obj_list, page_size)
    try:
        result_list  = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        result_list = paginator.page(1).object_list
    return result_list, paginator, page
