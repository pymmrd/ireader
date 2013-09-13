# -*- coding:utf-8 -*-

import os
import time
import random
import sys
import json
import glob
import threadpool
from hashlib import md5
from datetime import datetime

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/var/www/wwwroot/ireader/pybook/detail/*.json"

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

BOOK_DIR_MAP = {
    1: 'book1',
    2: 'book2',
    3: 'book3',
    4: 'book4',
    5: 'book5',
    6: 'book6',
    7: 'book7',
    8: 'book8',
    9: 'book9',
}

def get_bookdir_partition(name, author, prefix='book1', base=10):
    full = 'a'
    d = md5('%s%s' % (name.encode('utf-8'), author.encode("utf-8"))).hexdigest()
    partition = int(d[-1], 16) % base
    partition = '%s%s%s' % (prefix, full, partition) 
    return partition

def get_data(data_path):
    datas = []
    try:
        with open(data_path, 'r') as f:
            datas = json.load(f)
    except:
        print "jsonerror", data_path
    return datas
    
def process_has_part(content, cls, book, sleep):
    #sort value
    sort_ref = {}
    tmp_dict = {}
    result = []
    for k in content:
        if k != 'A':
            sort_value = sorted(content[k], key=lambda a:a['id']) 
            if sort_value:
                first = sort_value[0].get('id')
                sort_ref[first] = k
                tmp_dict[k] = sort_value
    keys = [sort_ref[i] for i in sorted(sort_ref.keys())]
    for k in keys:
        result.append({k: tmp_dict[k]}) 
    book_dir = BOOK_DIR_MAP.get(book.category.pk)
    if book_dir == 'book1':
        book_dir = get_bookdir_partition(book.name, book.author) 
    for elem in result:
        count = 0
        for key, value in elem.iteritems():
            if key != "A":
                bp = BookPart()
                bp.book = book
                bp.name = key
                bp.save()
                for item in value:
                    ins = cls()
                    book_url = item.get('book_url')
                    ct = '%s/%s' % (book_dir, book_url)
                    name = item.get('title')
                    if name is None:
                        name = ''
                    ins.content = ct
                    ins.name = name
                    ins.book = book
                    ins.part = bp
                    ins.save()
                    time.sleep(sleep)
                    count += 1

def process_null_part(content, cls, book, sleep):
    chapters = content.get('A')
    book_dir = BOOK_DIR_MAP.get(book.category.pk)
    if book_dir == 'book1':
        book_dir = get_bookdir_partition(book.name, book.author) 
    chapters = sorted(chapters, key=lambda a:a['id'])
    for item in chapters: 
        ins = cls()
        book_url = item.get('book_url')
        ct = '%s/%s' % (book_dir, book_url)
        name = item.get('title')
        if name is None:
            name = ''
        ins.content = ct
        ins.book = book
        ins.name = name
        ins.save()
        time.sleep(sleep)

def load_full_detail(data_path):
    has_part = False 
    item = get_data(data_path) 
    name = item.get('name', '')
    book = Book.objects.get(name=name)
    cls = get_bookitem_model(book.pk)
    intro = item.get('intro', '')
    book.intro = intro
    content = item.get('content', '')
    keys = content.keys()
    if len(keys) > 1:
        has_part = True
        process_has_part(content, cls, book)
    else:
        process_null_part(content, cls, book)
    book.has_part = has_part
    book.save()

def load_signle_detail(pk, sleep):
    has_part = False
    data_dir = "/var/www/wwwroot/ireader/pybook/detail/"
    #data_dir = "/home/zg163/djcode/ireader/pybook/detail/"
    book = Book.objects.get(pk=pk)
    cls = get_bookitem_model(pk)
    data_path = os.path.join(data_dir, '%s.json' % book.name.encode('utf-8'))
    item = get_data(data_path) 
    intro = item.get('intro', '')
    content = item.get('content', '')
    book.intro = intro
    keys = content.keys()
    if len(keys) > 1:
        has_part = True
        process_has_part(content, cls, book, sleep)
    else:
        process_null_part(content, cls, book, sleep)
    book.has_part = has_part
    book.save()

if __name__ == "__main__":
    import linecache
    from django.db import connection
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    pk = sys.argv[3]
    sleep = float(sys.argv[4])
    filename = '%s.part' % pk
    names = (linecache.getline(filename, n) for n in range(start, end))
    for book_id in names:
        try:
            book_id = book_id.strip()
            if book_id:
                book_id = int(book_id)
                load_signle_detail(book_id, sleep)
        except:
            with open('err.txt', 'a') as f:
                f.write('%s%s' % (book_id, os.linesep))
        
    """
    for item in glob.iglob(DATA_PATTERN):
        try:
            load_full_detail(item)
        except:
            print item
        else:
            time.sleep(3)
    """
    #import sys
    #load_full_detail(sys.argv[1])
    #pool = threadpool.ThreadPool(20)
    #requests = threadpool.makeRequests(load_full_detail, glob.iglob(DATA_PATTERN))
    #for req in requests:
    #    pool.putRequest(req)
    #pool.wait()
    #import pprint
    #pprint.pprint(connection.queries)
