# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   udpSend.py
@Time   :   2022-03-11 12:36
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import socket
import traceback

from PyQt5.QtCore import pyqtSignal, QThread

from tools.logs import logger

default_server_port = 18087
default_device_port = 18088


class MyUpdServer(QThread):

    receive_data_change = pyqtSignal(str, str)
    running_thread = True

    def __init__(self, server_port_1=None):
        super().__init__()
        if server_port_1 is None or server_port_1 < 0 or server_port_1 > 65535:
            self.server_port = default_server_port
        else:
            self.server_port = server_port_1

        # if self.udp_server is None:
        print("绑定通信端口：" + str(self.server_port))
        try:
            self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.udp_server.bind(("", self.server_port))
        except:
            traceback.print_exc()
        # self.udp_server.settimeout(5)

    def run(self):
        print("开启接收线程")
        while self.running_thread:
            self.receive()
        else:
            self.close()

    def receive(self):
        try:
            receiveData, ip = self.udp_server.recvfrom(1024)
            receiveData = receiveData.hex().upper()
            logger.info('ip({})返回数据：{}'.format(ip, receiveData))
            # data_processing(receiveData)
            if receiveData is not None and len(receiveData) >= 22:
                self.receive_data_change.emit(ip[0], receiveData)
        except Exception as e:
            # traceback.print_exc()
            pass

    def send_msg(self, send_data, ip, port=None):
        """
        建立UDP通道及绑定端口
        """
        if ip is None:
            ip = "<broadcast>"
        if port is None or port < 0 or port > 65535:
            port = default_device_port

        receiveData = None
        try:
            logger.info("向ip({}:{})发送数据:{}：".format(ip, port, send_data))
            self.udp_server.sendto(bytes.fromhex(send_data), (ip, port))
        except Exception as e:
            traceback.print_exc()
            logger.error('UDP 通信异常，异常信息：{}，向ip({})发送数据:{}'.format(e, ip, send_data))
        return receiveData

    def close(self):
        if self.udp_server is not None:
            try:
                self.udp_server.close()
            except:
                traceback.print_exc()
