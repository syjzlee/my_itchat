# encoding: utf-8


import hashlib
import math
import requests
import time
import random
import json
from urllib.parse import quote
from pprint import pprint


def getReqSign(params, appkey='618qt8ksxrNVRBe5469116'):
    data = sorted(params.items())
    _str = ''
    for item in data:
        if item[1] != '':
            _str += item[0] + '=' + quote(str(item[1])) + '&'

    _str += 'app_key=' + appkey
    sign = hashlib.md5(_str.encode('utf-8')).hexdigest().upper()
    return sign


def sendMessage(message: str):
    data = {
        'app_id': 2123126167,
        'time_stamp' : int(time.time()),
        'nonce_str' : str(int(random.random() * math.pow(10, 10))),
        'sign' : '',
        'session' : '10000',
        'question' : message
    }
    data['sign'] = getReqSign(data)
    url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'

    res = requests.get(url, params=data)
    content = json.loads(res.text)
    if content['ret'] == 0:
        answer = content['data']['answer']
        if not answer:
            return '我.....我不知道该怎么回答了...!老爹没教过我这个呀'
        print(data['question'], '====>>', answer)
        return answer
    return -1   # 接口出错了


if __name__ == '__main__':
    sendMessage('我饿了')