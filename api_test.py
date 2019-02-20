#!/usr/bin/python
#-*- coding: utf-8 -*-
import requests
import urllib.parse
import urllib.request
import  json


url2='http://wcphp172.xinhaimobile.cn/xh_sms/sms/sms_qcloud.php'
phone='18395806960'
name='TgCat'
contentDemo='出来挨打'
templId='32518' #模板id 32518预警模板
operationDemo='onesms'#onesms单条

def api_func(url,phoneNum,name,content,templId,operation):
    #print(url,phoneNum,name,content,templId,operation)
    data = urllib.parse.urlencode({'phone':phoneNum,'name':name,'content':content,'templId':templId,'operation':operation})
    data = data.encode('utf-8')
    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    f = urllib.request.urlopen(request, data)
    #print(f.read().decode('utf-8'))
    a=f.read().decode('utf-8')
    code=json.loads(a)['result']
    print(code)
    return code
#api_func(url2,phone,name,contentDemo,templId,operationDemo)

