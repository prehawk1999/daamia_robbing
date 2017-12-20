# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 23:47:33 2017

@author: prehawk
"""

import sys

import gevent
from gevent import monkey

monkey.patch_all()

import requests

def worker(url):
    print('enter worker')
    content = requests.get(url)
    print(content)

urls = ['https://github.com/save-net-neutrality']*5

def by_requests():
    print('enter by_requests?')
    jobs = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(jobs)


if __name__=='__main__':
    by_requests()