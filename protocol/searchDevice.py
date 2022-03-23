# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   searchDevice.py
@Time   :   2022-03-11 11:56
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class SearchDevice(Protocol):

    def __init__(self, device_mac):
        super(SearchDevice, self).__init__()
        # Protocol.__init__(self)
        self.device_mac = device_mac
        self.command = protocolCommand.search_device
        self.valid_data_length = "0000"


