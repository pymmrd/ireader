# -*- coding:utf-8 -*-

import json
from hashlib import md5

def get_img_status():
	adict = {}
	with open('img.txt', 'r') as f:
		for line in f:
			line = line.strip()
			name, author, img, status = line.split('\t')
			key = md5('%s%s' % (name, author)).hexdigest()
			adict.setdefault(key, (img, status))
	with open('img.json', 'w') as f:
		json.dump(adict, f)

if __name__ == "__main__":
	get_img_status()
			
