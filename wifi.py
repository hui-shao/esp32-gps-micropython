import network
import time


# import socket

class WIFI:
    port = 10000  # 端口号
    wlan = None  # wlan
    listenSocket = None  # 套接字

    def __init__(self, _ssid: str, _passwd: str):
        self.ssid = _ssid
        self.passwd = _passwd
        self.status = "[WIFI] No Connection."
        self.ip = "0.0.0.0"

    # 连接WiFi
    def connect(self) -> bool:
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)  # 激活网络
        self.wlan.disconnect()  # 断开WiFi连接
        self.wlan.connect(self.ssid, self.passwd)  # 连接WiFi
        i = 1
        while 1:  # 等待连接
            if self.wlan.ifconfig()[0] == "0.0.0.0":
                time.sleep(1)
                i += 1
            elif i >= 60:
                self.status = "[WIFI] Time Out."
                print(self.status)
                return False
            else:
                self.ip = str(self.wlan.ifconfig()[0])
                self.status = "[WIFI] {}".format(self.ip)
                print(self.status)
                return True

    def disconnect(self):
        self.wlan.disconnect()
        self.status = "[WIFI] Disconnected."


if __name__ == '__main__':
    W = WIFI("mmcblk0p7", "66661111")
    W.connect()
    print(W.status)
