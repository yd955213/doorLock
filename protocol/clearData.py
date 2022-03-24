# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   clearData.py
@Time   :   2022-03-24 9:16
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class ClearData(Protocol):
    def __init__(self, device_mac):
        Protocol.__init__(self)
        self.device_mac = device_mac
        self.command = protocolCommand.clear_data
        self.valid_data_length = "0001"