# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:31:06 2017

@author: prehawk
"""

import json
import codecs
from bs4 import BeautifulSoup


f = codecs.open('data/vac.html', 'r', 'utf8')
html = f.read()
f.close()

soup = BeautifulSoup(html, 'lxml')
infoJson = soup.find(id='MissionCountryLocationJSON')
info = json.loads(infoJson.attrs['value'])

sel = {
                'MissionId': 'Australia',
                'CountryId': 'China',
                'LocationId': 'Australia Visa Application Centre-Chengdu',
                'VisaCategoryId': 'Work and Holiday Visa',
                }


sel_id = {}


for i in info:
    if not i['Name'].startswith(sel['MissionId']):
        continue
    
    sel_id['MissionId'] = i['Id']
    for c in i['CountryJEs']:
        if not c['Name'].startswith(sel['CountryId']):
            continue
        
        sel_id['CountryId']= c['Id']
        
        for l in c['Locations']:
            if not l['Name'].startswith(sel['LocationId']):
                continue
            
            sel_id['LocaltionId'] = l['Id']
            
            for v in l['VisaCategories']:
                if not v['Name'].startswith(sel['VisaCategoryId']):
                    continue
                
                sel_id['VisaCategoryId']  = v['Id']
                
                
if len(sel_id) == 4:
    print('succ!', sel_id)
else:
    print('failed!', sel_id)
        