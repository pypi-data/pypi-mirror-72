import time

class NeoPixel(object):
  def __init__(self, board, pin_obj, num):
    self.pin_obj  = pin_obj
    self.board = board
    self.num = num
    self.__data = [(0,0,0) for i in range(num)]
    self.board.board.set_pin_mode_neo(self.pin_obj.pin)
    self.board.board.neopixel_config(self.pin_obj.pin,self.num)
    time.sleep(0.1)

  def __repr__(self):
    return 'pixel data (%s)' % self.__data
 
  def __getitem__(self, i):
    return self.__data[i]  # 返回data绑定列表中的第i个元素
 
  def __setitem__(self, i, v):
    #print(i,v)
    self.__data[i]=v
    self.board.board.neopixel_write(i,v)

  def write(self , n, r, g, b):
    self.board.board.neopixel_write(n,(r,g,b))

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.neopixel import NeoPixel
------------Pin API使用方法------------
NeoPixel(board, pin_obj, num)
  @board     使用PinPong类构造出来的主板
  @pin_obj   使用Pin类构造出来的对象, 连接灯带的引脚, 可使用Pin.D0-Dx或Pin.A0-Pin.Ax
  @num       连接的灯珠数量
[](i,v): 设置灯珠颜色，用法 np[i]=v
  @i:    灯珠编号，从0开始
  @v:    颜色值，tuple类型(r,g,b) r,g,b取值范围0-255
""")