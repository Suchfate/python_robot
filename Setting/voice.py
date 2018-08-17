#!usr/bin/ env python
# -*- coding:utf-8 -*-

#语音唤醒LED灯部分

from Setting import model_getvoice
from Setting import model_outvoice
from Setting import  setting
#import RPi.GPIO as GPIO

name = setting.name
def open_GPIO(num,mp3_path):

   # GPIO.setmode(GPIO.BCM)
    #GPIO.setup(num,GPIO.OUT)
   # GPIO.output(num, GPIO.HIGH)
  #  text = ''+str(name)+'，已帮你打开'+str(num)+'号灯'
    #print(text)
    #model_outvoice.get_hecheng_result(text,mp3_path=mp3_path)
   # return text

    return True

def close_GPIO(num,mp3_path):

  #  GPIO.setmode(GPIO.BCM)
   # GPIO.setup(num, GPIO.OUT)
   # GPIO.output(num, GPIO.LOW)
   # text = ''+str(name)+'，已帮你关闭'+str(num)+'号灯'
    #print(text)
   # model_outvoice.get_hecheng_result(text,mp3_path=mp3_path)
    #return  text

    return True
#获得语音识别输出文本，调用GPIO并播放
def voic_body(contect,mp3_path):
    word=''
    if '开启' in contect:
        if '1' in contect or '一' in contect:
            word = open_GPIO(16,mp3_path)
        if '2' in contect or '二' in contect:
            word =open_GPIO(20,mp3_path)
        if '3' in contect or '三' in contect:
            word = open_GPIO(21,mp3_path)
    if '关闭' in contect:
        if '1' in contect or '一' in contect:
            word = close_GPIO(16,mp3_path)
        if '2' in contect or '二' in contect:
            word =close_GPIO(20,mp3_path)
        if '3' in contect or '三' in contect:
            word =close_GPIO(21,mp3_path)
    return word
if __name__ == '__main__':
    text = '开启3号灯'
    path = 'E:\毕设'
    a = voic_body(text,path)
    print(a)