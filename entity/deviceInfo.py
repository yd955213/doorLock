# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   deviceInfo.py
@Time   :   2022-03-11 13:02
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""


class DeviceInfo(object):
    def __init__(self):
        self.ip = "None"
        self.command_port = 18088
        self.command_server_port = 18087
        self.auto_port = 18090
        self.auto_server_port = 18089
        self.reserved_local_port = "None"
        self.reserved_remote_port = "None"
        self.device_mac = "None"
        self.server_ip = "None"
        self.gateway = "None"
        self.subnet_mask = "None"
        self.hard_version = "None"
        self.soft_version = "None"

    def to_string(self):
        return "DeviceInfo{" + \
                "ip = " + self.ip + \
                ", command_port = " + str(self.command_port) + \
                ", command_server_port = " + str(self.command_server_port) + \
                ", auto_port = " + str(self.auto_port) + \
                ", auto_server_port = " + str(self.auto_server_port) + \
                ", reserved_local_port = " + str(self.reserved_local_port) + \
                ", reserved_remote_port = " + str(self.reserved_remote_port) + \
                ", device_mac = " + self.device_mac + \
                ", server_ip = " + self.server_ip + \
                ", gateway = " + self.gateway + \
                ", subnet_mask = " + self.subnet_mask + \
                ", hard_version = " + self.hard_version + \
                ", soft_version = " + self.soft_version + \
               "}"