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

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ireader.settings'

from book.models import Book

def init_img_status():
	with open('result.log', 'r') as f:
		for line in f:
			line = line.strip()
			param = line.split('\t')
			try:
				if len(param) == 4:
					name, author, status, cover = param 
					book = Book.objects.get(name=name, author=author)
					status = bool(int(status))
					book.status = status
					book.cover = cover
					book.save()
				elif len(param) == 3:
					name, author, status = param
					book = Book.objects.get(name=name, author=author)
					status = bool(int(status))
					book.status = status
					book.save()
				else:
					print line
			except:
				print name

if __name__ == "__main__":
	init_img_status()
