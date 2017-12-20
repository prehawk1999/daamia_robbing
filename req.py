# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 23:35:11 2017

@author: prehawk
"""

import gevent
from gevent import monkey; monkey.patch_all()
from datetime import datetime


def waitUntil(day, hour, minute):
    while True:
        now = datetime.now()
        if now.day >= now.day and now.hour >= hour and now.minute >= minute:
            print('ok')
            break
        else:
            gevent.sleep(1)
        
        
# 每一个账号一个greenlet,         
def rob_worker(tag):
    pass        
        
        
        
def main():
    pass










if __name__ is '__main__':
    main()