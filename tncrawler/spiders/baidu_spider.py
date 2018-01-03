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
        sql="select id, name from resitem limit %d,%d"
        # params=(24869, 73000)
        params=(24869, 20000)
        self.resitems = self.dbHelper.select(sql,*params)
        self.resitemsCount = len(self.resitems)
        # params=('baiduitem',)
        # self.dbHelper.clear(*params) #是否清DB数据

    def start_requests(self):
        for _index in range(self.resitemsCount):
            _resid = self.resitems[_index][0]
            _resname = self.resitems[_index][1]
            self.logger.log(logging.INFO, "Item will crawl spider: %d: %s" % (_resid, _resname))
            for _page in range(self.page_count):
                _search_word = self.key_word % _resname
                yield scrapy.Request(
                    url='https://www.baidu.com/s?wd=%s&pn=%d' % (_search_word, _page*10),
                    meta={'res_name': _resname, 'res_id': _resid},
                    callback=self.parse_title)

    def parse_title(self, response):
        self.se=Selector(response)
        # resDivs=self.se.xpath("//div[@id='content_left']/div[@class='result-op c-container xpath-log']").extract()
        resDivs=self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')]").extract()
        for i in range(len(resDivs)):
            i=i+1
            baidu_url = self.se.xpath("//div[@id='content_left']/div[contains(@class,'result')][%d]/h3/a/@href" % i).extract_first()
            item = RESItem()
            item['id'] = response.meta['res_id']
            item['urls'] = list()
            try:
                item['name'] = pymysql.escape_string(response.meta['res_name'])
            except:
                item['name'] = 'error'
            if baidu_url:
                try:
                    item['urls'].append(baidu_url)
                except:
                    item['urls'] = 'error'
            yield item
