# -*- coding:utf-8 -*-

import os
import sys
import json
import glob
import shutil
import threadpool
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/new_data/*.json"
DEST_PATH = '/home/zg163/data/'
SRC_PATH = '/home/zg163/pdf/data/book/'

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

CATEGORY_MAP = {
    'magic': (1, 'book1'),
    'sord': (2, 'book2'),
    'dushi': (3, 'book3'),
    'lover': (4, 'book4'),
    'time_travel': (5, 'book5'),
    'game': (6, 'book6'),
    'monster': (7, 'book7'),
    'science': (8, 'book8'),
    'other': (9, 'book9'),
}

#CATEGORY_LIST = list(Category.objects.all().order_by('id')) 
CATEGORY_LIST = [Category.objects.get(pk=pk) for pk in xrange(1,10)] 

def load_json(data_path):
    #print 'data_path------->', data_path
    file_name = data_path.rsplit('/', 1)[-1] 
    prefix_name = file_name.rsplit('_', 1)[0]
    try:
        index, sub_dir = CATEGORY_MAP.get(prefix_name)
    except KeyError:
        print 'error:', data_path
    else:
        dest_path = os.path.join(DEST_PATH, sub_dir)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        category = CATEGORY_LIST[index-1] 
        with open(data_path, 'r') as f:
            try:
                data = json.load(f)
            except:
                print 'jsonerror:', data_path
            else:
                for item in data:
                    try:
                        update_date = datetime.strptime(item.get('update_date'), '%Y-%m-%d')
                    except:
                        update_date = datetime.now()
                    index_link = item.get('index_link')
                    word_num = item.get('word_num')
                    author = item.get('author')
                    name = item.get('name')[:-4]
                    book, created = Book.objects.get_or_create(name=name, author=author, defaults={'category': category, 'word_num': word_num})
                    if not created:
                        book.save()
                        src_path = os.path.join(SRC_PATH, name).encode('utf-8')
                        try:
                            shutil.move(src_path, dest_path)
                        except:
                            pass

if __name__ == "__main__":
    from django.db import connection
    for item in glob.iglob(DATA_PATTERN):
        load_json(item)
    """
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(load_json, glob.iglob(DATA_PATTERN))
    for req in requests:
        pool.putRequest(req)
    pool.wait()
    """
