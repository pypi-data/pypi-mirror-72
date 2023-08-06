import time
from pinpong.pinpong import *

class SR04_URM10:
  def __init__(self,board,trigger_pin_obj, echo_pin_obj):
    self.board  = board
    self.trigger_pin_obj = trigger_pin_obj
    self.echo_pin_obj = echo_pin_obj
    self.board.board.set_pin_mode_sonar(self.trigger_pin_obj.pin, self.echo_pin_obj.pin)

  def distance_cm(self):
    return self.board.board.sonar_read(self.trigger_pin_obj.pin)[0]

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.sr04_urm10 import SR04_URM10
------------Pin API使用方法------------
SR04_URM10(board, trigger_pin_obj, echo_pin_obj)
  @board             使用PinPong类构造出来的主板
  @trigger_pin_obj   使用Pin类构造出来的对象, 触发测量引脚
  @echo_pin_obj      使用Pin类构造出来的对象, 接收反馈引脚
distance_cm(): 读取超声波距离，单位为厘米
    """)