import serial
import time
import traceback

ser = serial.Serial("/dev/ttyAMA0", 9600)


def run():
    line = str(ser.readline())
    print(line)
    if line.startswith("b\'$GPGLL"):
        wei = float(line[1][:2]) + float(line[1][2:]) / 60
        jing = float(line[3][:3]) + float(line[3][3:]) / 60
        print(f"WeiDu: {line[2]} {wei}")
        print(f"JingDu: {line[4]} {jing}")
        time.sleep(1)


if __name__ == "__main__":
    while True:
        try:
            run()
        except ValueError:
            print("[!] Value Error")
            print(traceback.format_exc(3))
            continue
