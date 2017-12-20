# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:31:06 2017

@author: prehawk
"""

import gevent
from datetime import datetime


#%%
###############################
###未登录态, 验证码输入, 登录
###可以预先登录
##############################


def waitUntil(month, day, hour, minute):
    while True:
        now = datetime.now()
        if now.month >= month and now.day >= now.day and now.hour >= hour and now.minute >= minute:
            print('ok')
            break
        else:
            gevent.sleep(1)
        