import time
import machine
from led import LED

buzzer = machine.Pin(27, machine.Pin.OUT)
buzzer.value(1)
adc32 = machine.ADC(machine.Pin(32))


class WaterSensor:
    @staticmethod
    def run() -> str:
        # if adc32.any():
        #     # print(str(adc32.read()))
        #     pass
        if 0 <= adc32.read() <= 200:
            WaterSensor.water_level_low()
            return "LOW water level"
        elif 200 < adc32.read() < 4000:
            WaterSensor.water_level_normal()
            return "NORMAL water level"
        elif adc32.read() >= 4000:
            WaterSensor.water_level_high()
            return "HIGH water level"

    @staticmethod
    def water_level_high():
        LED.red()
        buzzer.value(0)
        time.sleep(0.15)
        buzzer.value(1)
        time.sleep(0.3)
        buzzer.value(0)
        time.sleep(0.15)
        buzzer.value(1)

    @staticmethod
    def water_level_normal():
        LED.green()

    @staticmethod
    def water_level_low():
        LED.blue()
        buzzer.value(0)
        time.sleep(0.3)
        buzzer.value(1)
        time.sleep(0.5)
