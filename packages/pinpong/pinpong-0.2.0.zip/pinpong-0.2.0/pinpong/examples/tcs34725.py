# -*- coding: UTF-8 -*-
#实验效果：颜色读取实验
#接线：使用windows或linux电脑连接一块arduino主板，TCS34725接到I2C接口

import time

from pinpong.pinpong import PinPong
from pinpong.libs.dfrobot_tcs34725 import TCS34725

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

tcs = TCS34725(board)

print("Color View Test!");
while True:
  if tcs.begin():
    print("Found sensor")
    break  #找到传感器，初始化成功，跳出循环
  else:
    print("No TCS34725 found ... check your connections")
    time.sleep(1)

while True:
  r,g,b,c = tcs.get_rgbc()
  print(r,g,b,c)
  print("C=%d\tR=%d\tG=%d\tB=%d\t"%(c,r,g,b))
  
  '''
  r /= c
  g /= c
  b /= c
  r *= 256
  g *= 256
  b *= 256;
  print("------C=%d\tR=%d\tG=%d\tB=%d\t"%(c,r,g,b))
  '''
  time.sleep(1)