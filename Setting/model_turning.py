#!usr/bin/ env python
# -*- coding:utf-8 -*-

#使用图灵API模拟人工智能机器人
#输入文本str，返回文本list
import requests
import urllib.request
import logging
import urllib.parse
import json
from Setting import setting

Turn_secret = setting.turning_secret
Turn_API_KEY = setting.APP_KEY_turing
City = setting.location_city
Provience = setting.location_province
Street = setting.location_street
Name = setting.name
ID = setting.CUID

def get_html(url):#获取网站信息
    try:
        html = urllib.request.urlopen(url)
        return html.read().decode('utf-8')
    except Exception as e:
        logging.warning('Get_html error: {}'.format(e))
        return ''

def turning_txt(text):
    try:
        url = 'http://www.tuling123.com/openapi/api'
        headers = {"Content-Type": "application/json; charset=utf-8"}
        json_body = {
            'key': Turn_API_KEY,
            'info': text,
            'loc': Provience+City+Street
        }

        json_body = json.dumps(json_body).encode('utf-8')
        req = urllib.request.Request(url, json_body, headers,method='POST')
        responese = urllib.request.urlopen(req, timeout=30)
        result = json.loads(responese.read().decode('utf-8'))
        #print(result)
        #print(type(result))
        if isinstance(result, dict):
            return result

    except Exception as e:
        print('产生故障，感谢使用')
        logging.warning('turning_robot error:{}'.format(e))

def deal_contect(text):

    try:
        contect = []
        dic = turning_txt(text)
        error_dic={
            40001:'参数key错误',
            40002:'请求内容info为空',
            40004:'当天请求次数已使用完',
            40007:'数据格式异常',
        }
        if dic['code'] in error_dic.keys():
            print(error_dic[dic['code']])
            logging.warning(error_dic[dic['intent']['code']])
        else:
            if dic['code'] == 100000:
                txt = dic['text']
                contect.append(txt)
            if dic['code'] == 200000:
                txt = dic['text']
                url = dic['url']
                contect.append(txt)
                contect.append(url)
            if dic['code'] == 302000:
                txt = dic['text']
                contect.append(txt)
                list = dic['list']
                for i in list:
                    article = i['article']
                    source = i['source']
                    icon = i['icon']
                    detailurl = i['detailurl']
                    contect.append('标题：'+article)
                    contect.append('来源：'+source)
                    contect.append('配图：'+icon)
                    contect.append('全文链接：'+detailurl)
            if dic['code'] == 308000:
                txt = dic['text']
                contect.append(txt)
                list = dic['list']
                for i in list:
                    name = i['name']
                    info = i['info']
                    icon = i['icon']
                    detailurl = i['detailurl']
                    contect.append('名称：'+name)
                    contect.append('材料：'+info)
                    contect.append('配图：'+icon)
                    contect.append('全文链接：'+detailurl)
        if  contect :
            logging.info('Turning_txt successed')
            return contect
    except Exception as e:
        print('产生故障，感谢使用')
        logging.warning('turning_contect error:{}'.format(e))




if __name__ == '__main__':
    print(deal_contect('望庐山瀑布'))