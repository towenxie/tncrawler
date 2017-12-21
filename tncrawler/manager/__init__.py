# -*- coding: utf-8 -*-
import urllib3

if __name__=='__main__':
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    prox_url = "http://%s:%s" % ('185.153.248.130', '80')
    http = urllib3.ProxyManager(prox_url)
    r = http.request('GET', url)
    print(r.status)
