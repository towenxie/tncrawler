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
    count = 3000   #6174 6173441
    page_size = 1000
    init_index = 0

    def __init__(self):
        self.dbHelper=DBHelper()

    def start_requests(self):
        for _count_index in range(self.count + self.init_index):
            _count_index = _count_index + self.init_index
            sql="select id, url from baiduitem where url != 'error' and id > %d limit %d"
            params=(_count_index*self.page_size, self.page_size)
            _urlitems = self.dbHelper.select(sql,*params)
            _urlitemsCount = len(_urlitems)
            for _index in range(_urlitemsCount):
                _db_id = _urlitems[_index][0]
                _db_url = _urlitems[_index][1]
                self.logger.log(logging.INFO, "Item will crawl spider: count=%d: id=%s" % (_count_index, _db_id))
                if _db_url is not "error":
                    yield scrapy.Request(
                        url = _db_url,
                        meta={'db_id': _db_id},
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
