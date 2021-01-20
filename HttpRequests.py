import requests
import json

# 进行 Post 操作
def doPost(url, payload, headers={'Content-Type':'application/x-www-form-urlencoded'}):
    request = requests.post(url, data=payload.encode('utf-8'), headers=headers)
    return(request.text)

# 进行 Get 操作
def doGet(url, headers={'Content-Type':'application/x-www-form-urlencoded'}):
    request = requests.get(url, headers=headers)
    return(request.text)
