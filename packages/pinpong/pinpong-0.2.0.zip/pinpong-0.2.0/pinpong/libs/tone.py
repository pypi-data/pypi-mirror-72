class Tone:
  def __init__(self, board, pin_obj):
    self.pin_obj  = pin_obj
    self.board = board
    self.board.board.set_pin_mode_tone(self.pin_obj.pin)
    self.freq_value = 1000

  def on(self):
    self.board.board.play_tone(self.pin_obj.pin, self.freq_value, 0)

  def off(self):
    self.board.board.play_tone(self.pin_obj.pin, 0, 0)

  def freq(self, v=None):
    if v == None:
      return self.freq_value
    else:
      self.freq_value = v

  def tone(self, freq, duration):
    self.board.board.play_tone(self.pin_obj.pin, freq, duration)

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
from pinpong.libs.tone import Tone
------------Pin API使用方法------------
Tone(board, pin_obj)
  @board 使用PinPong类构造出来的主板
  @pin_obj   使用Pin类构造出来的对象, 发出声音的引脚
on():  打开声音
off(): 关闭声音
freq(v): 设置或获得声音频率
  @v        用户设置的频率值
            不传值  返回当前频率
tone(freq, duration)：播放特定频率固定时间
  @freq     播放的频率
  @duration 播放的时间长度，单位为毫秒，0表示永远播放
    """)