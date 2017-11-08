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

#%% 启动Chrome 并且设定屏幕大小
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



#%%


el_yuyue = driver.find_element_by_xpath('//*[@id="Accordion1"]/div/div[2]/div/ul/li[1]/a')
el_yuyue.click()

el_visit_country = driver.find_element_by_xpath('//*[@id="MissionId"]')
el_visit_country.find_element_by_xpath('//*[@id="MissionId"]/option[2]').click()

el_location = driver.find_element_by_xpath('//*[@id="LocationId"]')
el_location.find_element_by_xpath('//*[@id="LocationId"]/option[2]').click()

el_visa_type = driver.find_element_by_xpath('//*[@id="VisaCategoryId"]')
el_visa_type.find_element_by_xpath('//*[@id="VisaCategoryId"]/option[3]').click()

#%%
driver.find_element_by_xpath('//*[@id="btnContinue"]').click()

#%%
driver.save_screenshot('next.png')


#%%


# 添加申请人
driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/a').click()


#%%
el_visa_no = driver.find_element_by_xpath('//*[@id="PassportNumber"]')
el_visa_no.clear()
el_visa_no.send_keys('E234234234')

el_visa_date = driver.find_element_by_xpath('//*[@id="DateOfBirth"]')
el_visa_date.clear()
el_visa_date.send_keys('21121992')

el_visa_date_end = driver.find_element_by_xpath('//*[@id="PassportExpiryDate"]')
el_visa_date_end.clear()
el_visa_date_end.send_keys('21122028')


el_nation_select = driver.find_element_by_xpath('//*[@id="NationalityId"]')
el_nation_select.find_element_by_xpath('//*[@id="NationalityId"]/option[41]').click()


el_name = driver.find_element_by_xpath('//*[@id="FirstName"]')
el_name.clear()
el_name.send_keys('hua')

el_first_name = driver.find_element_by_xpath('//*[@id="LastName"]')
el_first_name.clear()
el_first_name.send_keys('puhui')

el_gender = driver.find_element_by_xpath('//*[@id="GenderId"]')
el_gender.find_element_by_xpath('//*[@id="GenderId"]/option[2]').click()

el_phone_area = driver.find_element_by_xpath('//*[@id="DialCode"]')
el_phone_area.clear()
el_phone_area.send_keys('86')

el_phone = driver.find_element_by_xpath('//*[@id="Mobile"]')
el_phone.clear()
el_phone.send_keys('18825182623')

el_email = driver.find_element_by_xpath('//*[@id="validateEmailId"]')
el_email.clear()
el_email.send_keys('rosirk1@yandex.com')


driver.save_screenshot('next1.png')

#%%


el_submit = driver.find_element_by_xpath('//*[@id="submitbuttonId"]')
el_submit.click()


#%%

driver.save_screenshot('next2.png')
