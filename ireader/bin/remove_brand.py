# -*- coding:utf-8 -*-

import os
import re
import sys

brand = u'全本小说'
regx1 = re.compile(r'[wW]{3}.[qQuUaAbBeEnN]{7}.[cCoOmM]{3}')
regx2 = re.compile(r'%s' % brand)

brand_list = [regx1, regx2]

def replace_logo(path):
	for p, d, f in os.walk(path):
		if not d:
			file_path = os.path.join(p, f)
			

