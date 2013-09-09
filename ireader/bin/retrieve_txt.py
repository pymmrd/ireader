# -*- coding:utf-8 -*-

import os
import sys
import json
import glob
from hashlib import md5

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname
CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))
DATA_PATTERN = "/home/zg163/djcode/ireader/pybook/new_data/*.json"

def retrive_index():
	with open('fulltext.txt', 'a') as f1:
		for i in glob.iglob(DATA_PATTERN):
			with open(i, 'r') as f:
				try:
					data = json.load(f)
				except:
					print "jsonerror", data_path
				else:
					for item in data:
						author = item.get('author')
						name = item.get('name')[:-4]
						index_link = item.get('txt_link', '')
						#raw = '%s%s' % (name, author)
						#raw = raw.encode('utf-8')
						#key = md5(raw).hexdigest()
						f1.write('%s\t%s\t%s%s' % (name.encode('utf-8'), author.encode('utf-8'), index_link.encode('utf-8'), os.linesep))

if __name__ == "__main__":
	retrive_index()
