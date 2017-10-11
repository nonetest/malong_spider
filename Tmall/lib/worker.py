#!/usr/bin/env python
# coding=utf-8

from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from parser import parser_info


class Worker(Thread):

    def __init__(self, file_lock, task_queue):
        super(Worker, self).__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.-10 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Refer': 'https://list.tmall.com/search_product.htm?q=%C5%AE%D7%B0&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp.pc_1_searchbutton'
        }
        self.task_queue = task_queue
        self.file_lock = file_lock
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.headers['User-Agent']
        dcap["phantomjs.page.settings.Refer"] = self.headers['Refer']
        dcap["phantomjs.page.settings.loadImages"] = False
        dcap['phantomjs.page.customHeaders.Cookie'] = open('lib/cookies').read().rstrip()
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)

    def set_proxy(self):
        """
        set PhantomJS proxy
        """
        pass

    def run(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            url = task['detail']
            self.driver.get(url)

            detail_info = parser_info(self.driver.page_source)
            with self.file_lock:
                with open('content.csv', 'a') as f:
                    for i in task:
                        f.write(task[i].encode('utf-8')+',')
                    f.write(detail_info['collect_count'].encode('utf-8')+',')
                    f.write(detail_info['comment_count'].encode('utf-8') + ',')
                    f.write('"'+detail_info['detail'].__str__()+'\"' + '\n')

            self.task_queue.task_done()
