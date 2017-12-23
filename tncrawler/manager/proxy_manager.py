# -*- coding: utf-8 -*-

import random
import urllib3

from tncrawler.items import ProxyItem
from tncrawler.manager.dbhelper import DBHelper

class ProxyManager():
    def __init__(self):
        self.dbHelper=DBHelper()

    def get_one(self):

        def check_proxy(proxy):
            url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
            # headers = urllib3.make_headers(proxy_basic_auth=’myusername:mypassword’)
            # proxy = urllib3.ProxyManager("http://%s:%s" % (proxy.ip, proxy.port), proxy_headers=headers)
            proxy_handler = urllib3.ProxyManager("http://%s:%s" % (proxy['ip'], proxy['port']))
            try:
                response = proxy_handler.request('GET', url, timeout=3)
                return response.status == 200
            except Exception:
                return False
        all_proxies = self.data_select()
        num_proxies = len(all_proxies)
        if (num_proxies -1) > 0:
            ok = False
            proxy = ProxyItem()
            while not ok:
                index = random.randint(0, num_proxies - 1)
                value = all_proxies[index]
                proxy['id'] = value[0]
                proxy['ip'] = value[1]
                proxy['port'] = value[2]
                ok = check_proxy(proxy)
            return proxy
        else:
            return ProxyItem()

    def data_count(self):
        sql="select count(*) from proxy"
        params=()
        return self.dbHelper.count(sql,*params)

    def data_select(self):
        sql="select * from proxy"
        params=()
        return self.dbHelper.select(sql,*params)

    def data_clear(self):
        params=("proxy",)
        self.dbHelper.clear(*params)

if __name__=='__main__':
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    prox_url = "http://%s:%s" % ('185.153.248.130', '80')
    http = urllib3.ProxyManager(prox_url)
    r = http.request('GET', url)
    print(r.status)
