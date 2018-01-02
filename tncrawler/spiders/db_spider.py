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
        sql="select id, url from baiduitem where url != 'error' limit %d,%d"
        params=(0, 10000)
        self.urlitems = self.dbHelper.select(sql,*params)
        self.urlitemsCount = len(self.urlitems)

    def start_requests(self):
        for _index in range(self.urlitemsCount):
            _db_url = self.urlitems[_index][1]
            if _db_url is not "error":
                yield scrapy.Request(
                    url = _db_url,
                    meta={'db_id': self.urlitems[_index][0]},
                    callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            item = BaiDuItem()
            item['id'] = response.meta['db_id']
            try:
                if response.status == 200:
                    item['text'] = response.text
                else:
                    item['text'] = 'error'
            except:
                item['text'] = 'error'
            yield item
        except Exception as error:
            self.logger.log(logging.ERROR, error)
