import time
import machine
from gps_uart import GPS
from geo_calculate import GeoCal
from oled import OLED
from water_sensor import WaterSensor


# from wifi import WIFI


class Screen:
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
        self.OL.text("Hello 1024WJX !", 5, 30)
        self.OL.show()
        time.sleep(5)

    def clear(self):
        self.OL.clear()

    def show(self):
        self.OL.show()

    def s_0(self):
        self.OL.clear()
        self.OL.rect()
        self.OL.text(GI_1.DT.date_str, 10, 3)
        self.OL.text(GI_1.DT.time_ms_str, 10, 13)
        self.OL.text("{:.5f} {}".format(GI_1.P.position[0], GI_1.P.position_f_s[2]), 10, 23)
        self.OL.text("{:.5f} {}".format(GI_1.P.position[1], GI_1.P.position_f_s[4]), 10, 33)
        self.OL.show()

    def s_dest(self, _i: int):
        _i -= 1  # 数组下标 序号减一
        lat_target = destination_arr[_i][0]
        lon_target = destination_arr[_i][1]
        self.OL.clear()
        self.OL.rect()
        self.OL.text(GI_1.DT.time_ms_str, 10, 3)
        self.OL.text("%.5f N" % lat_target, 10, 13)
        self.OL.text("%.5f E" % lon_target, 10, 23)
        gc = GeoCal(GI_1.P.position[0], GI_1.P.position[1], lat_target, lon_target)
        self.OL.text("{}".format(gc.distance_f_s), 10, 33)
        self.OL.text("{}".format(gc.angle_degree_s), 10, 43)
        self.OL.show()
        # print("Current: {0}".format(_i + 1))  # for test


class GpsInfoDefault:
    """
    用于初始化 GI_1
    """

    class P:
        position = [36.4001209, 117.0817661]  # 默认纬度在前
        position_s = ['A', '36.4001209', 'N', '117.0817661', 'E']
        position_f_s = ['A', '36°24′0″', 'N', '117°4′54″', 'E']

    class DT:
        date_str = "00-00-00"
        time_str = "00:00:00.000"
        time_ms_str = "00:00:00.000"


def send_data_to_pc(_input: str):
    # if not IS_WIFI_CONNECTED:
    #     pass
    # return False
    print(_input)


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
            lat = float(str_in_arr[0])  # 纬度
            lon = float(str_in_arr[1])  # 经度
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
            # print("Time Out.")
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
# W = WIFI("mmcblk0p7", "66661111")
# IS_WIFI_CONNECTED = W.connect()
S = Screen()

# Global vars
n = 0
screen_i = 0  # 用于记录显示第几屏幕
destination_arr = [[0.0 for i in range(2)] for j in range(5)]  # 二维数组 用于存放目标点坐标

while n < 89120:
    # GPS 模块
    GI_1 = GpsInfoDefault  # 初始化 GI_1
    GI_2 = G.read(n)
    if "null" not in GI_2.DT.date_str:
        GI_1 = GI_2
    print()

    # 数据上云
    send_data_to_pc(GI_1.P.position_s)

    # 按钮 1
    if pin0.value() == 0:
        time.sleep_ms(150)
        if pin0.value() == 0:
            if screen_i > 0:
                screen_i -= 1

    # 按钮 2
    if pin2.value() == 0:
        time.sleep_ms(150)
        if pin2.value() == 0:
            if screen_i < 5:
                screen_i += 1

    # 按钮 3
    if pin4.value() == 0:
        time.sleep_ms(150)
        if pin4.value() == 0:
            # 按钮 3 事件 读入数据
            read_target_p_from_pc(screen_i)

    # Screen
    # 显示第 1 - 5 屏内容
    S.show_n(screen_i)

    # WaterSensor
    alarm_info = WaterSensor.run()
    if "NORMAL" not in alarm_info:
        send_data_to_pc("['Alarm'] {}  ['Position'] {}".format(alarm_info, GI_1.P.position_s))

    time.sleep(0.05)
    n += 1
