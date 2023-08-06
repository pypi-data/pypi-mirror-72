# -*- coding: UTF-8 -*-

import time
from pinpong.pinpong import PinPong
from pinpong.libs.lcd1602_i2c import LCD1602_I2C

uno = PinPong("uno") #初始化，选择板型和端口号，不输入则留空进行自动识别
#uno = PinPong("uno", "COM16") #windows下指定端口初始化
#uno = PinPong("uno", "/dev/ttyACM0") #linux下指定端口初始化

lcd = LCD1602_I2C(uno, 0x20)

print("========DFRobot I2C LCD1602 TEST===========")
lcd.backlight(True)
lcd.clear()
lcd.set_cursor(0,0)                  #set the value of coordinates
lcd.print("helllo\nDFR")                #display "DFRobot"

lcd.set_cursor(5,1)
lcd.print("chengdu")

lcd.print(3322)
while True:
  time.sleep(1)
  lcd.scroll_left()           #Set the display mode and scroll direction
