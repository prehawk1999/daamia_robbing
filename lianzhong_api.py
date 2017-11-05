# coding: utf-8

import base64
import requests
import json
from conf import conf as cf

param = {}
param['softwareId'] = '8108'
param['softwareSecret'] = cf.yanzheng_sk
param['username'] = cf.yanzheng_user
param['password'] = cf.password
    
def check_points(param):
    s = requests.session()
    r = requests.post('https://v2-api.jsdama.com/check-points', data = json.dumps(param))
    print(json.loads(r.content.decode('utf8')))

def decode_reCaptcha(img_b64):
    param['captchaType'] = 1101
    param['captchaMinLength'] = 5
    param['captchaMaxLength'] = 5
    param['captchaData'] = img_b64   
    url = 'https://v2-api.jsdama.com/upload'
    s = requests.session()
    r = requests.post(url, data = json.dumps(param))
    return json.loads(r.content.decode('utf8'))


if __name__ == '__main__':
    url = 'https://v2-api.jsdama.com/upload'
    img_b64 = ''
    with open('bbb.png', 'rb') as f:
        img_content = f.read()
        img_b64 = base64.b64encode(img_content)
        img_b64 = img_b64.decode('ascii')
    
    #check_points(param)
    a = decode_reCaptcha(img_b64)
    print(a)

