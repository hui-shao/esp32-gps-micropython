class GeoCal:
    def __init__(self, lat1: float, lon1: float, lat2: float, lon2: float):
        self.distance = 0.0  # 单位为 km
        self.distance_f_s = "0.0 m"
        self.angle_rad = 0.0  # angle 指的是航向角
        self.angle_rad_s = "0.00 rad"
        self.angle_degree = 0.0
        self.angle_degree_s = "0.00 "
        self._cal_geo_distance_and_angle(lat1, lon1, lat2, lon2)
        self._format_data()

    def _cal_geo_distance_and_angle(self, _lat1: float, _lon1: float, _lat2: float, _lon2: float) -> None:
        from math import radians, tan, sin, cos, asin, atan2, sqrt, log, pi, degrees
        _lon1, _lat1, _lon2, _lat2 = map(radians, map(float, [_lon1, _lat1, _lon2, _lat2]))

        # 计算距离
        d_lon = _lon2 - _lon1
        d_lat = _lat2 - _lat1
        a = sin(d_lat / 2) ** 2 + cos(_lat1) * cos(_lat2) * sin(d_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371
        self.distance = c * r

        # 计算航向角度
        delta_fi = log(tan(_lat2 / 2 + pi / 4) / tan(_lat1 / 2 + pi / 4))
        delta_lon = abs(_lon1 - _lon2) % 180
        if _lon1 <= _lon2:
            theta = atan2(delta_lon, delta_fi)
        else:
            theta = 2 * pi - atan2(delta_lon, delta_fi)
        self.angle_rad = theta
        self.angle_degree = degrees(theta)
        return None

    def _format_data(self):
        if self.distance <= 1:
            self.distance_f_s = "%.3f m" % (self.distance * 1000)
        else:
            self.distance_f_s = "%.3f km" % self.distance
        # 转换为角度 str
        self.angle_degree_s = "%.2f" % self.angle_degree
        self.angle_rad_s = "%.2f rad" % self.angle_rad
        return None


if __name__ == '__main__':
    D = GeoCal(42.0123, 113.1038, 49.0124, 113.1037)
    print(D.distance)
    print(D.distance_f_s)
    print(D.angle_rad)
    print(D.angle_degree)
    print(D.angle_degree_s)
