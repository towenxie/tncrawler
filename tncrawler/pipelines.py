# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import codecs
import json
import logging
from tncrawler.items import *

class JsonWithEncodingPipeline(object):
    '''保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''
    def __init__(self):
        self.file = codecs.open('result.json', 'ab', encoding='utf-8')#保存为json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"#转为json的
        self.file.write(line.decode("unicode_escape"))#写入文件中

        return item
    def spider_closed(self, spider):#爬虫结束时关闭文件
        self.file.close()

class WebcrawlerScrapyPipeline(object):

    logger = logging.getLogger('WebcrawlerScrapyPipeline')
    '''保存到数据库中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行'''

    def __init__(self,dbpool):
        self.dbpool=dbpool

    @classmethod
    def from_settings(cls,settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool('pymysql',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到

    #pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, ProxyItem):
            query=self.dbpool.runInteraction(self._proxy_insert,item)#调用插入的方法
            query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        elif isinstance(item, BaiDuItem):
            try:
                query=self.dbpool.runInteraction(self._baidu_insert,item)#调用插入的方法
                query.addErrback(self._handle_error,item,spider)#调用异常处理方法
            except:
                self._handle_error()
        else:
            self.logger.log(logging.INFO, 'Item is nothing')
        return item

    #写入数据库中
    def _proxy_insert(self,tx,item):
        sql="insert into proxy(id,ip,port) values(%s,%s,%s)"
        params=(item["id"],item["ip"],item["port"],)

        tx.execute(sql,params)
        self.logger.log(logging.INFO, "Item stored in db: %s" % item)

    def _baidu_insert(self,tx,item):
        sql="insert into baiduitem(name,url,text) values(%s,%s,%s)"
        params=(item["name"],item["url"],item["text"],)
        tx.execute(sql,params)
        # self.logger.log(logging.INFO, "Item stored in db: %s" % item["name"])

    #错误处理方法
    def _handle_error(self, failue, item, spider):
        return
        # self.logger.log(logging.ERROR, "database operation exception %s" % failue)
