# -*- coding:utf-8 -*-

#import gevent.monkey
#gevent.monkey.patch_all()
import os
import os
import re
import sys
import json
import time
import random
import urllib2
import urlparse
import linecache

from lxml import html
from hashlib import md5

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category
from book.klass import get_bookitem_model

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

adict = {}
with open('full.json', 'r') as j:
    adict = json.load(j)

@coroutine
def get_content(parse_target):
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
    ]

    while True:
        content = ''
        headers = {'User-Agent':random.choice(user_agents)}
        title, url, pk = (yield )
        req = urllib2.Request(url=url, headers=headers)
        try:
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            if e.code == 503 : 
                time.sleep(30)
                content = tryAgain(req, 0)
        except :
            time.sleep(30)
            content = tryAgain(req, 0)
        if content:
            parse_target.send((title, pk, url, content))
        else:
            with open('miss3.txt', 'a') as f:
                f.write('%s%s' % (url, os.linesep))

def tryAgain(url, retries=0):
    content = ''
    if retries < 4:
        try:
            time.sleep(30)
            content = urllib2.urlopen(req).read()
        except :
            retries += 1
            content = tryAgain(url, retries)
    return content

@coroutine
def parse_detail(save_target):
    while True:
        title, pk, url, content = (yield )
        dom = html.fromstring(content)
        ct = dom.xpath("//div[@id='content']")[0]
        ct_str = html.tostring(ct, encoding='utf-8')
        #regx = re.compile('<div\sid="content">(?P<detail>.+)</div>')
        regx = re.compile('<div.+?>')
        detail = regx.sub('', ct_str)
        #detail = regx.match(ct_str)
        if detail is not None:
            detail = detail.replace('</div>', '')
            #detail = detail.group('detail')
            save_target.send((title, pk, detail))
        else:
            with open('miss.txt', 'a') as f:
                f.write('%s%s' % (url, os.linesep))

@coroutine
def save_detail():
    while True:
        title, pk, detail = (yield )
        sub_path = os.path.join(BOOK_PATH, title)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
        book_url = '%s/%s' % (title, pk) 
        book_path = os.path.join(sub_path, str(pk))
        with open(book_path, 'w') as f:
            print book_path
            f.write(detail)

def get_book(start, end, filename, task_target):
    """
    target is 'get_task'
    """
    names = (linecache.getline(filename, n) for n in range(start, end+1))
    for name in names:
        name = name.strip()
        path = os.path.join(BOOK_PATH, name)
        crawled = set(os.listdir(path))
        book = Book.objects.get(name=name)
        pk = book.pk
        cls = get_bookitem_model(pk)
        items = cls.objects.values_list('content', flat=True).filter(book__id=pk).order_by('pk')
        raws = set(map(lambda x : x.rsplit('/', 1)[-1], items))
        reserved = raws.difference(crawled)
        if reserved:
            task_target.send((book.name, book.author, reserved))

@coroutine
def get_task(content_target):
    while True:
        name, author, reserved = (yield )
        s = '%s%s' % (name, author) 
        key = md5(s.encode('utf-8')).hexdigest()
        prefix = adict.get(key)
        for pk in reserved:
            suffix = '%s.html' % pk  
            url = urlparse.urljoin(prefix, suffix) 
            print 'url--->', url
            content_target.send((name, url, pk))

if __name__ == "__main__":
    import sys
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    filename = sys.argv[3]
    pk = sys.argv[4] 
    BOOK_PATH = '/home/zg163/data/book%s' % pk
    get_book(start, end, filename, get_task(get_content(parse_detail(save_detail()))))
