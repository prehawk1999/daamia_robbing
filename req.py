# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:15:16 2017

@author: prehawk
"""

import time
import json
import vfs
from conf import conf as cf
from webloader import WebLoader
from conf import client as cl

#%%
###############################
###未登录态, 验证码输入, 登录
###可以预先登录
##############################
web = WebLoader()
soup = web.getHtmlSoup('https://online.vfsglobal.com/Global-Appointment/')
if soup is None:
    raise Exception('main page http get error')

print('[MAIN] - Stage : get before login main page')
token = vfs.getReqTokenBySoup(soup)

path = soup.find(id='CaptchaImage')
code = web.getReCaptchaCode(path['src'])
print('[MAIN] - Stage : success getting reca code : ', code)
   
form = vfs.buildLoginForm(soup, code, cf.register_user, cf.password)
if form is None:
    raise Exception('fill login form error')

print('[MAIN] - Stage : success filling login form : ', form)

home_soup = web.postFormDataSoup('https://online.vfsglobal.com/Global-Appointment/', form)
if not vfs.verifyPage(home_soup, 'HOME PAGE'):
    raise Exception('login failed')

print('[MAIN] - Stage : success login')


#%%
############################################
### 选择签证类型, 出发地点, 准备进入候选人添加
############################################

vac = home_soup.find(vfs.filterSelectVAC)
vac_url = vac['href']
if vac_url is None:
    raise Exception('selectVAC link not found')

# selectVAC
vac_soup = web.getHtmlSoup(vac_url)
token = vfs.getReqTokenBySoup(vac_soup)
if not vfs.verifyPage(vac_soup, 'Select Centre'):
    raise Exception('enter Schedule Appoint error')
    
print('[MAIN] - Stage: success enter selectVAC page')

infoJson = vac_soup.find(id='MissionCountryLocationJSON')
info = json.loads(infoJson.attrs['value'])
sel = vfs.parseMissionLocJson(info, cl.applicants[0])
print('[MAIN] - Stage: success parsing mission country location json')

## 不知道有啥用1
#check_area_url = 'https://online.vfsglobal.com/Global-Appointment/Account/CheckSeatAllotment'
#check_form = {}
#check_form['countryId'] = '11'
#check_form['missionId'] = '22'
#check_form['LocationId'] = '160'
#check_form['Location'] = 'Australia Visa Application Centre-Beijing'
#areaInfo = web.postFormDataJson(check_area_url, check_form, token)
#print(areaInfo)

## 不知道有啥用2
#visa_cate_url = 'https://online.vfsglobal.com/Global-Appointment/Account/GetEarliestVisaSlotDate'
#visa_form = {}
#visa_form['countryId'] = '11'
#visa_form['missionId'] = '22'
#visa_form['LocationId'] = '160'
#visa_form['VisaCategoryId'] = '418'
#visaInfo = web.postFormDataJson(visa_cate_url, visa_form, token)
#print(visaInfo)

vac_form = vfs.buildMissionForm(vac_soup, sel)

applicant_soup = web.postFormDataSoup(vac_url, vac_form)
if not vfs.verifyPage(applicant_soup, 'Applicant List'):
    raise Exception('enter Applicant list error')

print('[MAIN] - Stage: success enter applicant list')



#%%
###########################################
### 进入添加候选人页面, 添加多个候选人
###########################################

add_page = applicant_soup.find(vfs.filterAddApplicant)
add_page_soup = web.getHtmlSoup(add_page['href'])
token = vfs.getReqTokenBySoup(add_page_soup)
if not vfs.verifyPage(add_page_soup, 'Add New Applicant'):
    raise Exception('enter Add New Applicant error')
    
print('[MAIN] - Stage: success enter Add New Applicant')

# TODO: 多个客户进行配置
add_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/AddApplicant'
apc1 = cl.applicants[0]['form']
apc1['__RequestVerificationToken'] = token

apc2 = cl.applicants[1]['form']
apc2['__RequestVerificationToken'] = token

a_soup = web.postFormDataSoup(add_url, apc1)
if not vfs.verifyPage(a_soup, 'Applicant List'):
    raise Exception('Add Applicant error')
    
print('[MAIN] - Stage: success Add one Applicant')

final_soup = web.postFormDataSoup(add_url, apc2)
if not vfs.verifyPage(final_soup, 'Applicant List'):
    raise Exception('Add Applicant error')
    
print('[MAIN] - Stage: success Add one Applicant')

#%%
# 提交候选人
submit_applicant_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/ApplicantList'
submit_form = vfs.buildCalendarSubmitForm(final_soup)
calendar_soup = web.postFormDataSoup(submit_applicant_url, submit_form)
if calendar_soup.find(name='title').text.find('Booking Appointment') == -1:
    raise Exception('enter Booking Appointment error')

print('[MAIN] - Stage: success enter Booking Appointment')

#%%
#############################################
### 确认最终时间
#############################################


today_time = time.gmtime()
get_calendar_token = vfs.getReqTokenBySoup(calendar_soup)
get_calendar_json_url = 'https://online.vfsglobal.com/Global-Appointment/Calendar/GetCalendarDaysOnViewChange'
query = '?month=%s&year=%s&bookingType=%s&_=%s' % (today_time.tm_mon, today_time.tm_year, 'General', int(time.time()*1000))
get_calendar_json = web.getQueryDataJson(get_calendar_json_url + query, get_calendar_token)
if get_calendar_json is None:
    raise Exception('get calendar json error')
    
print('[MAIN] - Stage: success getting calendar json')

# TODO: 根据所有人的合理时间进行申请
sel_time_band = vfs.parseGetCalendarDaysJson(get_calendar_json, cl.applicants[0])
if sel_time_band is None:
    raise Exception('select time band error, config error!')
    
print('[MAIN] - Stage: success selecting time band')



#%%
final_submit_url = 'https://online.vfsglobal.com/Global-Appointment/Calendar/FinalCalendar'

## TODO: 动态修改
final_form = {
    '__RequestVerificationToken': get_calendar_token,
    'AvailableDatesAndSlotsJSON': '[]',
    'EncryptedSelectedAllocationId': sel_time_band,
    'PreviousScheduleDateTimeMessage': '',
    'URN AUGZ542020123': '',
    'isPaymentPageRequired': 'False',
    'isCriteriaPageRequired': 'False',
    'VisaCategory': 'General Visa',
    'PurposeOfTravel': '',
    'EnablePaymentGatewayIntegration': 'False',
    'NumberOfApplicants': '2',
    'applicantList.PassportNumber': '',
    'applicantList.AURN': '',
    'BookingcategoryType': 'General',
    'selectedTimeBand': sel_time_band
}


calendar_soup.find(id='URN').attrs['value']

after_submit_soup = web.postFormDataSoup(final_submit_url, final_form)
if after_submit_soup.find(name='title').text.find('Final Confirmation') == -1:
    raise Exception('enter Final Confirmation error')
    
print('[MAIN] - Stage: success Final Confirmation')


#%%
###############################################
### 最终提交(能够获得电子邮件)
###############################################
get_email_token = after_submit_soup.find(name='input').attrs['value']
get_email_url = 'https://online.vfsglobal.com/Global-Appointment/Payment/InitiatePayment'
get_email_form = {
        '__RequestVerificationToken': get_email_token,
        'ApplicantGroupEmail': after_submit_soup.find(id='ApplicantGroupEmail').attrs['value'],
        'IsCountryEmailFecility': 'False',
        'TotalAmount': '0',
        'EnablePaymentGatewayIntegration': 'False',
        'SurchargeFeeEnabled': 'False',
        'CanApplicantReachoutVFS': 'false'
}

last_soup = web.postFormDataSoup(get_email_url, get_email_form)
if last_soup.find(name='title').text.find('HOME PAGE') == -1:
    raise Exception('final confirmation error')

print('[MAIN] - Stage: success final confirmation, check your email')


# 登出, 安全退出, 防止被怀疑
# form2 = {}
# form2['__RequestVerificationToken'] = form['__RequestVerificationToken']

# r4 = s.post('https://online.vfsglobal.com/Global-Appointment/Account/LogOff', data=urllib.parse.urlencode(form2), headers=login_headers)
