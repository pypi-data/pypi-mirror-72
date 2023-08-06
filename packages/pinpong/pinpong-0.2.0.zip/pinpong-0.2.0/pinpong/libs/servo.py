class Servo:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_servo(self.pin_obj.pin)

  def angle(self, value):
    self.board.board.servo_write(self.pin_obj.pin, value)

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.servo import Servo
------------Pin API使用方法------------
Servo(board, pin_obj)
  @board     使用PinPong类构造出来的主板
  @pin_obj   使用Pin类构造出来的对象，舵机连接到引脚
angle(value): 舵机转动角度
  @value     舵机转动的角度，范围(0-180)
""")
