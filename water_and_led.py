import time
import machine

gp_buzzer = 27
buzzer = machine.Pin(gp_buzzer, machine.Pin.OUT)
pwm14 = machine.PWM(machine.Pin(14))
pwm15 = machine.PWM(machine.Pin(15))
pwm16 = machine.PWM(machine.Pin(16))
adc32 = machine.ADC(machine.Pin(32))


class WaterSensor:
    @staticmethod
    def run():
        if adc32.any():
            # print(str(adc32.read()))
            pass
        if 0 <= adc32.read() <= 200:
            pwm14.duty(0)
            pwm15.duty(0)
            pwm16.duty(255)
            buzzer.value(0)
            time.sleep(0.3)
            buzzer.value(1)
            time.sleep(1)
        if 200 < adc32.read() < 400:
            pwm14.duty(0)
            pwm15.duty(255)
            pwm16.duty(0)
        if adc32.read() >= 400:
            pwm14.duty(255)
            pwm15.duty(0)
            pwm16.duty(0)
            buzzer.value(0)
            time.sleep(0.3)
            buzzer.value(1)
            time.sleep(1)
