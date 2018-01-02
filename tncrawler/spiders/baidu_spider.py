# -*- coding: utf-8 -*-

import scrapy
import logging
import pymysql
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

from tncrawler.manager.dbhelper import DBHelper
from tncrawler.items import RESItem
from tncrawler.items import OtherItem

class BaiduSpider(CrawlSpider):
    name="tncrawler"
    allowed_domains=["www.baidu.com"]
    key_word = "%s 早期症状 初期症状"
    page_count = 10 #下载的页面数
    logger = logging.getLogger('BaiduSpider')

    def __init__(self):
        self.dbHelper=DBHelper()
        sql="select name from resitem limit %d,%d"
        params=(0, 5)
        self.resitems = self.dbHelper.select(sql,*params)
        self.resitemsCount = len(self.resitems)
        params=('baiduitem',)
        self.dbHelper.clear(*params) #是否清DB数据

    def start_requests(self):
        self.index = 0
        self.cindex = -1
        self.page = 0
        self.pageCount = self.page_count
        _search_word = self.key_word % self.resitems[self.index][0]
        yield scrapy.Request(
            url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page),
            meta={'res_name': self.resitems[self.index][0]},
            callback = self.parse_title)

    def parse_title(self, response):
        self.se=Selector(response)
        if (self.cindex != self.index):
            self.cindex = self.index
            self.pageCount = self.page_count
        # resDivs=self.se.xpath("//div[@id='content_left']/div[@class='result-op c-container xpath-log']").extract()
        resDivs=self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')]").extract()
        item = RESItem()
        item['urls'] = list()
        try:
            item['name'] = pymysql.escape_string(response.meta['res_name'])
        except:
            item['name'] = 'error'

        for i in range(len(resDivs)):
            i=i+1
            baidu_url = self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')][%d]/h3/a/@href" % i).extract_first()
            if baidu_url:
                try:
                    item['urls'].append(baidu_url)
                except:
                    item['url'] = 'error'
        yield item

        self.page += 1
        if (self.page < self.pageCount):
            _search_word = self.key_word % self.resitems[self.index][0]
            yield scrapy.Request(
                url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page*10),
                meta={'res_name': self.resitems[self.index][0]},
                callback=self.parse_title)
        else:
            self.index += 1
            if (self.index < self.resitemsCount):
                self.page = 0
                self.pageCount = self.page_count
                _search_word = self.key_word % self.resitems[self.index][0]
                yield scrapy.Request(
                    url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, self.page),
                    meta={'res_name': self.resitems[self.index][0]},
                    callback=self.parse_title)
