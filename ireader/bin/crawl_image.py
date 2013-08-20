# -*- coding:utf-8 -*-

import os
import re
import time
import sys
import threadpool
from datetime import datetime
from lxml import html

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/detail/*.json"

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book, BookItem, BookPart, Category

URL = "'http://search.17k.com/search.xhtml?c.st=0&c.q=%s"

def crawl_image():
	var boxes = dom.xpath("//div[@class=list]/div[@class=box]")

	
