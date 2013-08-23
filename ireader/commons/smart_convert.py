# -*- coding:utf-8 -*-

import socket
import struct
from django.http import Http404

def convert_int(arg, exct=False):
	try:
		arg = int(arg)
	except (TypeError, KeyError):
		if exct:
			raise Http404
		else:
			arg = 1
	return arg

def ip2long(ip):
	"""
	Convert an IP string to long
	"""
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]

def long2ip(n):
	return socket.inet_ntoa(struct.pack("!L", n))
