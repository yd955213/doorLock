# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   readTheCommunicationTimesOfTheDoorLock.py
@Time   :   2022-03-24 9:24
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from entity import protocolCommand
from protocol.common_protocol import Protocol


class ReadTheCommunicationTimesOfTheDoorLock(Protocol):
    def __init__(self, device_mac):
        Protocol.__init__(self)
        self.device_mac = device_mac
        self.command = protocolCommand.read_the_daily_communication_times_of_the_door_lock
        self.valid_data_length = "0000"