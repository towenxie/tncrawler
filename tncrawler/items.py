# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class ProxyItem(Item):
    id = Field()
    ip = Field()
    port = Field()

class RESItem(Item):
    bw = Field()
    name = Field()

class BaiDuItem(Item):
    name = Field()
    url = Field()
    text = Field()

class OtherItem(Item):
    name = Field()
    url = Field()
    text = Field()
