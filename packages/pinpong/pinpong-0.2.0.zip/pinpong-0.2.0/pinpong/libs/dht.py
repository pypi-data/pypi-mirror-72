import time

class DHT11:
  def __init__(self,board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.type = 11
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)

  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temp_c(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.dht import DHT11
------------Pin API使用方法------------
DTH11(board, pin_obj)
  @board     使用PinPong类构造出来的主板
  @pin_obj   使用Pin类构造出来的对象, 连接DHT11的引脚
temp_c(): 获取温度值，单位为摄氏度
humidity(): 相对湿度值，范围0-100
    """)

class DHT22:
  def __init__(self,board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.type = 22
    self.board.board.set_pin_mode_dht(self.pin_obj.pin, self.type, differential=.01)

  def measure(self):
    self.value = self.board.board.dht_read(self.pin_obj.pin)

  def temp_c(self):
    return self.board.board.dht_read(self.pin_obj.pin)[1]

  def humidity(self):
    return self.board.board.dht_read(self.pin_obj.pin)[0]

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.dht import DHT22
------------Pin API使用方法------------
DTH22(board, pin_obj)
  @board 使用PinPong类构造出来的主板
  @pin_obj 使用Pin类构造出来的对象, 连接DHT22的引脚
temp_c(): 获取温度值，单位为摄氏度
humidity(): 相对湿度值，范围0-100
    """)