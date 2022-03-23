# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   common_protocol.py
@Time   :   2022-03-11 11:14
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import traceback

import globalVariable
from tools import stringTrans
from tools.stringTrans import get_check_sum


class Protocol(object):
    def __init__(self):
        self.heard = "55"
        self.device_flag = "11"
        self.device_mac = "None"
        self.command = "None"
        self.valid_data_length = "None"
        self.valid_data = "None"
        self.command_status = "00"
        self.check_sum = "None"
        self.__data = "None"

    def get_protocol(self):
        try:
            length = int(self.valid_data_length) * 2
            if length == 0:
                self.valid_data = ""

            if len(self.valid_data) < length:
                self.valid_data = stringTrans.complement_string(self.valid_data, length)

            self.__data = self.heard + self.device_flag + self.device_mac + self.command + self.valid_data_length + \
                          self.valid_data + self.command_status
            self.__data += self._get_check_data()
        except Exception as e:
            traceback.print_exc()
        #     raise Exception("Protocol对象初始化错误，属性：device_mac、command、valid_data_length、valid_data 必须不能为空")
        return self.__data.upper()

    def split_data(self, receive_data=None):
        if receive_data is None:
            return
        try:
            self.device_flag = receive_data[2:4]
            self.device_mac = receive_data[4:10]
            self.command = receive_data[10:12]
            self.valid_data_length = receive_data[12:16]
            self.valid_data = receive_data[16:16 + int(self.valid_data_length, 16) * 2]
            self.command_status = receive_data[-6: -4]
            self.check_sum = receive_data[-4:]
        except:
            traceback.print_exc()

    def send_msg(self, ip=None, port=None):
        if globalVariable.get_my_udp_server() is not None:
            data = self.get_protocol()
            globalVariable.get_my_udp_server().send_msg(send_data=data, ip=ip, port=port)

    def _get_check_data(self):
        return get_check_sum(self.__data)
