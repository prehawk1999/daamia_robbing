# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:31:06 2017

@author: prehawk
"""

import time
import json
from conf import conf as cf
from webloader import WebLoader
from conf import client as cl
from vfs import parseMissionLocJson

#%%
###############################
###未登录态, 验证码输入, 登录
###可以预先登录
##############################
web = WebLoader()
soup = web.getHtmlSoup('https://online.vfsglobal.com/Global-Appointment/')
if soup is not None:
    print('[MAIN] - ERR: main page http get error')
    exit
else:
    exit
    

raise Exception('exit', len(soup))
exit(0)
exit
exit
    
print('after')

exit
exit
exit(0)
time.sleep(10)
exit(0)

token = web.getReqTokenBySoup(soup)

path = soup.find(id='CaptchaImage')
print('a')
code = web.getReCaptchaCode(path['src'])
print('b')
#print('[MAIN] - success getting reca code : ', code)
