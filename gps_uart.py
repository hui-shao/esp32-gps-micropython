import machine
from gps_info_format import GpsInfo


class GPS:
    def __init__(self):
        self.uart1 = machine.UART(2, baudrate=9600, rx=35, tx=36, timeout=10)

    def read(self, _i: int) -> GpsInfo:
        # self.uart1.write("Test " + str(_i))
        print("===========================\n")
        print("No." + str(_i))
        try:
            if self.uart1.any():
                bin_data = self.uart1.read()
                gi = GpsInfo(bin_data.decode())
                print("\nRaw data:")
                print(bin_data.decode())
                print("\nFormatted data:")
                print(gi.DT.date_str + " " + gi.DT.time_ms_str)
                print(gi.P.position_f)
            else:
                gi = GpsInfo("null")
                # print("\nNo data for read")
        except UnicodeError:
            gi = GpsInfo("null")
        print()
        print("===========================\n")
        return gi


if __name__ == '__main__':
    import time

    G = GPS()
    i = 0
    while i < 2048:
        GI = G.read(i)
        time.sleep(1)
        i = i + 1
