# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:15:16 2017

@author: prehawk
"""

import requests
from bs4 import BeautifulSoup
from lianzhong_api import decode_reCaptchaBytes
import json
import urllib
from conf import conf as cf

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

login_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://online.vfsglobal.com/Global-Appointment/',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
#%%

# 建立一个session
s = requests.Session()

# 通过首页获取cookies
r = s.get('https://online.vfsglobal.com/Global-Appointment/', headers=html_headers)
soup = BeautifulSoup(r.content, 'lxml')
a = soup.find(id='CaptchaImage')
recaptcha_url = prefix + a['src']
print('reca url : ' + recaptcha_url)

# 通过首页的html找到验证码地址, 并且访问它
rr = s.get(recaptcha_url, headers=img_headers)



# TODO: 验证此验证码
reca = decode_reCaptchaBytes(rr.content)
if reca['code'] != 0:
    print('error getting recaptcha' + reca)
    exit(1)

print('reca result : ')
print(reca)

# 获取__RequestVerificationToken
token = None
cookie_dict = r.cookies.get_dict()
for name,value in cookie_dict.items():
    if name.startswith('__RequestVerificationToken'):
        token = value

if token is None:
    print('token not found')
    exit(1)

#%%
form = {}
form['__RequestVerificationToken'] = soup.find(name='input').attrs['value']
form['reCaptchaPublicKey'] = soup.find(id='reCaptchaPublicKey').attrs['value']
form['CaptchaInputText'] = reca['data']['recognition']
form['Mission']= soup.find(id='Mission').attrs['value']
form['Country'] = soup.find(id='Country').attrs['value']
form['Center'] = soup.find(id='Center').attrs['value']
form['IsGoogleCaptchaEnabled']= soup.find(id='IsGoogleCaptchaEnabled').attrs['value']
form['reCaptchaURL'] = soup.find(id='reCaptchaURL').attrs['value']
form['CaptchaDeText'] = soup.find(id='CaptchaDeText').attrs['value']
form['EmailId'] = cf.register_user # soup.find(id='EmailId').attrs['value']
form['Password'] = cf.password #soup.find(id='Password').attrs['value']
print('submit form : ', form)

# POST 提交表单到主页
rrr = s.post('https://online.vfsglobal.com/Global-Appointment/', data=urllib.parse.urlencode(form), headers=login_headers, allow_redirects=False)
print('response status code : ', rrr.status_code)
print('response cookie : ', rrr.cookies)
print(rrr.content)