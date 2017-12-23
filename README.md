# TNCrawler使用手册

## 安装所需软件
1. python3.6
2. mysql数据库
3. Anaconda(可选)

## 安装依赖
<pre>
pip install scrapy
pip install pymysql
pip install urllib3
</pre>


## 运行
### 创建DB
文件位置：db/baidudb.sql
<pre>
# 代理数据表
1. proxy
# 疾病数据表
2. resitem
# 百度爬虫数据表
3. baiduitem
</pre>

### 运行爬虫
1.爬取所有代理IP

<pre>
命令：
scrapy crawl prycrawler
scrapy crawl proxy_xicidaili
scrapy crawl proxy_httpsdaili
</pre>

2.疾病列表存储到DB里面
<pre>
位置：demo\tncrawler\manager\reshelper.py
命令：python reshelper.py
</pre>

3.爬取百度数据
<pre>

命令：scrapy crawl tncrawler 或者 python main.py
原理，是从resitem表读取疾病列表，然后循环爬虫，获得数据结果存储在表baiduitem中。
</pre>
相关配置
<pre>

1. 配置一次爬取的疾病列表个数
位置：baidu_spider.py
-----------------------------------
    def __init__(self):
        self.dbHelper=DBHelper()
        sql="select name from resitem limit %d, %d"
        params=(0, 1) //更改这个数值

2. 配置搜索的关键字
位置：baidu_spider.py
----------------------------------
class BaiduSpider(CrawlSpider):
    name="tncrawler"
    allowed_domains=["www.baidu.com"]
    key_word = "%s 早期症状 初期症状" // 更改这个关键字

3. 配置数据库
位置：tncrawler\settings.py
------------------------------
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'baidudb'         #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = 'root'         #数据库密码，请修改
MYSQL_PORT = 3306               #数据库端口，在dbhelper中使用


</pre>

## 参考

[https://www.cnblogs.com/liruihua/p/5957393.html](https://www.cnblogs.com/liruihua/p/5957393.html "https://www.cnblogs.com/liruihua/p/5957393.html")
