#!usr/bin/ env python
# -*- coding:utf-8 -*-

import os
import time
from Setting import voice
from Setting import model_getvoice
from tkinter import *
from Setting import model_outvoice
from Setting import model_turning
import logging

path_re = ''#输入录音文件存储路径
path_hecheng =''#输入合成录音输出地址
path_history =''#输入聊天记录存放地址

logging.basicConfig(format='%(asctime)s|PID:%(process)d|%(levelname)s: %(message)s',
                        level=logging.INFO, filename='')#输入日志存储地址


def record(wav_path):
    #os.system('sh ~/work/record.sh '+str(wav_path)+'')#树莓派录音模块
    return True

def down_history(text_list,txt_path):
    path = os.path.join(txt_path, 'his.txt')
    with open(path, 'a', encoding='utf-8') as fh:
        for i in text_list:
            #print(i)
            fh.write(i)
        fh.close()
    time.sleep(1)

def main_body():
    history = []
    t.insert(CURRENT, '机器人：开始录音，为时五秒请说话\n')
    history.append('机器人：开始录音，为时五秒请说话\n')
    t.update()
    record(wav_path=path_re)
    time.sleep(7)

    t.insert(CURRENT, '机器人：请您耐心等待，正在为您识别哟......\n')
    history.append('机器人：请您耐心等待，正在为您识别哟......\n')
    t.update()
    record_text_str = model_getvoice.get_shibie_result(wav_path=path_re)
    t.insert(CURRENT,'我：'+str(record_text_str)+'\n')
    history.append('我：'+str(record_text_str)+'\n')
    t.update()
    voice_text_str = voice.voic_body(record_text_str,mp3_path=path_hecheng)
    if voice_text_str:
       t.insert(CURRENT, '机器人：' + str(voice_text_str) + '\n')
       history.append('机器人：' + str(voice_text_str) + '\n')
       t.update()
    turning_text_list =model_turning.deal_contect(text=record_text_str)
    time.sleep(1)
    if turning_text_list:
        for i in turning_text_list:
            t.insert(CURRENT, '机器人：' + str(i) + '\n')
            history.append('机器人：' + str(i) + '\n')
            t.update()
        if len(turning_text_list) < 20 :
            model_outvoice.get_hecheng_result(turning_text_list[0], mp3_path=path_hecheng)
    t.insert(CURRENT, '机器人：若要继续请点击按钮\n')
    history.append('机器人：若要继续请点击按钮\n')
    t.update()
    down_history(text_list=history,txt_path=path_history)

root = Tk()
root.title('智能生活语音模式识别系统')
root.geometry('600x600')
root.resizable(width=True, height=True)

t = Text()  # 文本框属性
t.pack()

b = Button(text="程序启动：录音", command = main_body,width=100, height=100)  # 按钮属性
b.pack()

root.mainloop()