from book import models
from django.conf import settings

def get_bookitem_model(pk, base=models.BookItem, partition=settings.BOOKITEM_PARTITION):
	num = pk % partition
	name = "%s%s" %(base.__name__, num)
	return getattr(models, name)
	

