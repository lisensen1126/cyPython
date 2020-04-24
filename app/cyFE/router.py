# coding:utf8
import hashlib

from . import fe
from app.cyFE.models import feUserList
import time
import requests
import json
import random
import urllib.parse
import http.client
@fe.route('/feUserList')
def feUserList():
    data={'status':'ok','data':[]}
    data['data']=feUserList.query.all()
    return data
@fe.route('/sendVerifyCode1')
def util_sendmsg():
    url = 'https://api.netease.im/sms/sendcode.action'
    post_data = {
        # 要发送的电话号码
        "mobile": "19829681126"
    }
    AppSecret = "98978287960b"
    AppKey = "498aec5b663f5d0d621612dd145aeda3"
    #json类型
    Nonce = str(random.randint(10000, 100000000))#这个字符串时随机的长度不大于128，随便设
    CurTime = str(int((time.time() * 1000)))  #采用时间戳
    content =AppSecret + Nonce + CurTime
    print("headers", Nonce,CurTime)
    CheckSum = hashlib.sha1(content.encode()).hexdigest()  #对上述进行按要求哈希
    print("CheckSum", CheckSum)
    headers = {   #设置请求头
        'AppKey':AppKey,
        'Nonce':Nonce,
        'CurTime':CurTime,
        'CheckSum':CheckSum
    }
    print("headers",headers)
    response = requests.post(url, data=post_data, headers=headers)#发送post请求
    str_result = response.text
    json_result = json.loads(str_result)
    return json_result
@fe.route('/sendVerifyCode2')
def util_sendmsg2():
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    # 下面的参数需要填入自己注册的账号和对应的密码
    params = urllib.parse.urlencode(
        {'account': 'C00380551', 'password': '5fd2cb4011438e0ddcc42d67fea279f8', 'content': '您的验证码是：666666。请不要把验证码泄露给其他人。', 'mobile': '19829681126',
         'format': 'json'})
    print(params)
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request('POST', sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    jsonstr = response_str.decode('utf-8')
    print(json.loads(jsonstr))
    conn.close()