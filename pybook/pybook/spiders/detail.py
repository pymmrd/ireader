# -*- coding:utf-8 -*-

import re
from lxml import html
from urllib2 import Request, urlopen
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from pybook.items import PybookItemDetail

DEFAULT_ENCODE = 'utf-8'
#demo = Www,quanBEn,cOM

class DetailSpider(BaseSpider):
    name = 'detail'

    def __init__(self, *args, **kwargs):
        super(MagicSpider, self).__init__(*args, **kwargs) 
        json_file = kwargs.get('json_file')
        with open(json_file, 'r') as f:
            data = json.load(f)
            start_urls = [item.get('index_link' for item in data)] 
        self.start_urls = start_urls

    def parse(self, response):
        intro = ''
        url = response.url
        regx = re.compile('(?P<pk>\d+)\.html')
        intro_identy = u'内容简介：'
        doms = html.fromstring(response.body)
        title = doms.xpath("//h1/text()")[0]
        trs = doms.xpath("//table/child::tr")
        if trs: 
            items = trs[1:-1]
            intro_dom = trs[0].xpath("child:td/text()") 
            if intro_dom:
                intro = intro_dom[0].split(intro_identy)[-1].strip()
            for tr in items:
                tds = tr.xpath("child::td")
                if len(tds) == 1:
                    detail = {}
                    part = tds[0].text
                    detail[prdt] = []
                else:
                    links = tr.xpath("child::a")
                    for link in links:
                        href = link.attrib['href'] 
                        match = regx.match(href)
                        pk = int(match.group('pk'))
                        text = link.text
                        detail_url = '%s/%s' % (url, href)
