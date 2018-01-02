# -*- coding: utf-8 -*-

import scrapy
import logging
import pymysql
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

from tncrawler.manager.dbhelper import DBHelper
from tncrawler.items import BaiDuItem
from tncrawler.items import OtherItem

class DBSpider(CrawlSpider):
    name="dbcrawler"
    allowed_domains=["www.baidu.com"]
    logger = logging.getLogger('DBSpider')

    def __init__(self):
        self.dbHelper=DBHelper()
        sql="select id, url from baiduitem limit %d,%d"
        params=(10, 10)
        self.urlitems = self.dbHelper.select(sql,*params)
        self.urlitemsCount = len(self.urlitems)

    def start_requests(self):
        self.index = 0
        _db_url = self.urlitems[self.index][1]
        if _db_url is not "error":
            yield scrapy.Request(
                url = _db_url,
                meta={'db_id': self.urlitems[self.index][0]},
                callback=self.parse_detail)

    def parse_detail(self, response):
        if response.status == 200:
            item = BaiDuItem()
            item['id'] = response.meta['db_id']
            try:
                item['text'] = response.text
            except:
                item['text'] = 'error'
            yield item
        self.index += 1
        if (self.index < self.urlitemsCount):
            _db_url = self.urlitems[self.index][1]
            if _db_url is not "error":
                yield scrapy.Request(
                    url = _db_url,
                    meta={'db_id': self.urlitems[self.index][0]},
                    callback=self.parse_detail)
