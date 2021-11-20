import time
import machine
from gps_info_format import GpsInfo

uart1 = machine.UART(2, baudrate=9600, rx=13, tx=12, timeout=10)
i = 1
while i <= 1000:
    # uart1.write("Test " + str(i))
    time.sleep(1)
    print("===========================\n")
    print("No." + str(i))
    if uart1.any():
        bin_data = uart1.read()
        G = GpsInfo(bin_data.decode())
        print("\nRaw data:")
        print(bin_data.decode())
        print("\nFormatted data:")
        print(G.DT.date_str + " " + G.DT.time_ms_str)
        print(G.P.position_f)
    else:
        print("\nNo data for read")
    print()
    print("===========================\n")
    i += 1
