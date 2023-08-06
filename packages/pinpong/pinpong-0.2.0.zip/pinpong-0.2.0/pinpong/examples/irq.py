# -*- coding: UTF-8 -*-

#实验效果：中断实验
#接线：使用windows或linux电脑连接一块arduino主板，按钮接到D8引脚

import time
from pinpong.pinpong import PinPong,Pin

uno = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#uno = PinPong("uno", "COM16") #windows下指定端口初始化
#uno = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

btn = Pin(uno, Pin.D8, Pin.IN)

def btn_handler(data):
  print("\n-----")
  print("pin_mode = ", data[0])
  print("pin = ", data[1])
  print("value = ", data[2])

#btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_handler)
btn.irq(trigger=Pin.IRQ_RISING, handler=btn_handler)
#btn.irq(trigger=Pin.IRQ_RISING+Pin.IRQ_FALLING, handler=btn_handler)

while True:
  time.sleep(1)
