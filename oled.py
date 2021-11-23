from machine import I2C, Pin
from ssd1306 import SSD1306_I2C


class OLED:
    i2c = I2C(scl=Pin(21), sda=Pin(22), freq=10000)  # 软件I2C
    oled = SSD1306_I2C(128, 64, i2c)  # 创建oled对象

    def __init__(self):
        pass

    def show(self):
        self.oled.show()

    def clear(self):
        self.oled.fill(0)  # 清空屏幕

    def text(self, _text_in: str, _line: int, _row: int):
        """
        打印文字
        :param _text_in:
        :param _line: 列
        :param _row: 行
        :return:
        """
        self.oled.text(_text_in, _line, _row)

    def rect(self):
        self.oled.rect(0, 0, 127, 63, 1)
