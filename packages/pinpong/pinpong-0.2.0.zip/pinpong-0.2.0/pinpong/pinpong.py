# -*- coding: utf-8 -*-

import os
import time
import serial
import platform
import serial.tools.list_ports

from pinpong.base.avrdude import *
from pinpong.base import pymata4

PINPONG_MAJOR=0
PINPONG_MINOR=2
PINPONG_DELTA=0

FIRMATA_MAJOR = 2
FIRMATA_MINOR = 6

gboard = None

def get_pin(board,vpin):
  if board.boardname == "UNO" or board.boardname == "LEONARDO" or board.boardname == "MEGA2560":
    dpin = vpin if vpin<20 else (vpin-100+14) if vpin >= 100 else -1
    apin = vpin-100 if vpin >= 100 else -1
  return dpin,apin

class Pin:
  D0 = 0
  D1 = 1
  D2 = 2
  D3 = 3
  D4 = 4
  D5 = 5
  D6 = 6
  D7 = 7
  D8 = 8
  D9 = 9
  D10 = 10
  D11 = 11
  D12 = 12
  D13 = 13
  D14 = 14
  D15 = 15
  D16 = 16
  D17 = 17
  D18 = 18
  D19 = 19
  D20 = 20
  D21 = 21
  D22 = 22
  D23 = 23
  D24 = 24
  D25 = 25
  D26 = 26
  D27 = 27
  D28 = 28
  D29 = 29
  D30 = 30
  D31 = 31
  D32 = 32
  D33 = 33
  D34 = 34
  D35 = 35
  D36 = 36
  D37 = 37
  D38 = 38
  D39 = 39
  D40 = 40
  D41 = 41
  D42 = 42
  D43 = 43
  D44 = 44
  D45 = 45
  D46 = 46
  D47 = 47
  D48 = 48
  D49 = 49
  D50 = 50
  D51 = 51
  D52 = 52
  
  A0 = 100
  A1 = 101
  A2 = 102
  A3 = 103
  A4 = 104
  A5 = 105
  
  IN = 1
  OUT = 3
  IRQ_FALLING = 2
  IRQ_RISING = 1
  IRQ_DRAIN = 7
  PULL_DOWN = 1
  PULL_UP = 2

  def __init__(self, board, vpin, mode=None):
    self.board = board
    if(vpin == None):
      self.pin = None
      return
    self.pin,self.apin = get_pin(self.board, vpin)
    self.mode = mode
    if(mode == self.OUT):
      self.board.board.set_pin_mode_digital_output(self.pin)
    elif(mode == self.IN):
      self.board.board.set_pin_mode_digital_input(self.pin, callback=None)

  def value(self, v = -1):
    if v == -1:
      if self.mode == self.OUT:
        return self.val
      else:
        if(self.pin == None):
          return
        self.v = self.board.board.digital_read(self.pin)
        return self.v
    else:
      self.val = v
      if(self.pin == None):
        return
      self.board.board.digital_pin_write(self.pin, v)
      time.sleep(0.001)

  def on(self):
    self.val = 1
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, 1)

  def off(self):
    self.val = 0
    if(self.pin == None):
      return
    self.board.board.digital_pin_write(self.pin, 0)
  
  def irq(self, trigger, handler):
    self.board.board.set_pin_mode_digital_input(self.pin, handler)
    self.board.board.set_digital_pin_params(self.pin, trigger, handler)
  
  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin
------------Pin API使用方法------------
Pin(board, pin, mode)
  @board 使用PinPong类构造出来的主板
  @pin   Pin.D0-Pin.Dx 或 Pin.A0-Pin.Ax
  @mode  Pin.IN Pin.OUT Pin.PULL_UP Pin.PULL_DOWN
value(v): 设置或读取引脚电平
  @v:    0 输出低电平，1 输出高电平
         不传值  输入模式下读取引脚电平
on(): 输出高电平
off(): 输出低电平
irq(trigger, handler):将引脚设置为中断模式
  @trigger   IRQ_RISING 上升沿触发 IRQ_FALLING 下降沿触发
  @handler   中断被触发后的回调函数
