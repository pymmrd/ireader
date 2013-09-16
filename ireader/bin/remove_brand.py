# -*- coding:utf-8 -*-

import os
import re
import sys
import time
import string
import random
import threadpool

brand = u'全本小说'
repl1 = u'40页小说'
regx1 = re.compile(r'[wW]{3}.[qQuUaAnNbBeEnN]{7}.[cCoOmM]{3}')
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
	print path
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

def preview_check(d):
	book_path = os.path.join(SUB_PATH, d)
	files = os.listdir(book_path)
	for filename in files: 
		domain = get_random_domain()
		file_path = os.path.join(book_path, filename)
		print file_path
		try:
			with open(file_path, 'r') as f:
				content = f.read()
				content = content.decode('utf-8')
				if regx1.findall(content) or regx2.findall(content):
					content = regx1.sub(domain, content)
					content = regx2.sub(repl1, content)
				else:
					index1 = random.choice(xrange(100))
					content = u'%s%s%s' % (content[:index1], domain , content[index1:])
					index2 = random.choice(xrange(101, 500))
					content = u'%s%s%s%s%s' % (content[:index2], u'(40页小说网 ', domain , u')', content[index2:]) 
			with open(file_path, 'w') as f:
				f.write(content.encode('utf-8'))
				f.flush()
		except:
			pass
				

if __name__ == "__main__":
	import sys
	SUB_PATH = sys.argv[1]
	"""
	for d in os.listdir(SUB_PATH):
		preview_check(d)
	"""
	pool = threadpool.ThreadPool(5)
	requests = threadpool.makeRequests(preview_check, os.listdir(SUB_PATH))
	for req in requests:
		pool.putRequest(req)
	pool.wait()
	#path = '/home/zg163/data/book1'
	#preview_check(path)
				
