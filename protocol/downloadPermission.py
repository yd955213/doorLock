# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   downloadPermission.py
@Time   :   2022-03-24 9:11
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   有效数据长度 可变 7+8*AA
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class DownloadPermission(Protocol):
    """
    有效数据长度 可变 7+8*AA , 需调用时自己设置
    """
    def __init__(self, device_mac):
        Protocol.__init__(self)
        self.device_mac = device_mac
        self.command = protocolCommand.set_permission
        self.valid_data_length = "0007"