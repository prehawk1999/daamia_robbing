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
        print('[WEB] - reca url : ', recaptcha_url)
        
        # 通过首页的html找到验证码地址, 并且访问它
        head = self.modifyHeaders(self.img_headers)
        r = self.sess.get(recaptcha_url, headers=head)
        if r.status_code == 200:
            reca = decode_reCaptchaBytes(r.content)
            if reca['code'] != 0:
                print('[WEB] - error getting recaptcha, ret: ', reca)
                return
            return reca['data']['recognition']
                
    
    def postFormDataJson(self, url, pydict, token):
        url = self.extractUrl(url)
        print('[WEB] - postFormDataJson query : ', url)
        
        head = self.modifyHeaders(self.json_headers)
        head['__RequestVerificationToken'] = token
        
        data = urllib.parse.urlencode(pydict)
        r = self.sess.post(url, data=data, headers=head)
        if r.status_code == 200:
            return r.json()
        else:
            print('[WEB] - ERR, code: ', r.status_code)
                
    def getQueryDataJson(self, url, token):
        url = self.extractUrl(url)
        print('[WEB] - getQueryDataJson query : ', url)
        
        head = self.modifyHeaders(self.json_headers)
        head['__RequestVerificationToken'] = token
        
        r = self.sess.get(url, headers=head)
        if r.status_code == 200:
            return r.json()
        else:
            print('[WEB] - ERR, code: ', r.status_code)
                
        
    def getHtmlSoup(self, url):
        url = self.extractUrl(url)
        print('[WEB] - getHtmlSoup query : ', url)
        
        head = self.modifyHeaders(self.html_headers)
        self.previous_url = url
        
        r = self.sess.get(url, headers=head)
    
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
        else:
            print('[WEB] - ERR, code: ', r.status_code)
    
    def postFormDataSoup(self, url, pydict):
        url = self.extractUrl(url)
        print('[WEB] - postFormDataSoup query: ', url)
        
        data = urllib.parse.urlencode(pydict)
        head = self.modifyHeaders(self.form_headers)
        self.previous_url = url
        
        r = self.sess.post(url, data=data, headers=head)
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
        else:
            print('[WEB] - ERR, code: ', r.status_code)
            

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
    

if __name__ == '__main__':
    web = main()
    pass