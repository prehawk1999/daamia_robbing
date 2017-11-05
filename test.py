# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:31:06 2017

@author: prehawk
"""

import requests

url = 'http://trade.damai.cn/multi/trans/submitOrderInfo'


payload = """
{"tid":"9630f054be3febd4e2ca1a6198565a18",
   "orderId":0,"groupId":"906-3-3-2-14",
   "projectId":133854,
   "performId":8995569,
   "deliveryType":1,
   "payKind":1,
   "trader":{"provinceName":"广东",
     "provinceId":"892",
     "cityName":"广州市",
     "cityId":"893",
     "countyName":"天河区",
     "countyId":"897",
     "districtName":"天河区 全境",
     "districtId":"281268",
     "address":"冼村街道广电平云广场B塔15楼",
     "userName":"黄镨卉",
     "mobilePhone":"18825182623",
     "tel":"",
     "prefix":"86"
     },
     "sKULimit":[],
     "frontPivilege":{"groupId":"",
                      "limitBank":0,
                      "privilegeAmount":0,
                      "privilegeId":"",
                      "privilegeName":"",
                      "privilegeType":0,
                      "providerId":"",
                      "usable":0,
                      "flag":false},
                      "insurance":null,
                      "invoice":null,
                      "note":null
                      ,"buyCommodityList":[
                              {"batchID":"8995569","buyNum":1,"cityID":"906","commodityID":11989082}
                              ],
                      "commodityParams":"2|11989082^1^8995569",
                      "payMethod":0,
                      "businessType":"107001",
                      "businessSubType":"2",
                      "sellChannel":"100100010001",
                      "isVerification":"0"
                      }
     
     

     
     """
     
     