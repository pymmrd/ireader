# -*- coding:utf-8 -*-

import os
import sys
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
DATA_PATTERN = "/var/www/wwwroot/ireader/pybook/detail/%s.json"

def print_miss():
        book = Book.objects.values('id', 'name')
        for b in book:
            pk = b['id']
            part = pk % 10
            filename = '%s.part' % part 
            cls = get_bookitem_model(pk)
            count = cls.objects.filter(book__id=pk).count()
            if count == 0:
                name = b['name']
                path = DATA_PATTERN %  name
                if os.path.exists(path):
                    with open(filename, 'a') as f:
                        f.write('%s\n'% name.decode('utf-8'))
                else:
                    with open('lost.txt', 'a') as f1:
                        f1.write('%s\n'% name.encode('utf-8'))

if __name__ == "__main__":
    print_miss()


