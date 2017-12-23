# -*- coding: utf-8 -*-

import scrapy
import logging
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

from tncrawler.manager.dbhelper import DBHelper
from tncrawler.items import BaiDuItem
from tncrawler.items import OtherItem

class BaiduSpider(CrawlSpider):
    name="tncrawler"
    allowed_domains=["www.baidu.com"]
    key_word = "%s 早期症状 初期症状"
    page_count = 10 #下载的页面数
    logger = logging.getLogger('BaiduSpider')

    def __init__(self):
        self.dbHelper=DBHelper()
        sql="select name from resitem limit %d, %d"
        params=(0, 1)
        self.resitems = self.dbHelper.select(sql,*params)
        self.resitemsCount = len(self.resitems)
        params=('baiduitem',)
        # self.dbHelper.clear(*params) #是否清DB数据

    def parse_search_word(self, *params):
        return self.key_word % params

    def start_requests(self):
        self.index = 0
        self.cindex = -1
        self.page = 0
        self.pageCount = self.page_count
        _search_word = self.key_word % self.resitems[self.index][0]
        yield scrapy.Request(
            url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page),
            callback=self.parse_title)

    def parse_detail(self, response):
        item = BaiDuItem()
        try:
            item['name'] = response.meta['name']
            item['url'] = response.url
            item['text'] = response.text
        except:
            item['name'] = 'error'
            item['url'] = 'error'
            item['text'] = 'error'
        yield item

    def parse_title(self, response):
        self.se=Selector(response)
        if (self.cindex != self.index):
            self.cindex = self.index
            self.pageCount = self.page_count
        # resDivs=self.se.xpath("//div[@id='content_left']/div[@class='result-op c-container xpath-log']").extract()
        resDivs=self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')]").extract()
        for i in range(len(resDivs)):
            i=i+1
            baidu_url = self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')][%d]/h3/a/@href" % i).extract_first()
            if baidu_url:
                yield scrapy.Request(
                    url = baidu_url,
                    meta={'name': self.resitems[self.index][0]},
                    callback=self.parse_detail)

        self.page += 1
        if (self.page < self.pageCount):
            _search_word = self.key_word % self.resitems[self.index][0]
            yield scrapy.Request(
                url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page*10),
                callback=self.parse_title)
        else:
            self.index += 1
            if (self.index < self.resitemsCount):
                self.page = 0
                self.pageCount = self.page_count
                _search_word = self.key_word % self.resitems[self.index][0]
                yield scrapy.Request(
                    url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page),
                    callback=self.parse_title)
