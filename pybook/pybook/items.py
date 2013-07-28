# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

MAGIC = FINISHED = 1
SORD = UNFINISHED = 2
DUSHI = 3
LOVER = 4
TIME_TRAVEL = 5
GAME = 6
MONSTER = 7
SICIENCE = 8
OTHER = 9

class PybookItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    author = Field()
    word_num = Field()
    update_date = Field()
    index_link = Field()
    txt_link = Field()
    status = Field()
    category = Field()

class PybookItemDetail(Item):
    name = Field()
    intro = Field()
    content = Field()
    
    
