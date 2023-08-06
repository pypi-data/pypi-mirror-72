# -*- coding: UTF-8 -*-

#实验效果： PWM输出实验：当前（0.2.0）版本不可用
#接线：使用windows或linux电脑连接一块arduino主板，LED灯接到D6引脚上

import time
from pinpong.pinpong import PinPong,PWM

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

pwm0 = PWM(board,Pin(board,Pin.D6))

while True:
  for i in range(255):
    print(i)
    pwm0.duty(i)
    time.sleep(0.05)
