# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:15:16 2017

@author: prehawk
"""

import requests
from bs4 import BeautifulSoup

prefix = 'https://online.vfsglobal.com'

html_headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
img_headers = {
        'Accept': 'image/png, image/svg+xml, image/jxr, image/*;q=0.8, */*;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Referer': 'https://online.vfsglobal.com/Global-Appointment/'
        }

#%%

with requests.Session() as s:

    r = s.get('https://online.vfsglobal.com/Global-Appointment/', headers=html_headers)
    soup = BeautifulSoup(r.content, 'lxml')
    a = soup.find(id='CaptchaImage')
    recaptcha_url = prefix + a['src']
    print(recaptcha_url)


    rr = s.get(recaptcha_url, headers=img_headers)
    with open('a.png', 'wb') as f:
        f.write(rr.content)
    
    