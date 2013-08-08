# -*- coding:utf-8 -*-

import os
import sys
import json
import glob
import threadpool
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/data/*.json"

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

CATEGORY_MAP = {
    'magic': 1,
    'sord': 2,
    'dushi': 3,
    'lover': 4,
    'time_travel': 5,
    'game': 6,
    'monster': 7,
    'science': 8,
    'other': 9,
}

#CATEGORY_LIST = list(Category.objects.all().order_by('id')) 
CATEGORY_LIST = [Category.objects.get(pk=pk) for pk in xrange(1,10)] 

def load_json(data_path):
    print 'data_path------->', data_path
    file_name = data_path.rsplit('/', 1)[0] 
    prefix_name = file_name.rsplit('_', 1)[0]
    try:
        index = CATEGORY_MAP.get('magic')
    except KeyError:
        print 'error:', data_path
    else:
        category = CATEGORY_LIST[index-1] 
        with open(data_path, 'r') as f:
            try:
                data = json.load(f)
            except:
                print 'error:', data_path
            else:
                for item in data:
                    update_date = datetime.strptime(item.get('update_date'), '%Y-%m-%d')
                    index_link = item.get('index_link')
                    word_num = item.get('word_num')
                    author = item.get('author')
                    name = item.get('name')[:-4]

if __name__ == "__main__":
    from django.db import connection
    for item in glob.iglob(DATA_PATTERN):
        load_json(item)
    #pool = threadpool.ThreadPool(10)
    #requests = threadpool.makeRequests(load_json, glob.glob(DATA_PATTERN))
    #for req in requests:
    #    pool.putRequest(req)
    #pool.wait()
    import pprint
    pprint.pprint(connection.queries)
