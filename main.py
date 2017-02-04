# -*- coding: utf-8 -*-
# @Date    : 2014-06-25 15:43:36
# @Author  : xindervella@gamil.com yml_bright@163.com

import threading

from utils.TornadoUtils import tornado_main
from utils.CrawlerUtils import crawler_main

threads = []
t1 = threading.Thread(target=tornado_main)
threads.append(t1)

t2 = threading.Thread(target=crawler_main)
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.start()

