# -*- coding:utf -*-

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_partition(pk):
	return pk % settings.BOOKITEM_PARTITION

@register.filter
def rm_str(string, tar_str):
	#import pdb
	#pdb.set_trace()
	return string.replace(tar_str, '')
