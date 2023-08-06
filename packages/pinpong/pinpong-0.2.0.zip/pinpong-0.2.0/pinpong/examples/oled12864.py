# -*- coding: UTF-8 -*-

#实验效果： I2C OLED12864屏幕控制
#接线：使用windows或linux电脑连接一块arduino主板，OLED12864显示屏接到I2C接口

import time
from pinpong.pinpong import PinPong
from pinpong.libs.dfrobot_ssd1306_i2c import SSD1306_I2C #导入ssd1306库

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下制定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下制定端口初始化

oled=SSD1306_I2C(board, 128, 64)


while True:
  oled.fill(1) #全部填充显示
  oled.show()  #显示生效
  time.sleep(1)
  
  oled.fill(0) #全部填充熄灭，清屏
  oled.show()  #显示生效
  time.sleep(1)
  
  oled.text(0) #显示数字
  oled.text("hello pinpong",8,8) #制定位置显示文字
  oled.show()  #显示生效
  time.sleep(2)
