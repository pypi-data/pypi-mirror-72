# -*- coding: UTF-8 -*-

#实验效果：灯带实验
#接线：使用windows或linux电脑连接一块arduino主板，WS2812灯带接到A4口


import time
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.neopixel import NeoPixel

NEOPIXEL_PIN = Pin.A4
PIXELS_NUM = 4

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

np = NeoPixel(board, Pin(board,NEOPIXEL_PIN),PIXELS_NUM)

while True:
  np[0] = (0, 255 ,0)
  np[1] = (255, 0, 0)
  np[2] = (0, 0, 255)
  np[3] = (255, 0, 255)
  time.sleep(1)
  np[1] = (0, 255, 0)
  np[2] = (255, 0, 0)
  np[3] = (255, 255, 0)
  np[0] = (0, 0, 255)
  time.sleep(1)