""")
    return

class ADC:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_analog_input(self.pin_obj.apin, None)

  def read(self):
    return self.board.board.analog_read(self.pin_obj.apin)
  
  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,ADC,Pin
------------Pin API使用方法------------
ADC(board, pin_obj)
  @board     使用PinPong类构造出来的主板
  @pin_obj   使用Pin类构造出来的对象,只能使用Pin.A0-Pin.Ax
read(): 读取引脚电平，范围（0-1024）
""")

class PWM:
  def __init__(self, board, pin_obj):
    self.board = board
    self.pin_obj = pin_obj
    self.board.board.set_pin_mode_pwm_output(self.pin_obj.pin)
    self.freq_value = 0
    self.duty_value = 0

  def freq(self, v=-1):
    if v == -1:
      return self.freq_value
    else:
      self.freq_value = v
      #self.board.board.pwm_write(self.pin_obj.pin, self.freq_value)

  def duty(self, v=-1):
    if v == -1:
      return self.duty_value
    else:
      self.duty_value = v
      self.board.board.pwm_write(self.pin_obj.pin, self.duty_value)

  def deinit(self):
    self.board.board.set_pin_mode_digital_input(self.pin_obj.pin, callback=None)

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,PWM,Pin
------------Pin API使用方法------------
PWM(board, pin_obj)
  @board    使用PinPong类构造出来的主板
  @pin_obj  使用Pin类构造出来的对象
freq(v): 设置pwm频率
  @v:       用户设置的频率值
            不传值  返回当前频率
duty(v): 设置pwm占空比
  @v:        用户设置的占空比 范围 0-100
             不传值  返回当前占空比
deinit(): 取消次引脚PWM功能
    """)

class SoftSPI:
  # spi四种模式SPI的相位(CPHA)和极性(CPOL)分别可以为0或1，对应的4种组合构成了SPI的4种模式(mode)
  # Mode 0 CPOL=0, CPHA=0  -> 第一个跳变，即上升沿采样
  # Mode 1 CPOL=0, CPHA=1  -> 第二个跳变，即下降沿采样
  # Mode 2 CPOL=1, CPHA=0  -> 第一个跳变，即下降沿采样
  # Mode 3 CPOL=1, CPHA=1  -> 第二个跳变，即上升沿采样
  # 时钟极性CPOL: 即SPI空闲时，时钟信号SCLK的电平（1:空闲时高电平; 0:空闲时低电平）
  # 时钟相位CPHA: 即SPI在SCLK第几个边沿开始采样（0:第一个边沿开始; 1:第二个边沿开始）
  # 默认设置为MODE 0 因为大部分的外设使用的是MODE 0
  def __init__(self, board, sck, mosi, miso, baudrate=100000, polarity=0, phase=0, bits=8):
    self.board = board
    self.mosi = mosi
    self.miso = miso
    self.sck = sck
    self.phase = phase
    self.mosi.value(0)
    self.sck.value(polarity)

  def read(self, num, default_value=0xff):
    ret = bytearray(num)
    for i in range (num):
      ret[i] = self._transfer(default_value)
    return ret

  def readinto(self, buf):
    num = len(buf)
    buf=self.read(num)

  def write(self, buf): #write some bytes on MOSI
    num = len(buf)
    for i in range (num):
      self._transfer(buf[i])

  def write_readinto(self, wbuf, rbuf): # write to MOSI and read from MISO into the buffer
    num = len(wbuf)
    for i in range (num):
      rbuf[i] = self._transfer(wbuf[i])

  def _transfer(self,data):
    ret = 0
    for i in range(8):
      self.mosi.value(1 if data&0x80 else 0)
      self.sck.value(0 if self.sck.value() else 1) #这样书写兼容了MODE0 和 MODE3
      self.sck.value(0 if self.sck.value() else 1)
      if self.miso:
        ret= ret<<1 + self.miso.value()
      data <<= 1
    return ret

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong,Pin,SoftSPI
------------Pin API使用方法------------
SoftSPI(self, board, baudrate, polarity, phase, bits, sck, mosi, miso)
  @board      使用PinPong类构造出来的主板
  @baudrate   使用Pin类构造出来的对象
  @polarity   空闲时clk引脚的电平
  @phase      SPI在SCLK第几个边沿开始采样（0:第一个边沿开始; 1:第二个边沿开始）
  @bits       默认传输8 bits，不可更改
  @sck        Pin对象，时钟引脚
  @mosi       Pin对象，数据输出引脚
  @miso       Pin对象，数据输入引脚

read(num, default_value=0xff): 读取num个数据
  @num:           读取的数据字节数
  @default_value  读过过程中发送过去的值，不填写默认发送0xff
readinto(buf): 从spi总线读取数据到buf中
  @buf:           bytearray格式的缓冲，读取数据字节长度为buf的长度
write(buf): 将buf中的数据写入到spi总线
write_readinto(wbuf, rbuf): 将wbuf中的数据写入spi总线，同时从spi总线读取数据到rbuf，两个buf长度相等
  @wbuf           bytearray格式的缓冲，写入wbuf的长度的数据字节
  @rbuf           bytearray格式的缓冲，读取rbuf的长度的数据字节
    """)

