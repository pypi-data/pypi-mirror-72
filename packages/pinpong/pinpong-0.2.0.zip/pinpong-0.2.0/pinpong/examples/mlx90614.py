# -*- coding: UTF-8 -*-

#实验效果：温度测量实验
#接线：使用windows或linux电脑连接一块arduino主板，按钮接到D8引脚

import time
from pinpong.pinpong import PinPong
from pinpong.libs.dfrobot_mlx90614 import MLX90614

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

ir=MLX90614(board)                           #create ir object,and transmit the i2c object to it

while True:
  print("Object  %s *C"% ir.obj_temp_c())     #print celsius of Object
  print("Object  %s *F"% ir.obj_temp_f())     #print fahrenheit of Object
  print("Ambient %s *C"% ir.env_temp_c())     #print celsius of Ambient
  print("Ambient %s *F"% ir.env_temp_f())     #print fahrenheit of Ambient
  print()
  time.sleep(1)
