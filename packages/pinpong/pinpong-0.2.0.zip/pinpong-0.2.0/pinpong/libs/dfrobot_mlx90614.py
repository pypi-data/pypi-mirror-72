class MLX90614:
  MLX90614_IIC_ADDR   = (0x5A)
  MLX90614_TA         = (0x06)
  MLX90614_TOBJ1      = (0x07)
  
  def __init__(self, board, i2c_addr=MLX90614_IIC_ADDR):
    self.board = board
    self.i2c_addr = i2c_addr
    self.i2c = board.get_i2c_master(0)

  def obj_temp_c(self):
    return self.__temperature(self.MLX90614_TOBJ1)	#Get celsius temperature of the object 

  def env_temp_c(self):
    return self.__temperature(self.MLX90614_TA)    #Get celsius temperature of the ambient

  def obj_temp_f(self):
    return (self.__temperature(self.MLX90614_TOBJ1) * 9 / 5) + 32  #Get fahrenheit temperature of the object

  def env_temp_f(self):
    return (self.__temperature(self.MLX90614_TA) * 9 / 5) + 32 #Get fahrenheit temperature of the ambient

  def __temperature(self,reg):
    temp = self.__get_reg(reg)*0.02-273.15             #Temperature conversion
    return temp

  def __get_reg(self,reg):
    data = self.i2c.readfrom_mem(self.i2c_addr,reg,3)               #Receive DATA
    result = (data[1]<<8) | data[0]
    return result

  @classmethod
  def help(cls):
    print("""
------------用户导入方法---------------
from pinpong.pinpong import PinPong
from pinpong.libs.dfrobot_mlx90614 import MLX90614
------------Pin API使用方法------------
MLX90614(board, i2c_addr)
  @board      使用PinPong类构造出来的主板
  @i2c_addr   传感器的i2c地址，如果不传入，默认是0x5A

obj_temp_c(): 获取目标温度，单位为摄氏度
env_temp_c(): 获取环境温度，单位为摄氏度
obj_temp_f(): 获取目标温度，单位为华氏度
env_temp_f(): 获取环境温度，单位为华氏度
""")