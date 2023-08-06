# -*- coding: UTF-8 -*-

#实验效果：舵机实验
#接线：使用windows或linux电脑连接一块arduino主板，舵机接到D4引脚上

import time
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.servo import Servo

SERVO_PIN = Pin.D12

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

servo1 = Servo(board, Pin(board,SERVO_PIN))

while True:
  servo1.angle(0) #设置舵机转动角度
  time.sleep(1)

  servo1.angle(90)
  time.sleep(1)

  servo1.angle(180)
  time.sleep(1)

  servo1.angle(90)
  time.sleep(1)