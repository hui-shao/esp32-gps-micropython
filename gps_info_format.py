# -*-coding:utf-8 -*-
"""
# Author: Hui-Shao
# Description: 用于格式化 GPS 模块(ublox-neo-6m) 串口信息的一个工具
"""


class GpsInfo:
    """
    使用方法: g = GpsInfo(str_in)
    """
    raw_dict = {}

    class P:
        position = ["null"] * 5  # 经纬度 大体格式 ['A', '3640.01209', 'N', '11708.17661', 'E'] A 是有效定位的意思
        position_f = ["null"] * 5  # 以度分秒显示的经纬度(精度低) 大体格式 ['A', '36°24′0″', 'N', '117°4′54″', 'E']

    class DT:
        date_str = "null"
        time_str = "null"
        time_ms_str = "null"

    def __init__(self, _raw_input: str):
        self.raw_dict = self._text_format(_raw_input)
        self._generate(self.raw_dict)  # 调用 generate 函数 提取部分信息保存至类变量中

    @staticmethod
    def _text_format(raw_str_in: str) -> dict:
        """
        用于将从 gps 模块处接收的 str 转为 dict
        :param raw_str_in: 输入字符 多行文本
        :return: dict
        """
        res = dict()
        lines = raw_str_in.splitlines()
        for line in lines:
            if line.startswith("$G"):
                info_arr = line.split(",")
                res.update({info_arr[0]: {}})
                for i in range(1, len(info_arr), 1):
                    res[info_arr[0]].update({str(i): info_arr[i]})
            else:
                continue
        return res

    def _generate(self, _dict: dict) -> None:
        """
        从 _dict 解析数据, 用于给类变量赋值
        :param _dict: gps 信息转换得到的 dict
        :return: None
        """

        def run():
            # 生成 self.P.position
            for i in range(0, 5, 1):
                self.P.position[i] = _dict.get("$GPRMC", {}).get(str(i + 2), "null")
                self.P.position_f[i] = _dict.get("$GPRMC", {}).get(str(i + 2), "null")

            # 生成 self.P.position_f
            if "null" not in self.P.position_f and all(len(j) > 0 for j in self.P.position_f):  # 防止下面的类型转换出错
                for i in range(1, 4, 2):
                    # noinspection PyTypeChecker
                    du = int(float(self.P.position_f[i]) / 100)
                    fen = int((float(self.P.position_f[i]) / 100 - du) * 60)
                    miao = int((((float(self.P.position_f[i]) / 100 - du) * 60 - fen) * 60).__round__(0))
                    self.P.position_f[i] = str(du) + "°" + str(fen) + "′" + str(miao) + "″"

            # 生成 self.DT.xxx
            date = _dict.get("$GPRMC", {}).get("9", "")
            time_ = _dict.get("$GPRMC", {}).get("1", "")
            if len(date) * len(time_) > 0:
                time_ms = time_.split(".")[1] + "0"  # 小数点后默认只有两位, 因此补个0
                time_ = time_.split(".")[0]
                self.DT.date_str = "{}-{}-{}".format(date[4:6], date[2:4], date[0:2])
                self.DT.time_str = "{0}:{1}:{2}".format(time_[0:2], time_[2:4], time_[4:6])
                self.DT.time_ms_str = self.DT.time_str + ".{}".format(time_ms)
            return None

        try:
            run()
        except KeyError:
            print("[!] KeyError")
        except ValueError:
            print("[!] ValueError")
        except IndexError:
            print("[!] IndexError")
        except Exception as e:
            print(e)
        else:
            pass
        return None


if __name__ == '__main__':  # for debug
    f = open("./tests/test.txt", "r", encoding="utf-8")
    info = f.read()
    f.close()
    G = GpsInfo(info)
    print(G.raw_dict)

    # GpsInfo.P
    print(G.P.position)
    print(G.P.position_f)

    # GpsInfo.DT
    print(G.DT.date_str + " " + G.DT.time_ms_str)

    # other
    print("Finished.")
