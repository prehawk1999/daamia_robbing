# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:51:05 2017

@author: prehawk
"""

"""
MissionId = Australia
CountryId = China
LocationId = [
        Australia Visa Application Centre - Guangzhou
        Australia Visa Application Centre-Beijing
        Australia Visa Application Centre-Chengdu
        Australia Visa Application Centre-Shanghai
]
VisaCategoryId = [
        Biometrics Enrolment
        General Visa
        Work and Holiday Visa
]


"""

def parseMissionLocJson(json, sel):
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
    return sel_id

if __name__ == '__main__':
    
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
    sel_id = parseMissionLocJson(info, sel)
    print(sel_id)