# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 00:20:13 2017

@author: prehawk
"""

import requests
import json
import urllib
import codecs
import time
from bs4 import BeautifulSoup
from lianzhong_api import decode_reCaptchaBytes
from conf import conf as cf
from form import applicant2, applicant1


class WebLoader:
    
    previous_url = None
    
    prefix = 'https://online.vfsglobal.com'

    html_headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
    
    json_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
    
    img_headers = {
            'Accept': 'image/png, image/svg+xml, image/jxr, image/*;q=0.8, */*;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Referer': 'https://online.vfsglobal.com/Global-Appointment/'
            }
    
    form_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://online.vfsglobal.com/Global-Appointment/',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
    
    def extractUrl(self, url):
        if url.startswith('https://'):
            return url
        elif url.startswith('/'):
            return self.prefix + url
        else:
            return self.prefix + '/' + url
        
    def modifyHeaders(self, head):
        if self.previous_url is None:
            return head
        
        head['Referer'] = self.previous_url
        return head
    
    
    def __init__(self):
        self.sess = requests.Session()
        
    
    def getReCaptchaCode(self, path):
        recaptcha_url = self.extractUrl(path)
        print('reca url : ' + recaptcha_url)
        
        # 通过首页的html找到验证码地址, 并且访问它
        head = self.modifyHeaders(self.img_headers)
        r = self.sess.get(recaptcha_url, headers=head)
        if r.status_code == 200:
            reca = decode_reCaptchaBytes(r.content)
            if reca['code'] != 0:
                print('error getting recaptcha')
                print(reca)
                return
            return reca['data']['recognition']
                
    
    def postFormDataJson(self, url, pydict, token):
        url = self.extractUrl(url)
        print('postJson : ' + url)
        
        head = self.modifyHeaders(self.json_headers)
        head['__RequestVerificationToken'] = token
        
        data = urllib.parse.urlencode(pydict)
        r = self.sess.post(url, data=data, headers=head)
        if r.status_code == 200:
            return r.json()
                
    def getQueryDataJson(self, url, token):
        url = self.extractUrl(url)
        print('postJson : ' + url)
        
        head = self.modifyHeaders(self.json_headers)
        head['__RequestVerificationToken'] = token
        
        r = self.sess.get(url, headers=head)
        if r.status_code == 200:
            return r.json()
                
        
    def getHtmlSoup(self, url):
        url = self.extractUrl(url)
        print('getHtmlSoup : ' + url)
        
        head = self.modifyHeaders(self.html_headers)
        self.previous_url = url
        
        r = self.sess.get(url, headers=head)
    
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
        
    def getReqTokenBySoup(self, soup):
        return soup.find(name='input').attrs['value']
    
    def postFormDataSoup(self, url, pydict):
        url = self.extractUrl(url)
        print('postFormDataSoup : ' + url)
        
        data = urllib.parse.urlencode(pydict)
        head = self.modifyHeaders(self.form_headers)
        self.previous_url = url
        
        r = self.sess.post(url, data=data, headers=head)
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
            

def main():
    
    ###############################
    ###未登录态, 验证码输入, 登录
    ##############################
    web = WebLoader()
    soup = web.getHtmlSoup('https://online.vfsglobal.com/Global-Appointment/')
    path = soup.find(id='CaptchaImage')
    code = web.getReCaptchaCode(path['src'])
    print(code)
    
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
    
    home_soup = web.postFormDataSoup('https://online.vfsglobal.com/Global-Appointment/', form)
    title = home_soup.find(name='title').text
    print(title)
    
    
    
    ############################################
    ### 选择签证类型, 出发地点, 准备进入候选人添加
    ############################################
    def filterSelectVAC(node):
        return node.has_attr('href') and node.text.startswith('Schedule Appointment')

    vac = home_soup.find(filterSelectVAC)
    vac_url = vac['href']
    if not vac_url:
        print('selectVAC not found')
        return
    
    # selectVAC
    vac_soup = web.getHtmlSoup(vac_url)
    token = vac_soup.find(name='input').attrs['value']
    
    # 富信息json
    infoJson = vac_soup.find(id='MissionCountryLocationJSON')
    info = json.loads(infoJson.attrs['value'])
    print(info)

    check_area_url = 'https://online.vfsglobal.com/Global-Appointment/Account/CheckSeatAllotment'
    check_form = {}
    check_form['countryId'] = '11'
    check_form['missionId'] = '22'
    check_form['LocationId'] = '160'
    check_form['Location'] = 'Australia Visa Application Centre-Beijing'
    areaInfo = web.postFormDataJson(check_area_url, check_form, token)
    print(areaInfo)

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
    vac_form['paraMissionId'] = 22
    vac_form['paramCountryId'] = 11
    vac_form['paramCenterId'] = ''
    vac_form['MissionCountryLocationJSON'] = infoJson.attrs['value']
    vac_form['MissionId']
    vac_form['CountryId']
    vac_form['LocationId']
    vac_form['LocationId']
    vac_form['VisaCategoryId']
    vac_form['AppointmentType']
    applicant_soup = web.postFormDataSoup(vac_url, vac_form)
    print(len(applicant_soup))
    
    
    
    ###########################################
    ### 进入添加候选人页面, 添加多个候选人
    ###########################################
    def filterAddApplicant(node):
        return node.has_attr('href') and node.attrs['href'].startswith('/Global-Appointment/Applicant/AddApplicant')
    
    add_page = applicant_soup.find(filterAddApplicant)
    
    add_page_soup = web.getHtmlSoup(add_page)
    
    add_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/AddApplicant'
    
    web.postFormDataSoup(add_url, applicant1)
    final_soup = web.postFormDataSoup(add_url, applicant2)
    
    submit_token = final_soup.find(name='input').attrs['value']
    
    # 提交候选人
    submit_applicant_url = 'https://online.vfsglobal.com/Global-Appointment/Applicant/ApplicantList'
    submit_form = {}
    submit_form['__RequestVerificationToken'] = submit_token
    submit_form['URN'] = final_soup.find(id='URN').attrs['value']
    submit_form['EnablePaymentGatewayIntegration'] = 'False'
    submit_form['IsVAFValidationEnabled'] = 'False'
    submit_form['IsEndorsedChildChecked'] = '0'
    submit_form['NoOfEndorsedChild'] = '0'
    submit_form['IsEndorsedChild'] = '0'
    calendar_soup = web.postFormDataSoup(submit_applicant_url, submit_form)
    
    
    
    
    
    #############################################
    ### 确认最终时间
    #############################################
    get_calendar_token = calendar_soup.find(name='input').attrs['value']
    get_calendar_json_url = 'https://online.vfsglobal.com/Global-Appointment/Calendar/GetCalendarDaysOnViewChange'
    query = '?month=%s&year=%s&bookingType=%s&_=%s' % (12, 2017, int(time.time()*1000))
    web.getQueryDataJson(get_calendar_json_url + query, get_calendar_token)
    
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
        
if __name__ == '__main__':
    web = main()
    pass