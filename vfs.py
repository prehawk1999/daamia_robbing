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
import json
import time

def parseMissionLocJson(json, sel):
    sel_id = {}

    for i in json:
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
                
                sel_id['LocationId'] = l['Id']
                
                for v in l['VisaCategories']:
                    if not v['Name'].startswith(sel['VisaCategoryId']):
                        continue
                    
                    sel_id['VisaCategoryId']  = v['Id']
    return sel_id


def parseGetCalendarDaysJson(info, sel):
    realJson = json.loads(info['CalendarDatesOnViewChange'])
    
    dateTimeBandMap = {}
    for d in realJson:
        if len(d['TimeBands']) == 0:
            continue
        dateTimeBandMap[d['Date']] = d['TimeBands']
 
    for exp in sel['Expects']:
        print(exp)
        if exp['Date'] not in dateTimeBandMap:
            continue
        
        if exp['Early'] is None:
            exp['Early'] = "7:00"
        if exp['Late'] is None:
            exp['Late'] = "18:00"
    
        early = time.strptime(exp['Early'], '%H:%M')
        late = time.strptime(exp['Late'], '%H:%M')
        
        for t in dateTimeBandMap[exp['Date']]:
            if t['RemainingSlots'] < 1:
                continue
            curr = time.strptime(t['StartTime'], '%H:%M')
            if curr >= early and curr <= late:
                print("[VFS] - select date: ", exp['Date'])
                print("[VFS] - select time: ", t['StartTime'])
                print("[VFS] - select band: ", t['AllocationId'])
                return t['AllocationId']
    pass
    
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
    
    f = open('data/GetCalendarDaysOnViewChange.json')
    info = json.loads(f.read())
    
    sel = {
            "Expects": 
                [
                    {
                            "Date" : "12/27/2017",            
                            "Early": "8:00",
                            "Late": "8:15"
                    },
                    {
                            "Date" : "12/18/2017",            
                            "Early": "8:00",
                            "Late": "8:30"
                    }
                ]
            }
    
    sel_id = parseGetCalendarDaysJson(info, sel)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    