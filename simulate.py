# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 22:48:00 2017

@author: prehawk
"""

from conf import conf as cf
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


landing = 'https://online.vfsglobal.com/Global-Appointment/'
username = cf.register_user
password = cf.password


#chromedriver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
chromedriver = 'bin\windows\chromedriver.exe'
if platform.system() == 'Linux':
    chromedriver = 'bin/linux/chromedriver'
elif platform.system() == 'Darwin':
    chromedriver = 'bin/mac/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# chrome_options.binary_location = '/opt/google/chrome/chrome'


driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)