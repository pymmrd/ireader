# -*- coding:utf-8 -*-

import os
import sys
import glob
import simplejson
import threadpool
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

def category_init():
    category_list = [
        {'name': u'玄幻'},
        {'name': u'武侠'},
        {'name': u'都市'},
        {'name': u'言情'},
        {'name': u'穿越'},
        {'name': u'网游'},
        {'name': u'惊恐'},
        {'name': u'科幻'},
        {'name': u'其它'},
    ]
    for index, item in enumerate(category_list):
        pk = index + 1
        category = Category(pk=pk, name=item.get('name', ''))
        category.save()

if __name__ == "__main__":
    category_init()
        
