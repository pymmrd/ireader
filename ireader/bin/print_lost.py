# -*- coding:utf-8 -*-

import os
import sys
import json
import urlparse
from hashlib import md5
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

adict = {}
with open('full.json', 'r') as j:
    adict = json.load(j)

def print_lost():
    dir1 = '/mnt/data1/book'
    dir2 = '/data'
    book = Book.objects.all()
    f = open('lost_url.log', 'a')
    for b in book:
        cls = get_bookitem_model(b.pk)
        s = '%s%s' % (b.name.encode('utf-8'), b.author.encode('utf-8')) 
        key = md5(s).hexdigest()
        prefix = adict.get(key)
        items = cls.objects.filter(book__id=b.pk)
        for item in items:
            content = item.content
            path1 = os.path.join(dir1, content)
            path2 = os.path.join(dir2, content)
            if not os.path.exists(path1) and  not os.path.exists(path2): 
                sub, name, pk = content.split('/') 
                suffix  = '%s.html' % pk
                url = urlparse.urljoin(prefix, suffix)
                f.write('%s\t%s\t%s\n' % ( name.encode('utf-8'), sub.encode('utf-8'), url.encode("utf-8")))
    f.close()
                
                
            

if __name__ == "__main__":
    print_lost()


