import machine

pwm14 = machine.PWM(machine.Pin(14))
pwm15 = machine.PWM(machine.Pin(15))
pwm16 = machine.PWM(machine.Pin(16))


class LED:
    @staticmethod
    def red():
        pwm14.duty(255)
        pwm15.duty(0)
        pwm16.duty(0)

    @staticmethod
    def green():
        pwm14.duty(0)
        pwm15.duty(255)
        pwm16.duty(0)

    @staticmethod
    def blue():
        pwm14.duty(0)
        pwm15.duty(0)
        pwm16.duty(255)
