# -*- coding: UTF-8 -*-

#实验效果：按键实验
#接线：使用windows或linux电脑连接一块arduino主板，LED灯接到D13引脚, 按钮接到D8引脚

import time
from pinpong.pinpong import PinPong,Pin

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

btn = Pin(board, Pin.D8, Pin.IN)
led = Pin(board, Pin.D13, Pin.OUT)

while True:
  v = btn.value()
  #print(v)
  led.value(v)
  time.sleep(0.1)