class IIC:
  def __init__(self, board, bus_num=0):
    self.bus_num = bus_num
    self.board = board

  def scan(self):
    return []

  def writeto(self, i2c_addr, value):
    self.board.board.i2c_write(i2c_addr, value)

  def readfrom(self, i2c_addr, read_byte):
    pass

  def readfrom_mem(self, i2c_addr, reg, read_byte):
    return self.board.board.i2c_read(i2c_addr, reg, read_byte, None)

  def writeto_mem(self, i2c_addr, reg, value):
    self.board.board.i2c_write(i2c_addr, [reg]+list(value))

class PinPong:
  def __init__(self, boardname="", port=None):
    global gboard
    self.boardname = boardname.upper()
    self.port = port
    self._i2c_init = [False,False,False,False,False]
    self.i2c = [None, None, None, None, None]
    gboard = self
    name = platform.platform()
    if self.port == None:
      if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
        self.port="/dev/ttyS1"
    self.connected = False
    self.connect()

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong
------------Pin API使用方法------------
PinPong(boardname, port)
  @boardname   主板名称，当前支持uno leonardo mega2560
  @port        串口名字，不填写系统会自动选择合适的端口
get_i2c_master(bus_num) : 获取I2C主机控制器
  @bus_num     I2C主机控制器编号
