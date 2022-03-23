# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   downloadDoorLockDevices.py
@Time   :   2022-03-23 15:26
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class DownloadDoorLockDevices(Protocol):
    def __init__(self, device_mac):
        super(DownloadDoorLockDevices, self).__init__()
        self.device_mac = device_mac
        self.command = protocolCommand.add_door_lock
        self.valid_data_length = "0006"
