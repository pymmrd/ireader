# -*- coding:utf-8 -*-

import os
import re
import sys
import time
import string
import random

brand = u'全本小说'
repl1 = u'40亿小说'
regx1 = re.compile(r'[wW]{3}.[qQuUaAbBeEnN]{7}.[cCoOmM]{3}')
regx2 = re.compile(r'%s' % brand)

def get_random_domain():
	ww = 'wW' * 10
	www = ''.join(random.sample(ww, 3))
	name = '%s%s%s' % ('40', random.choice(['y', 'Y']), random.choice(['e', 'E']))
	com = '%s%s%s' % ( random.choice(['c', 'C']), random.choice(['o', 'O']), random.choice(['m', 'M']))
	sep = random.choice(string.punctuation.replace('\\', ''))
	domain = '%s%s%s%s%s' % (www, sep, name, sep, com) 
	return domain

def replace_logo(path):
	for p, d, f in os.walk(path):
		if not d:
			file_path = os.path.join(p, f)
			file_path = file_path.encode('utf-8')
			with open(file_path, 'r+') as f:
				content = f.read()
				content = content.decode('utf-8')
				domain  = get_random_domain()
				content = regx1.sub(domain, content)
				content = regx2.sub(repl1, content)
				f.seek(0)
				f.write(content)

def preview_check(path):
	for d in os.listdir(path):
		book_path = os.path.join(path, d)
		files = os.listdir(book_path)
		if files:
			filename = files[0]
			file_path = os.path.join(book_path, filename)
			with open(file_path, 'r+') as f:
				content = f.read()
				content = content.decode('utf-8')
				domain  = get_random_domain()
				try:
					content = regx1.sub(domain, content)
					content = regx2.sub(repl1, content)
				except:
					print file_path
				time.sleep(1)

if __name__ == "__main__":
	import sys
	path = sys.argv[1]
	replace_logo(path)
	#path = '/home/zg163/data/book1'
	#preview_check(path)
				
