# -*- coding: UTF-8 -*-

#实验效果：超声波测距实验
#接线：使用windows或linux电脑连接一块arduino主板，URM09超声波模块接到I2C接口上

import time
from pinpong.pinpong import PinPong
from pinpong.libs.dfrobot_urm09 import URM09

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

urm = URM09(board,0x11)
urm.set_mode_range(urm._MEASURE_MODE_AUTOMATIC ,urm._MEASURE_RANG_500)

while True:
  dist = urm.distance_cm() #获取距离，单位厘米（cm）
  temp = urm.temp_c()      #获取温度，单位摄氏度（C）

  print("Temperature is %.2f .c    "%temp)
  print("Distance is %d cm         "%dist)
  time.sleep(0.5)
