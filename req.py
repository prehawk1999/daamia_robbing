# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 23:15:16 2017

@author: prehawk
"""

import time
import json
from conf import conf as cf
from webloader import WebLoader
from client import applicants
from vfs import parseMissionLocJson

#%%
###############################
###未登录态, 验证码输入, 登录
###可以预先登录
##############################
web = WebLoader()
soup = web.getHtmlSoup('https://online.vfsglobal.com/Global-Appointment/')
token = web.getReqTokenBySoup(soup)

path = soup.find(id='CaptchaImage')
code = web.getReCaptchaCode(path['src'])
print(code)

form = {}
# 刚好是第一个input 是requestToken
try:
    form['__RequestVerificationToken'] = token        
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
except:
    print('Register Login error')
    
print('submit form : ', form)

home_soup = web.postFormDataSoup('https://online.vfsglobal.com/Global-Appointment/', form)
title = home_soup.find(name='title').text
print(title)


#%%
############################################
### 选择签证类型, 出发地点, 准备进入候选人添加
############################################
def filterSelectVAC(node):
    return node.has_attr('href') and node.text.startswith('Schedule Appointment')

vac = home_soup.find(filterSelectVAC)
vac_url = vac['href']
if not vac_url:
    print('selectVAC not found')
    exit(1)

# selectVAC
vac_soup = web.getHtmlSoup(vac_url)
token = web.getReqTokenBySoup(vac_soup)

# TODO: 富信息json
infoJson = vac_soup.find(id='MissionCountryLocationJSON')
info = json.loads(infoJson.attrs['value'])

sel = parseMissionLocJson(info, applicants[0])

## 不知道有啥用1
check_area_url = 'https://online.vfsglobal.com/Global-Appointment/Account/CheckSeatAllotment'
check_form = {}
check_form['countryId'] = '11'
check_form['missionId'] = '22'
check_form['LocationId'] = '160'
check_form['Location'] = 'Australia Visa Application Centre-Beijing'
areaInfo = web.postFormDataJson(check_area_url, check_form, token)
print(areaInfo)

## 不知道有啥用2
visa_cate_url = 'https://online.vfsglobal.com/Global-Appointment/Account/GetEarliestVisaSlotDate'
visa_form = {}
visa_form['countryId'] = '11'
visa_form['missionId'] = '22'
visa_form['LocationId'] = '160'
visa_form['VisaCategoryId'] = '418'
visaInfo = web.postFormDataJson(visa_cate_url, visa_form, token)
print(visaInfo)



vac_form = {}
vac_form['__RequestVerificationToken'] = token
vac_form['paraMissionId'] = sel['MissionId']
vac_form['paramCountryId'] = sel['CountryId']
vac_form['paramCenterId'] = ''
vac_form['MissionCountryLocationJSON'] = infoJson.attrs['value']
vac_form['MissionId'] = sel['MissionId']
vac_form['CountryId'] = sel['CountryId']
vac_form['LocationId'] = sel['LocationId']
vac_form['VisaCategoryId'] = sel['VisaCategoryId']
vac_form['AppointmentType'] = 'StandardAppointment'
applicant_soup = web.postFormDataSoup(vac_url, vac_form)
print(len(applicant_soup))



#%%
###########################################
### 进入添加候选人页面, 添加多个候选人
###########################################
def filterAddApplicant(node):
    return node.has_attr('href') and node.attrs['href'].startswith('/Global-Appointment/Applicant/AddApplicant')

add_page = applicant_soup.find(filterAddApplicant)
add_page_soup = web.getHtmlSoup(add_page['href'])
token = web.getReqTokenBySoup(add_page_soup)

add_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/AddApplicant'
apc1 = applicants[0]['form']
apc1['__RequestVerificationToken'] = token

apc2 = applicants[1]['form']
apc2['__RequestVerificationToken'] = token
a_soup = web.postFormDataSoup(add_url, apc1)
final_soup = web.postFormDataSoup(add_url, apc2)
token = web.getReqTokenBySoup(final_soup)

#%%
# 提交候选人
final_token = token
submit_applicant_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/ApplicantList'
submit_form = {}
submit_form['__RequestVerificationToken'] = final_token
submit_form['URN'] = final_soup.find(id='URN').attrs['value']
submit_form['EnablePaymentGatewayIntegration'] = 'False'
submit_form['IsVAFValidationEnabled'] = 'False'
submit_form['IsEndorsedChildChecked'] = '0'
submit_form['NoOfEndorsedChild'] = '0'
submit_form['IsEndorsedChild'] = '0'
calendar_soup = web.postFormDataSoup(submit_applicant_url, submit_form)




#%%
#############################################
### 确认最终时间
#############################################
get_calendar_token = calendar_soup.find(name='input').attrs['value']
get_calendar_json_url = 'https://online.vfsglobal.com/Global-Appointment/Calendar/GetCalendarDaysOnViewChange'
query = '?month=%s&year=%s&bookingType=%s&_=%s' % (12, 2017, 'General', int(time.time()*1000))
get_calendar_json = web.getQueryDataJson(get_calendar_json_url + query, get_calendar_token)

#%%
final_submit_url = 'https://online.vfsglobal.com/Global-Appointment/Calendar/FinalCalendar'

final_form = {
    '__RequestVerificationToken': get_calendar_token,
    'AvailableDatesAndSlotsJSON': '[]',
    'EncryptedSelectedAllocationId': '0iPrshRIkUUKoo3XlQeKYw==',
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
    'selectedTimeBand': '0iPrshRIkUUKoo3XlQeKYw=='
}

after_submit_soup = web.postFormDataSoup(final_submit_url, final_form)

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
    


# 登出, 安全退出, 防止被怀疑
# form2 = {}
# form2['__RequestVerificationToken'] = form['__RequestVerificationToken']

# r4 = s.post('https://online.vfsglobal.com/Global-Appointment/Account/LogOff', data=urllib.parse.urlencode(form2), headers=login_headers)
