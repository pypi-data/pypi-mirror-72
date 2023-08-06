# -*- coding: UTF-8 -*-

import time
from pinpong.pinpong import PinPong
from pinpong.libs.rgb1602 import RGB1602

board = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#board = PinPong("uno", "COM16") #windows下指定端口初始化
#board = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

lcd = RGB1602(board)

print("========DFRobot I2C RGB1602 TEST===========")
lcd.set_rgb(0,50,0);                 #set the value of RGB
lcd.set_cursor(0,0)                  #set the value of coordinates
lcd.print("DFRobot")                #display "DFRobot"

lcd.set_cursor(5,1)
lcd.print("chengdu")

lcd.print(3322)
while True:
  time.sleep(1)
  lcd.scroll_left()           #Set the display mode and scroll direction