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
from webloader import WebLoader
import codecs


web = WebLoader()

#%%

# 通过首页获取cookies
soup = web.getHtmlSoup('https://online.vfsglobal.com/Global-Appointment/')

path = soup.find(id='CaptchaImage')
code = web.getReCaptchaCode(path['src'])
print(code)

# 获取__RequestVerificationToken
#token = None
#cookie_dict = r.cookies.get_dict()
#for name,value in cookie_dict.items():
#    if name.startswith('__RequestVerificationToken'):
#        token = value

#if token is None:
#    print('token not found')
#    exit(1)

#%%
form = {}
form['__RequestVerificationToken'] = soup.find(name='input').attrs['value']         # 刚好是第一个input
form['reCaptchaPublicKey'] = soup.find(id='reCaptchaPublicKey').attrs['value']
form['CaptchaInputText'] = code
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
home_soup = web.postFormDataSoup('https://online.vfsglobal.com/Global-Appointment/', form)


if home_soup is None:
    print('login failed ')
    exit(1)
    
#%%
# 找到添加预约的页面, 访问它
def filterSelectVAC(node):
    return node.has_attr('href') and node.text.startswith('Schedule Appointment')

vac = home_soup.find(filterSelectVAC)

# selectVAC
vac_soup = web.getHtmlSoup(vac['href'])

#%%
# 1. 获取centre地区
check_area_url = 'https://online.vfsglobal.com/Global-Appointment/Account/CheckSeatAllotment'
areaInfo = web.getJson(check_area_url)

# 2. 获取visa类型
visa_cate_url = 'https://online.vfsglobal.com/Global-Appointment/Account/GetEarliestVisaSlotDate'
visaInfo = web.getJson(visa_cate_url)

# 获取富内容json, 通过json解析内部的表单信息
infoJson = vac_soup.find(id='MissionCountryLocationJSON')
info = json.loads(infoJson.attrs['value'])
print(info)


vac_form = {}
vac_form['paraMissionId'] = vac_soup.find(id='paraMissionId').attrs['value']
vac_form['paramCountryId'] = vac_soup.find(id='paramCountryId').attrs['value']
vac_form['paramCenterId'] = vac_soup.find(id='paramCenterId').attrs['value']
vac_form['LocationId'] = ''





# 登出, 安全退出, 防止被怀疑
# form2 = {}
# form2['__RequestVerificationToken'] = form['__RequestVerificationToken']

# r4 = s.post('https://online.vfsglobal.com/Global-Appointment/Account/LogOff', data=urllib.parse.urlencode(form2), headers=login_headers)
