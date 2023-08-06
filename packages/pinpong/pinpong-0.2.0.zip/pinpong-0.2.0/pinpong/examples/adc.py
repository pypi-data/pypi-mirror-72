# -*- coding: UTF-8 -*-

#实验效果：电压测量实验
#实验方法：使用windows或linux电脑连接一块arduino主板，测量A0和A1引脚的电压

import time
from pinpong.pinpong import PinPong,Pin,ADC

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

adc0 = ADC(board,Pin(board, Pin.A0))
adc1 = ADC(board,Pin(board, Pin.A1))

while True:
  v = adc0.read()
  print("A0=", v)
  v = adc1.read()
  print("A1=", v)
  time.sleep(0.5)
