import time

class LCD1602_I2C:
  def __init__(self, board, i2c_addr):
    self.board = board
    self.i2c_addr = i2c_addr
    self.i2c = board.get_i2c_master(0)
    self.buf = bytearray(1)
    self.BK = 0x08
    self.RS = 0x00
    self.E = 0x04
    self.set_cmd(0x33)
    time.sleep(0.005)
    self.send(0x30)
    time.sleep(0.005)
    self.send(0x20)
    time.sleep(0.005)
    self.set_cmd(0x28)
    self.set_cmd(0x0C)
    self.set_cmd(0x06)
    self.set_cmd(0x01)
    self.version='1.0'
    self.x=0
    self.y=0

  def set_reg(self, dat):
      self.buf[0] = dat
      self.i2c.writeto(self.i2c_addr, self.buf)
      time.sleep(0.001)

  def send(self, dat):
    d=dat&0xF0
    d|=self.BK
    d|=self.RS
    self.set_reg(d)
    self.set_reg(d|0x04)
    self.set_reg(d)

  def set_cmd(self, cmd):
    self.RS=0
    self.send(cmd)
    self.send(cmd<<4)

  def set_data(self, dat):
    self.RS=1
    self.send(dat)
    self.send(dat<<4)

  def clear(self):
    self.set_cmd(1)

  def backlight(self, on):
    if on:
      self.BK=0x08
    else:
      self.BK=0
    self.set_cmd(0)

  def display(self, on):
    if on:
      self.set_cmd(0x0C)
    else:
      self.set_cmd(0x08)

  def scroll_left(self):
    self.set_cmd(0x18)

  def scroll_right(self):
    self.set_cmd(0x1C)

  def set_cursor(self, x, y):
    if x >= 16:
      x=16
    if y >= 2:
      y=1

    self.x = x
    self.y = y

  def char(self, ch):
    if ch == 10 or ch == 13:
      self.y = 1-self.y
      self.x = 0
    elif self.x>=0:
      a=0x80
      if self.y>0:
        a=0xC0
      a+=self.x
      self.set_cmd(a)
      self.x += 1
      if self.x == 16:
        self.x = 0
        self.y = 1-self.y
      self.set_data(ch)

  def print(self, s):
    if(isinstance(s,int)):
      s=str(s)
    if len(s)>0:
      self.char(ord(s[0]))
      for i in range(1, len(s)):
        self.char(ord(s[i]))

  @classmethod
  def help(cls):
    print("""
------------用户导入方法------------
from pinpong.pinpong import PinPong
from pinpong.libs.lcd1602_iic import LCD1602_I2C
------------Pin API使用方法------------
LCD1602_I2C(board, i2c_addr)
  @board 使用PinPong类构造出来的主板
  @i2c_addr   液晶的i2c地址
clear(): 清屏
backlight(on): 打开关闭背光
  @on True 打开背光  False 关闭背光
display(on):   打开关闭显示
  @on True 打开显示  False 关闭显示
set_cursor(x, y): 设置光标位置
  @x 光标的x坐标
  @y 光标的y坐标
print(s): 在液晶上显示内容
  @s 显示的内容，可以是字符串，数字等格式
scroll_left():向左滚屏一个字符宽度
scroll_right():向右滚屏一个字符宽度
""")