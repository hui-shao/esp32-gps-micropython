# coding=utf-8

import time
from pubsub import send_message
from recv_serial import COM

if __name__ == '__main__':
    com = COM('com3', 115200)
    com.open()
    i = 1
    while True:
        try:
            arr = com.get_data(3).splitlines()
            for s in arr:
                if s.startswith("[\'V"):
                    print("[*] No.{} -> Received V".format(i))
                    i += 1
                elif "null" in s:
                    print("[*] No.{} -> Received null".format(i))
                    i += 1
                elif s.startswith("[\'A"):
                    print("\n[+] No.{} -> Received A".format(i))
                    print(s + "\n")
                    i += 1
                    rc = send_message(s)  # 发送消息
                    time.sleep(1)
                    # 循环太快的话，丢消息
                else:
                    pass
            time.sleep(0.1)
        except KeyboardInterrupt:
            com.close()
            exit(0)
        else:
            continue
