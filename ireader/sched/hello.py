# -*- coding:utf-8 -*-

import sys
import os

pk = sys.argv[1]

prefix = "#!/bin/sh"

s = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 900 1000 %s 0.3 """ % pk
with open('s103.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s1 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 900 1000 %s 0.2""" % pk
with open('s202.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s2 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 1 100 %s 0.4""" % pk
with open('s304.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s3 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 1000 1100 %s 0.1""" % pk
with open('s401.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s4 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 1100 1200 %s 0.2""" % pk
with open('s502.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s5 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 100 200 %s 0.2""" % pk
with open('s602.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s6 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 200 300 %s 0.5""" % pk
with open('s705.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s7 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 300 400 %s 0.4""" % pk
with open('s804.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s8 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 400 500 %s 0.3""" % pk
with open('s903.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s9 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 500 600 %s 0.4""" % pk
with open('s1004.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s10 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 600 700 %s 0.1""" % pk
with open('s1101.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s11 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 700 800 %s 0.1""" % pk
with open('s1201.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))

s12 = """python /var/www/wwwroot/ireader/ireader/bin/load_full_detail.py 800 900 %s 0.4""" % pk
with open('s1304.sh', 'w') as f:
    f.write('%s%s' % (prefix, os.linesep))
    f.write('%s%s' % (s, os.linesep))
