# -*- coding: UTF-8 -*-

#实验效果：声调输出实验
#接线：使用windows或linux电脑连接一块arduino主板，蜂鸣器接到D7接口

import time
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.tone import Tone

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

tone = Tone(board, Pin(board,Pin.D7))
tone.freq(200)

#while True:
#  tone.tone(200,500) #播放频率200HZ的声音500ms
#  time.sleep(1)

while True:
  print("freq=",tone.freq())
  tone.on()                 #开启声音输出
  time.sleep(1)
  tone.off()                #关闭声音输出
  time.sleep(1)
  tone.freq(tone.freq()+100) #设置声音频率