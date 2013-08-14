# -*- coding:utf-8 -*-

from django.conf import settings

def ireader(request):
	return {
			'domain': settings.DOMAIN,
	}
