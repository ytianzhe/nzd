#!/usr/bin/python
#-*- coding: utf-8 -*-
import requests
import urllib.parse
import urllib.request
import  json


url2='https://api.weixin.qq.com/sns/oauth2/access_token'
appid='wxbce3138d5425b8f6'
secret=''



def api_func(url,appid,secret,code):
    #print(url,phoneNum,name,content,templId,operation)
    data = urllib.parse.urlencode({'appid':appid,'secret':secret,'code':code,'grant_type':'authorization_code'})
    data = data.encode('utf-8')
    request = urllib.request.Request(url)
    request.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
    f = urllib.request.urlopen(request, data)
    #print(f.read().decode('utf-8'))
    a=f.read().decode('utf-8')
    code=json.loads(a)
    #print(code)
    return code
#api_func(url2,phone,name,contentDemo,templId,operationDemo)

