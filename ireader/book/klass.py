from book import models
from django.conf import settings

def get_bookitem_model(base, pk, partition=settings.BOOKITEM_PARTITION):
	num = pk % partition
	name = "%s%s" %(base, num)
	return getattr(models, name)
	

