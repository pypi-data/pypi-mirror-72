# -*- coding: UTF-8 -*-

#实验效果：数码管实验
#接线：使用windows或linux电脑连接一块arduino主板，数码管模块的LATCH接到D8引脚、CLOCK接到D3引脚，DATA接到D9引脚

import time
from pinpong.pinpong import PinPong,Pin,SoftSPI

latchPin = Pin.D8
clockPin = Pin.D3
dataPin = Pin.D9

tab = bytearray([0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0xff])
taf = bytearray([0xA0,0x83,0xa7,0xa1,0x86,0x8e,0xc2,0x8b,0xe6,0xe1,0x89,0xc7,0xaa,0xc8,0xa3,0x8c,0x98,0xce,0x9b,0x87,0xc1,0xe3,0xd5,0xb6,0x91,0xb8]) #a,b,c,d,e,f,g,h,i,j,k,l,o,m,n,o,p,q,r,s,t,u,v,w,x,y,z
tap = bytearray([0xff,0x7f]) #"space", "."

board = PinPong("uno")
#board = PinPong("uno", "COM16")
#board = PinPong("uno", "/dev/ttyACM0")

latch = Pin(board, latchPin, Pin.OUT)
mosi = Pin(board,dataPin, Pin.OUT)
sck = Pin(board,clockPin, Pin.OUT)
spi = SoftSPI(board, sck=sck, mosi=mosi, miso=None)

for v in tab:
  latch.value(0)
  buf = bytearray([v])
  spi.write(buf)
  latch.value(1)
  time.sleep(1)

for v in taf:
  latch.value(0)
  buf = bytearray([v])
  spi.write(buf)
  latch.value(1)
  time.sleep(1)

for v in tap:
  latch.value(0)
  buf = bytearray([v])
  spi.write(buf)
  latch.value(1)
  time.sleep(1)

