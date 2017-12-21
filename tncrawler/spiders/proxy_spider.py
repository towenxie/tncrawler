#encoding=UTF-8

import sys
import logging
import importlib
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from tncrawler.items import ProxyItem
from tncrawler.manager.proxy_manager import ProxyManager

class ProxySpider(CrawlSpider):
    name = 'prycrawler'
    logger = logging.getLogger('ProxySpider')
    start_urls = ['http://www.mimiip.com/gngao/1',
                  'http://www.mimiip.com/gngao/2',
                  'http://www.mimiip.com/gngao/3',
                  'http://www.mimiip.com/gngao/4',
                  'http://www.mimiip.com/gngao/5',
                  'http://www.mimiip.com/gngao/6',
                  'http://www.mimiip.com/gngao/7',
                  'http://www.mimiip.com/gngao/8',
                  'http://www.mimiip.com/gngao/9',
                  'http://www.mimiip.com/gngao/10']

    def __init__(self, *a, **kw):
        super(ProxySpider, self).__init__(*a, **kw)
        self.logger.log(logging.INFO, "Start to remove old proxy data from MySQLdb.")
        proxy_manager = ProxyManager()
        proxy_manager.data_clear()
        self.logger.log(logging.INFO, "End to remove old proxy data from MySQLdb.")

    def parse(self, response):
        proxies_set = set()
        for sel in response.xpath('//*[@id="middle_wrapper"]/div/table/tr[position()>1]'):
            ip = sel.xpath('td[1]/text()').extract()[0]
            port = sel.xpath('td[2]/text()').extract()[0]
            proxies_set.add((ip, port))
        if proxies_set:
            for proxy_ele in proxies_set:
                ip, port = proxy_ele
                proxy_item = ProxyItem()
                proxy_item['id'] = ip + ':' + port
                proxy_item['ip'] = ip
                proxy_item['port'] = port
                yield proxy_item

class ProxySpider2(ProxySpider):
    name = 'proxy_xicidaili'
    start_urls = ['http://www.xicidaili.com/nn/1']

    def __init__(self, *a, **kw):
        super(ProxySpider, self).__init__(*a, **kw)
        self.logger.log(logging.INFO, "Start to remove old proxy data from MySQLdb.")
        proxy_manager = ProxyManager()
        proxy_manager.data_clear()
        self.logger.log(logging.INFO, "End to remove old proxy data from MySQLdb.")

    def parse(self, response):
        proxies_set = set()
        for sel in response.xpath('//*[@id="ip_list"]/tr[position()>1]'):
            ip = sel.xpath('td[2]/text()').extract()[0]
            port = sel.xpath('td[3]/text()').extract()[0]
            proxies_set.add((ip, port))
        if proxies_set:
            for proxy_ele in proxies_set:
                ip, port = proxy_ele
                proxy_item = ProxyItem()
                proxy_item['id'] = ip + ':' + port
                proxy_item['ip'] = ip
                proxy_item['port'] = port
                yield proxy_item

class ProxySpider3(ProxySpider):
    name = 'proxy_httpsdaili'
    start_urls = ['http://www.httpsdaili.com/free.asp?page=1',
                  'http://www.httpsdaili.com/free.asp?page=2',
                  'http://www.httpsdaili.com/free.asp?page=3',
                  'http://www.httpsdaili.com/free.asp?page=4',
                  'http://www.httpsdaili.com/free.asp?page=5',
                  'http://www.httpsdaili.com/free.asp?page=6',
                  'http://www.httpsdaili.com/free.asp?page=7',
                  'http://www.httpsdaili.com/free.asp?page=8',
                  'http://www.httpsdaili.com/free.asp?page=9',
                  'http://www.httpsdaili.com/free.asp?page=10']

    # def __init__(self, *a, **kw):
    #     super(ProxySpider, self).__init__(*a, **kw)
    #     self.logger.log(logging.INFO, "Start to remove old proxy data from MySQLdb.")
    #     proxy_manager = ProxyManager()
    #     proxy_manager.data_clear()
    #     self.logger.log(logging.INFO, "End to remove old proxy data from MySQLdb.")

    def parse(self, response):
        importlib.reload(sys)
        proxies_set = set()
        for sel in response.xpath('//*[@id="list"]/table/tbody/tr[position()>1]'):
            ip = sel.xpath('td[1]/text()').extract()[0]
            port = sel.xpath('td[2]/text()').extract()[0]
            proxies_set.add((ip, port))
        if proxies_set:
            for proxy_ele in proxies_set:
                ip, port = proxy_ele
                proxy_item = ProxyItem()
                proxy_item['id'] = ip + ':' + port
                proxy_item['ip'] = ip
                proxy_item['port'] = port
                yield proxy_item
