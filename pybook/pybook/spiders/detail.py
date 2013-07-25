# -*- coding:utf-8 -*-

import re
import os
import time
import urllib2
from lxml import html
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from pybook.items import PybookItemDetail

DEFAULT_ENCODE = 'utf-8'
#demo = Www,quanBEn,cOM
MEDIA_ROOT = '/home/zg163/data/'

class DetailSpider(BaseSpider):
    name = 'detail'

    def __init__(self, *args, **kwargs):
        super(MagicSpider, self).__init__(*args, **kwargs) 
        json_file = kwargs.get('json_file')
        with open(json_file, 'r') as f:
            data = json.load(f)
            start_urls = [item.get('index_link' for item in data)] 
        self.start_urls = start_urls

    def tryAgain(self, url, retries=0):
        content = ''
        if retries < 4:
            try:
                time.sleep(30)
                content = urllib2.urlopen(req).read()
            except :
                retries += 1
                content = self.tryAgain(url, retries)
        return content

    def get_content(self, url):
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
        ]
        headers = {'User-Agent':choice(user_agents)}
        req = urllib2.Request(url=url, headers=headers)
        try:
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError, e:
            if e.code == 503 : 
                time.sleep(30)
                content = self.tryAgain(req, 0)
        except :
            time.sleep(30)
            content = self.tryAgain(req, 0)
        return content

    def get_detail(self, url):
        detail = ''
        content = self.get_content(url)
        if content:
            dom = html.fromstring(content)
            ct = dom.xpath("//div[@id='content']")[0]
            regx = re.compile('div.id="content">(?P<detail>.+)</div>')
            detail = regx.match(html.tostring(ct)).group('detail').decode('gbk').encode('utf-8')
        else:
            with open('miss.txt', 'a') as f:
                f.write('%s%s' % ( url, os.linesep))
        return detail

    def save_detail(self, title, url, pk):
        detail = self.get_detail(url)
        book_dir = '%s/%s' % ('book', title)
        sub_path = os.path.join(MEDIA_ROOT, book_dir)
        if not os.path.exists(sub_path):
            os.mkdirs(sub_path)
        book_url = '%s/%s' % ( book_dir, pk) 
        book_path = os.path.join(sub_path, book_url)
        with open(book_path, 'w') as f:
            f.write(detail)
        return book_url

    def parse(self, response):
        """
        out = { 'name'; ''
                'intro': ''
                'content': []/{}
        }
        """
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
            detail = {}
            for tr in items:
                tds = tr.xpath("child::td")
                if len(tds) == 1:
                    part = tds[0].text
                    detail[part] = []
                else:
                    links = tr.xpath("child::a")
                    for link in links:
                        tmp_dict = {}
                        href = link.attrib['href'] 
                        match = regx.match(href)
                        pk = int(match.group('pk'))
                        text = link.text
                        detail_url = '%s/%s' % (url, href)
                        book_url = self.save_detail(title, detail_url, pk)
                        tmp_dict['id'] = pk
                        tmp_dict['title'] = text
                        tmp_dict['book_url'] = book_url
