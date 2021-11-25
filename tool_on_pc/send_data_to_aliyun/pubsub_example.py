# 注意 使用时 请重命名本模块为 pubsub.py
# 并填写相应参数

import hmac
import base64
from hashlib import sha1
import time
from mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from mqtt import client as mqtt


class AliyunMQTT(object):

    def __init__(self):
        # 实例 ID，购买后从产品控制台获取
        self.instanceId = ''
        # 账号AccessKey 从阿里云账号控制台获取
        self.accessKey = ''
        # 账号secretKey 从阿里云账号控制台获取
        self.secretKey = ''
        # MQTT GroupID,创建实例后从 MQTT 控制台创建
        self.groupId = ''
        # MQTT ClientID，由 GroupID 和后缀组成，需要保证全局唯一
        self.client_id = ''
        # Topic， 其中第一级父级 Topic 需要从控制台创建
        self.topic = ''
        # MQTT 接入点域名，实例初始化之后从控制台获取
        self.brokerUrl = ''

        self.client = mqtt.Client(self.client_id, protocol=mqtt.MQTTv311, clean_session=False)
        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        # username和 Password 签名模式下的设置方法，
        # 参考文档 https://help.aliyun.com/document_detail/48271.html?spm=a2c4g.11186623.6.553.217831c3BSFry7
        userName = 'Signature' + '|' + self.accessKey + '|' + self.instanceId
        password = base64.b64encode(hmac.new(self.secretKey.encode(), self.client_id.encode(), sha1).digest()).decode()
        # password = 'Jr4lJqFmb5gyxXdwU1sJGrJyVN0'
        self.client.username_pw_set(userName, password)
        self.client.connect(self.brokerUrl, 1883, 60)
        # 这个loop不能启用，否则阻塞进程
        # self.client.loop_forever()

    def on_log(self, userdata, level, buf):
        if level == MQTT_LOG_INFO:
            head = 'INFO'
        elif level == MQTT_LOG_NOTICE:
            head = 'NOTICE'
        elif level == MQTT_LOG_WARNING:
            head = 'WARN'
        elif level == MQTT_LOG_ERR:
            head = 'ERR'
        elif level == MQTT_LOG_DEBUG:
            head = 'DEBUG'
        else:
            head = level

        print('%s: %s' % (head, buf))

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        # 一旦连接，就订阅自己发送的消息的toppic；为了测试使用，但是没调试好，可以注释掉
        client.subscribe(self.topic, 0)

    def on_message(self, client, userdata, msg):
        # 当客户端收到消息是，干什么
        print(msg.topic + ' ' + str(msg.payload))

    def on_disconnect(self, client, userdata, rc):
        # 当客户端失去连接时
        if rc != 0:
            print('Unexpected disconnection %s' % rc)

    def put_message_into_queue(self, message):
        # 实际调用mqtt客户端发送消息
        rc = self.client.publish(self.topic, message, qos=0)
        print('rc: %s' % rc)
        # time.sleep(0.1)
        return rc


# 初始化一个mqtt消息的类
aliyunMQTTUtil = AliyunMQTT()


# 外部调用这个函数，把待发送消息放入消息变量内；然后消息变量会被程序循环读取，并发送出去；
def send_message(message):
    return aliyunMQTTUtil.put_message_into_queue(message)
