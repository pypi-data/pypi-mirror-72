# -*- coding: UTF-8 -*-

#实验效果：温度测量实验
#接线：使用windows或linux电脑连接一块arduino主板，DHT11接到D7引脚，DHT22接到D6引脚

import time
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.dht import DHT11,DHT22

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

dht11 = DHT11(board, Pin(board,Pin.D7))
dht22 = DHT22(board, Pin(board,Pin.D6))

while True:
  temp = dht11.temp_c()
  humi = dht11.humidity()
  print("dht11 temperature=",temp," humidity=",humi)
  
  temp = dht22.temp_c()
  humi = dht22.humidity()
  print("dht22 temperature=",temp," humidity=",humi)
  time.sleep(1)


