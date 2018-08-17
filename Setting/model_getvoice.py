#!usr/bin/ env python
# -*- coding:utf-8 -*-

#百度语音识别模块调用，输出文本
#输入语音wav,8000,1 | 输出文本str

import urllib.parse
import urllib.request
from Setting import setting
import json
import logging
import base64

API_ID = setting.APP_ID_baidu
API_Key = setting.API_Key_baidu
API_Secret = setting.Secret_Key_baidu
API_CUID = setting.CUID

framerate = 8000
channels = 1
TIME = 2

def get_html(url):#获取网站信息
    try:
        html = urllib.request.urlopen(url)
        return html.read().decode('utf-8')
    except Exception as e:
        logging.warning('Get_html error: {}'.format(e))
        return ''

def get_file_content(filePath):#打开wav文件
    try:
        with open(filePath+'/record.wav', 'rb') as fp:
            return fp.read()
    except Exception as e:
        logging.warning('Open_wav '+str(filePath)+' error:{}'.format(e))
        return ''

def get_api_token():
    try:
        url = 'https://openapi.baidu.com/oauth/2.0/token?'
        values = {'grant_type': 'client_credentials',
                  'client_id': API_Key,
                  'client_secret': API_Secret,
                  }
        api = url + urllib.parse.urlencode(values)
        #print(api)
        data = get_html(api)
        json_data = json.loads(data)
        token = json_data['access_token']
        logging.info('Get_token successed')
        return token
    except Exception as e:
        logging.warning('Get_token error:{}'.format(e))

def yuyin_shibie(token,wav_path):#需指定获取音频路径
    try:
        url = 'http://vop.baidu.com/server_api'
        re_data = get_file_content(wav_path)
        #print(re_data)
        base64_data = base64.b64encode(re_data).decode('utf-8')
        #print(type(base64_data))
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_body = {
            'format' : 'wav',
            'rate' : 16000,
            'channel' : 1,
            'token': token,
            'cuid': API_CUID,
            'speech': base64_data,
            'len': len(re_data)
        }
        json_body = json.dumps(json_body).encode('utf-8')
        req = urllib.request.Request(url, json_body, headers)
        responese = urllib.request.urlopen(req, timeout=30)
        #print(responese.read().decode('utf-8'))
        #shibie = json.load(responese.read().decode('utf-8'))
        shibie = json.loads(responese.read().decode('utf-8'))
        err_no = shibie['err_no']
        err_msg = shibie['err_msg']
        if err_no != 0:
            print('识别错误：' + str(err_no) + '/' + str(err_msg) + '')
            logging.warning('识别错误：' + str(err_no) + '/' + str(err_msg) + '')
        result = shibie['result'][0]
        #print('我：' + result)
        logging.info('Baidu_shibie successed')
        return result

    except Exception as e:
        print('产生故障，感谢使用')
        logging.warning('Baidu_shibie error:{}'.format(e))

def get_shibie_result(wav_path):
    token = get_api_token()
    contect = yuyin_shibie(token,wav_path)
    return contect

if __name__ == '__main__':
    contect = get_shibie_result('D:/flie/毕设/16k.wav')
    print(contect)