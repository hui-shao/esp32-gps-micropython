import time
import machine

buzzer = machine.Pin(27, machine.Pin.OUT)
buzzer.value(1)
pwm14 = machine.PWM(machine.Pin(14))
pwm15 = machine.PWM(machine.Pin(15))
pwm16 = machine.PWM(machine.Pin(16))
adc32 = machine.ADC(machine.Pin(32))


class WaterSensor:
    @staticmethod
    def run():
        # if adc32.any():
        #     # print(str(adc32.read()))
        #     pass
        if 0 <= adc32.read() <= 200:
            WaterSensor.led_blue()
            buzzer.value(0)
            time.sleep(0.3)
            buzzer.value(1)
        elif 200 < adc32.read() < 3750:
            WaterSensor.led_green()
        elif adc32.read() >= 3750:
            WaterSensor.led_red()
            buzzer.value(0)
            time.sleep(0.3)
            buzzer.value(1)

    @staticmethod
    def led_red():
        pwm14.duty(255)
        pwm15.duty(0)
        pwm16.duty(0)

    @staticmethod
    def led_green():
        pwm14.duty(0)
        pwm15.duty(255)
        pwm16.duty(0)

    @staticmethod
    def led_blue():
        pwm14.duty(0)
        pwm15.duty(0)
        pwm16.duty(255)
