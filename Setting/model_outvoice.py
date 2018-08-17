#!usr/bin/ env python
# -*- coding:utf-8 -*-

#使用百度语音合成API合成语音并保存为MP3格式
#获取文本str，输出音频Mp3

import urllib.request
import urllib.parse
import logging
import  requests
import json
from Setting import setting
import os
#from pydub import AudioSegment

API_ID = setting.APP_ID_baidu
API_Key = setting.API_Key_baidu
API_Secret = setting.Secret_Key_baidu
API_CUID = setting.CUID

framerate = 8000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2

def play_mp3(mp3_path):
    os.system('sh ~/work/record.sh ' + str(mp3_path) + '')
    return True

def get_html(url):#获取网站信息
    try:
        html = urllib.request.urlopen(url)
        return html.read()
    except Exception as e:
        logging.warning('Get_html error: {}'.format(e))
        return ''

def get_api_token():
    try:
        url = 'https://openapi.baidu.com/oauth/2.0/token?'
        values = {'grant_type': 'client_credentials',
                  'client_id': API_Key,
                  'client_secret': API_Secret,
                  }
        api = url + urllib.parse.urlencode(values)
        data = get_html(api)
        json_data = json.loads(data)
        token = json_data['access_token']
        logging.info('Get_token successed')
        return token
    except Exception as e:
        logging.warning('Get_token error:{}'.format(e))


def yuyin_hecheng(text,token,mp3_path):#需指定合成路径
    try:
        url = 'http://tsn.baidu.com/text2audio?'
        headers = {"Content-Type": "application/json; charset=utf-8"}
        #print(token)
        json_body = {'tex': text,
                     'tok': token,
                     'cuid': API_CUID,
                     'token': token,
                     'ctp': '1',
                     'lan': 'zh',
                     }

        api = url + urllib.parse.urlencode(json_body)
        #print(api)
        result = get_html(api)
        #print(result)
        '''''
        json_body = json.dumps(json_body).encode('utf-8')
        req = urllib.request.Request(url, json_body, headers,method='POST')
        responese = urllib.request.urlopen(req, timeout=30)
        result = eval(responese.read().decode('utf-8'))
        '''''
        #print(result)
        if isinstance(result, dict):
            err_no = result['err_no']
            err_msg = result['err_msg']
            logging.warning('合成失败：' + str(err_no) + '/' + str(err_msg) + '')
            print('合成失败：' + str(err_no) + '/' + str(err_msg) + '')
        path = os.path.join(mp3_path,'hecheng.mp3')
        #print(path)
        with open(path, 'wb') as f:
            f.write(result)
        logging.info('Baidu_hecheng successed')
        return path
    except Exception as e:
        print('产生故障，感谢使用')
        logging.warning('Baidu_hecheng error:{}'.format(e))
        return ''


def get_hecheng_result(text,mp3_path):#输入mp3存放地址
    token = get_api_token()
    path = yuyin_hecheng(text,token,mp3_path)
    play_mp3(path)



if __name__ == '__main__':
    path = 'E:\毕设'#测试地址
    contect = ''#测试文本
    print(get_api_token())

'''
def mp3_wav():
    sound = AudioSegment.from_mp3('auido.mp3')
    sound.export("auido.wav", format="wav")
'''