# coding=utf-8

import sys
import json
import base64
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = '3XRD2yAKTGujI1CrkEUHsz3l'
SECRET_KEY = 'rId3CfMnqeVLIs6GwNNx0bDLaitaxAes'
TEXT_CORRECT_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/ecnet"

# TOKEN start
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

# get token
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()
    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


# call remote http server
def make_request(url, originalText):
    print("---------------------------------------------------")
    print("原始文本：")
    print("    " + originalText)
    print("\n修改意见：")

    response = request(url, json.dumps(
        {
            "text": originalText
        }))

    data = json.loads(response)

    if "error_code" not in data or data["error_code"] == 0:
        correctText = data['item']['correct_query']
        faults = data['item']['vec_fragment']
        print("正确文本：")
        print("    " + correctText)
        print("出错处：")
        print(faults)
        return data['item']
    else:
        # print error response
        return response

    # 防止qps超限
    time.sleep(0.5)


# call remote http server
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except URLError as err:
        print(err)

def in_door(input):
    # 输入
    originalText = input
    # get access token
    token = fetch_token()
    # concat url
    url = TEXT_CORRECT_URL + "?charset=UTF-8&access_token=" + token
    # 纠正文本输出
    suggestion = make_request(url, originalText)
    return suggestion
