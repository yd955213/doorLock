# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   initializeController.py
@Time   :   2022-03-23 16:49
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import traceback

from conctroller import common
from protocol.resetDevices import ResetDevices
from protocol.resetLoraCommunication import ResetLoraCommunication
from protocol.restartDevices import RestartDevices
from ui.myQMessageBox import MyQMessageBox


def reset_gateway(main_ui, device_mac):
    message_box = MyQMessageBox("网关恢复出厂", "请注意!!! 是否继续?")
    if message_box.clicked_yes_button():
        # print("继续")
        reset = ResetDevices(device_mac)
        common.send_msg(reset, main_ui)
    # elif message_box.clicked_no_button():
    #     print("否")


def reset_lora_communication(main_ui, device_mac):
    message_box = MyQMessageBox("Lora通信恢复出厂", "请注意!!! 是否继续?")

    if message_box.clicked_yes_button():
        # print("继续")
        reset = ResetLoraCommunication(device_mac)
        common.send_msg(reset, main_ui)


def restart_devices(main_ui, device_mac):
    restart = RestartDevices(device_mac)
    common.send_msg(restart, main_ui)