""")

  def printlogo(self):
    print("""
  __________________________________________
 |    ____  _       ____                    |
 |   / __ \(_)___  / __ \____  ____  ____ _ |
 |  / /_/ / / __ \/ /_/ / __ \/ __ \/ __ `/ |
 | / ____/ / / / / ____/ /_/ / / / / /_/ /  |
 |/_/   /_/_/ /_/_/    \____/_/ /_/\__, /   |
 |   v%d.%d.%d  Designed by DFRobot  /____/    |
 |__________________________________________|
 """%(PINPONG_MAJOR,PINPONG_MINOR,PINPONG_DELTA))
    import sys
    version = sys.version.split(' ')[0]
    plat = platform.platform()
    print("[01] Python"+version+" "+plat+" Board: "+self.boardname)
  def connect(self):
    if self.connected:
      return
    self.printlogo()
    major,minor = self.detect_firmata()
    print("[32] Firmata ID: %d.%d"%(major,minor))
    if major != FIRMATA_MAJOR or minor != FIRMATA_MINOR:
      print("[35] Burning firmware...")
      cwdpath,_ = os.path.split(os.path.realpath(__file__))
      pgm = Burner(self.boardname,self.port)
      if(self.boardname == "UNO"):
        name = platform.platform()
        if name.find("Linux_vvBoard_OS")>=0 or name.find("Linux-4.4.159-aarch64-with-Ubuntu-16.04-xenial")>=0:
          cmd = "/home/scope/software/avrdude-6.3/avrdude -C/home/scope/software/avrdude-6.3/avrdude.conf -v -patmega328p -carduino -P"+self.port+" -b115200 -D -Uflash:w:"+cwdpath + "/base/FirmataExpress.Uno."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex"+":i"
          os.system(cmd)
        else:
          pgm.burn(cwdpath + "/base/FirmataExpress.Uno."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == "LEONARDO"):
        port_list_0 = list(serial.tools.list_ports.comports())
        port_list_2 = port_list_0 = [list(x) for x in port_list_0]
        ser = serial.Serial(self.port,1200,timeout=1)
        ser.close()

        retry = 5
        port = None
        while retry:
          retry = retry - 1
          port_list_2 = list(serial.tools.list_ports.comports())
          port_list_2 = [list(x) for x in port_list_2]
          for p in port_list_2:
            if p not in port_list_0:
              port = p
              break
          if port == None:
            time.sleep(0.5)
          if port:
            print("port=====",port)
            break
        pgm = Burner(self.boardname,port[0])
        pgm.burn(cwdpath + "/base/FirmataExpress.Leonardo."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      elif(self.boardname == 'MEGA2560'):
        pgm.burn(cwdpath + "/base/FirmataExpress.MEGA2560."+str(FIRMATA_MAJOR)+"."+str(FIRMATA_MINOR)+".hex")
      print("[37] Burn done")
    time.sleep(2)
    self.board = pymata4.Pymata4(com_port=self.port, baud_rate=115200)
    self.connected = True
    return True
  '''
  Uno:
  ['COM99', 'Arduino Uno (COM99)', 'USB VID:PID=2341:0043 SER=5573932393735151F0C1 LOCATION=1-10']
  ['/dev/ttyACM0', 'ttyACM0', 'USB VID:PID=2341:0043 SER=5573932393735151F0C1 LOCATION=1-2:1.0']
  Leonardo:
  ['COM18', 'Arduino Leonardo (COM18)', 'USB VID:PID=2341:8036 SER=6 LOCATION=1-10.10:x.0']
  ['/dev/ttyACM1', 'Arduino Leonardo', 'USB VID:PID=2341:8036 LOCATION=1-10:1.0']
  MEGA2560:
  ['COM7', 'Arduino Mega 2560 (COM7)', 'USB VID:PID=2341:0042 SER=556393132333512141A2 LOCATION=1-10']
  ['/dev/ttyACM0', 'ttyACM0', 'USB VID:PID=2341:0042 SER=556393132333512141A2 LOCATION=1-2:1.0']
  '''
  def detect_firmata(self):
    vidpid={
    "UNO":"2341:0043",
    "LEONARDO":"2341:8036",
    "MEGA2560":"2341:0042"
    }
    portlist=[]
    localportlist=[]
    if self.boardname == "":
      print("Using local resources")
      return (-1,-1)
    elif self.port == None:
      plist = list(serial.tools.list_ports.comports())
      for port in plist:
        msg = list(port)
        if msg[2].find(vidpid[self.boardname]) > 0:
          portlist.insert(0,msg)
        elif msg[2].find("LOCATION") > 0:
          portlist.append(msg)
        else:
          localportlist.append(msg)
        portlist += localportlist
      if len(portlist) > 0:
        self.port = portlist[0][0]
        print("Automatically selected -> ",self.port)
    print("[10] Opening "+self.port)
    ser=serial.Serial(self.port, 115200, timeout=3)
    if(self.boardname == "UNO" or self.boardname == "MEGA2560"):
      time.sleep(3)
    ser.read(ser.in_waiting)
    buf=bytearray(b"\xf0\x79\xf7")
    ser.write(buf)
    res = ser.read(10)
    if len(res) < 3:
      major=0
      minor=0
    elif res[0] == 0xF9:
      major = res[1]
      minor = res[2]
    elif res[0] == 0xF0 and res[1] == 0x79:
      major = res[2]
      minor = res[3]
    else:
      major=0
      minor=0
    ser.close()
    print("[15] Close "+self.port)
    return major,minor

  def get_i2c_master(self,bus_num=0):
    if not self._i2c_init[bus_num]:
      self.board.set_pin_mode_i2c()
      self._i2c_init[bus_num] = True
      self.i2c[bus_num] = IIC(self)
    return self.i2c[bus_num]
