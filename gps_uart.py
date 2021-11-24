import machine
from gps_info_format import GpsInfo


class GPS:
    def __init__(self, is_print: bool = False):
        self.uart1 = machine.UART(2, baudrate=9600, rx=23, tx=22, timeout=10)
        self.is_print = is_print

    # @staticmethod
    # def print_data(_i: int, _is_recv: bool, _gi, _bin_data: bytes = ""):
    #     print("===========================\n")
    #     print("No." + str(_i))
    #     if _is_recv:
    #         print("\nRaw data:")
    #         print(_bin_data.decode())
    #         print("\nFormatted data:")
    #         print(_gi.DT.date_str + " " + _gi.DT.time_ms_str)
    #         print(_gi.P.position_f_s)
    #     else:
    #         print("\nNo data for read")
    #     print()
    #     print("===========================\n")

    def read(self, _i: int) -> GpsInfo:
        try:
            if self.uart1.any():
                bin_data = self.uart1.read()
                gi = GpsInfo(bin_data.decode())
                # self.print_data(_i, True, gi, bin_data)
            else:
                gi = GpsInfo("null")
                # self.print_data(_i, True, gi)
        except UnicodeError:
            gi = GpsInfo("null")
            # self.print_data(_i, True, gi)
        return gi


if __name__ == '__main__':
    import time

    G = GPS()
    i = 0
    while i < 2048:
        GI = G.read(i)
        time.sleep(1)
        i = i + 1
