#!/usr/bin/env python
# coding=utf-8

import requests
from Queue import Queue
from threading import Lock

from lib.parser import parser_product, random_choice_cookie
from lib.worker import Worker


def get_product(url):
    cookies = random_choice_cookie()
    headers = {
        'User-Agent': 'Mozilla/5.-10 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Refer': 'https://list.tmall.com/search_product.htm?q=%C5%AE%D7%B0&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp.pc_1_searchbutton'
    }

    product_list = []
    for url in start_url:
        resp = requests.get(url, headers=headers, cookies=cookies)
        product_list += parser_product(resp.content)
        print len(product_list)
    return product_list


if __name__ == '__main__':
    start_url = [
        'https://list.tmall.com/search_product.htm?q=%C5%AE%D7%B0&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',
        'https://list.tmall.com/search_product.htm?q=%C4%D0%D7%B0&type=p&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',
        'https://list.tmall.com/search_product.htm?q=%C5%AE%D0%AC&type=p&spm=a220m.1000858.a2227oh.d100&from=.list.pc_1_searchbutton',
        'https://list.tmall.com/search_product.htm?q=%C4%D0%D0%AC&type=p&spm=a220m.1000858.a2227oh.d100&from=.list.pc_1_searchbutton',
    ]
    file_lock = Lock()
    for i in start_url:
        product_list = get_product(i)
    task_queue = Queue()

    for p in product_list:
        task_queue.put(p)

    thread = []
    for i in range(4):
        thread.append(Worker(file_lock, task_queue))

    for i in thread:
        i.start()
    for i in thread:
        i.join()
