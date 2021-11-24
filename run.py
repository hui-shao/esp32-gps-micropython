import time
import machine
from gps_uart import GPS
from oled import OLED
from wifi import WIFI


class Screen:  # todo 完善 5 个屏幕
    def __init__(self):
        self.OL = OLED()
        self.init()

    def show_n(self, _n: int):
        if _n == 0:
            self.s_0()
        elif 0 < _n <= 5:
            self.s_dest(_n)
        else:
            self.init()

    def init(self):
        self.OL.clear()
        self.OL.rect()
        self.OL.text("Hello 1024WJX !", 5, 10)
        self.OL.show()

    def clear(self):
        self.OL.clear()

    def show(self):
        self.OL.show()

    # todo 用变量替换屏幕内容
    def s_0(self):
        self.OL.clear()
        self.OL.rect()
        self.OL.text("21-11-17", 10, 3)
        self.OL.text("08:53:26.000", 10, 13)
        self.OL.text("36°24′0″ N", 10, 23)
        self.OL.text("117°4′54″ E", 10, 33)
        print("s 0")

    def s_dest(self, _i: int):
        _i -= 1  # 数组下标 序号减一
        self.OL.clear()
        self.OL.rect()
        self.OL.text("08:53:26.000", 10, 3)
        self.OL.text("36°24′0″ N", 10, 13)
        self.OL.text("117°4′54″ E", 10, 23)
        self.OL.text("778.376 km 0.00°", 10, 33)
        print("Current: {0}".format(_i + 1))  # for test


def send_data_to_cloud():
    if not IS_WIFI_CONNECTED:
        return False
    pass


def read_target_p_from_pc(_i: int) -> bool:
    """
    获取 PC 下发的 GPS 目的地坐标信息
    输入格式 23.2302 119.5625
    分隔符为空格 纬度在前
    :param _i: 坐标点的序号 从 1开始
    :return: bool
    """
    global destination_arr
    _i -= 1  # 数组下标
    n_ = 1
    while 1:  # 用于限时 60 s
        try:
            str_in_arr = input("请输入目标点经纬度: ").split(" ")
            lat = float(str_in_arr[0])
            lon = float(str_in_arr[1])
            destination_arr[_i] = [lat, lon]
        except IndexError:
            continue
        except ValueError:
            continue
        else:
            return True
        finally:
            time.sleep(1)
            n_ += 1
        if n_ >= 60:
            print("Time Out.")
            return False


# Button
pin0 = machine.Pin(0, machine.Pin.OUT)
pin0.value(1)
pin2 = machine.Pin(2, machine.Pin.OUT)
pin2.value(1)
pin4 = machine.Pin(4, machine.Pin.OUT)
pin4.value(1)

# Class instantiation
G = GPS()
W = WIFI("mmcblk0p7", "66661111")
IS_WIFI_CONNECTED = W.connect()
S = Screen()

# Global vars
n = 0
screen_i = 0  # 用于记录显示第几屏幕
destination_arr = [[0.0 for i in range(2)] for j in range(5)]  # 二维数组 用于存放目标点坐标

while n < 89120:
    # GPS 模块
    GI = G.read(n)
    print()

    # 数据上云
    # todo
    send_data_to_cloud()

    # 按钮 1
    if pin0.value() == 0:
        time.sleep_ms(150)
        if pin0.value() == 0:
            # 按钮 1 事件 todo
            if screen_i > 0:
                screen_i -= 1

    # 按钮 2
    if pin2.value() == 0:
        time.sleep_ms(150)
        if pin2.value() == 0:
            # 按钮 2 事件 todo
            if screen_i < 5:
                screen_i += 1

    # 按钮 3
    if pin4.value() == 0:
        time.sleep_ms(150)
        if pin4.value() == 0:
            # 按钮 3 事件 读入数据
            read_target_p_from_pc(screen_i)

    # Screen
    S.show_n(screen_i)

    time.sleep(0.08)
    n += 1
