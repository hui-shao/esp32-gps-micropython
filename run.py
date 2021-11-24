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


# Button
pin0 = machine.Pin(0, machine.Pin.OUT)
pin0.value(1)
pin2 = machine.Pin(2, machine.Pin.OUT)
pin2.value(1)
# todo 新增一个按钮 用于接收坐标

# Class instantiation
G = GPS()
W = WIFI("mmcblk0p7", "66661111")
IS_WIFI_CONNECTED = W.connect()
S = Screen()

# Global vars
n = 0
screen_i = 0  # 用于记录显示第几屏幕
destination_arr = [[0.00, 0.00] * 5]  # 二维数组 用于存放目标点坐标

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

    # Screen
    S.show_n(screen_i)

    time.sleep(0.08)
    n += 1
