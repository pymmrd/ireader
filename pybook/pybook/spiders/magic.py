# -*- coding:utf-8 -*-

import chardet
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from pybook.items import PybookItem

DEFAULT_ENCODE = 'utf-8'

class MagicSpider(BaseSpider):
    name = 'magic'

    def __init__(self, *args, **kwargs):
        super(MagicSpider, self).__init__(*args, **kwargs) 
        start_urls = []
        start_urls.append(kwargs.get('start_url'))
        self.start_urls = start_urls
    #pattern = 'http://www.quanben.com/book1/0/%s/'

    #start_urls = [ pattern % str(i) for i in xrange(5, 0, -1)]
    #start_urls = ['http://www.quanben.com/book1/0/36/'] 

    def parse(self, response):
        encoding = chardet.detect(response.body)['encoding']
        if encoding != DEFAULT_ENCODE:
            response.body = response.body.decode(encoding, 'replace').encode(DEFAULT_ENCODE)
        hxs = HtmlXPathSelector(response)                      
        trs = hxs.select("//div[@id='content']/descendant::tr[position()>1]")
        items = []
        for tr in trs:
            tds = tr.select("child::td")
            link = tds[0].select("child::a/@href").extract()[0]
            name = tds[0].select("child::a/text()").extract()[0]
            txt_link = tds[1].select("child::a/@href").extract()[0]
            author = tds[2].select("child::a/text()").extract()[0]
            word_num = tds[3].select('text()').extract()[0]
            update_date = tds[4].select('text()').extract()[0]
            item = PybookItem()
            item['name'] = name
            item['author'] = author
            item['update_date'] = update_date
            item['index_link'] = link
            item['word_num'] = word_num
            item['category'] = 1 
            item['txt_link'] = txt_link
            items.append(item)
        return items

