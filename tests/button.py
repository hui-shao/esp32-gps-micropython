import time
import machine


pin0 = machine.Pin(0, machine.Pin.OUT)
pin0.value(1)
pin2 = machine.Pin(2, machine.Pin.OUT)
pin2.value(1)
i = 0
while True:
    if pin0.value() == 0:
        time.sleep_ms(150)
        if pin0.value() == 0:
            i += 1
            print(str(i) + " Pre")
    if pin2.value() == 0:
        time.sleep_ms(150)
        if pin2.value() == 0:
            i += 1
            print(str(i) + "Next!")
    if i >= 10:
        break
    time.sleep_ms(50)
