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

def remove():
    with open('lost.log', 'r') as f:
        for line in f:
            name = line.strip()
            book = Book.objects.get(name=name)
            book.delete()

if __name__ == "__main__":
    remove()
