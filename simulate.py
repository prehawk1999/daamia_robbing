# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 22:48:00 2017

@author: prehawk
"""

from conf import conf as cf
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from lianzhong_api import *
from io import BytesIO

landing = 'https://online.vfsglobal.com/Global-Appointment/'
username = cf.register_user
password = cf.password

def element_screenshot(driver, element, filename):
    bounding_box = (
        element.location['x'], # left
        element.location['y'], # upper
        (element.location['x'] + element.size['width']), # right
        (element.location['y'] + element.size['height']) # bottom
    )
    return bounding_box_screenshot(driver, bounding_box, filename)

def bounding_box_screenshot(driver, bounding_box, filename):
    driver.save_screenshot(filename)
    base_image = Image.open(filename)
    cropped_image = base_image.crop(bounding_box)
    base_image = base_image.resize(cropped_image.size)
    base_image.paste(cropped_image, (0, 0))
    base_image.save(filename)
    return base_image

#%%
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
driver.set_window_size(1440, 900)


#%%
driver.get(landing)

#%%
# test ok, with  real captcha
# driver.get_screenshot_as_file('aaa.png')

el_recap = driver.find_element_by_xpath('//*[@id="CaptchaImage"]')
img_obj = element_screenshot(driver, el_recap, 'bbb.png')
buffer = BytesIO()
img_obj.save(buffer, format='PNG')
img_b64 = base64.b64encode(buffer.getvalue()).decode('ascii')

#%%
recap = decode_reCaptcha(img_b64)
print(recap)

#%%
el_user = driver.find_element_by_xpath('//*[@id="EmailId"]')
el_user.send_keys(username)

el_password = driver.find_element_by_xpath('//*[@id="Password"]')
el_password.send_keys(password)

el_recap_input = driver.find_element_by_xpath('//*[@id="CaptchaInputText"]')
el_recap_input.send_keys(recap['data']['recognition'])

#%%
el_next = driver.find_element_by_xpath('//*[@id="ApplicantListForm"]/div[4]/input')
el_next.click()

#%%
driver.save_screenshot('next.png')


