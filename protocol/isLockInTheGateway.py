# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   isLockInTheGateway.py
@Time   :   2022-03-23 15:40
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class IsLockInTheGateway(Protocol):
    def __init__(self, device_mac):
        super(IsLockInTheGateway, self).__init__()
        self.device_mac = device_mac
        self.command = protocolCommand.lock_is_in_gateway
        self.valid_data_length = "0006"