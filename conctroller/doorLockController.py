# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   doorLockController.py
@Time   :   2022-03-23 15:22
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import threading
import time
import traceback

import globalVariable
from protocol.deleteDoorLockDevices import DeleteDoorLockDevices
from protocol.downloadDoorLockDevices import DownloadDoorLockDevices
from protocol.isLockInTheGateway import IsLockInTheGateway


def download_to_the_gateway(main_ui, mac):
    door_lock_mac = str(main_ui.doorLockNumbercomboBox.currentText())
    protocol = DownloadDoorLockDevices(mac)
    protocol.valid_data = door_lock_mac
    __send_msg(protocol, main_ui)


def download_to_the_gateway_receive_date_process(main_ui, protocol):
    pass


def delete_to_the_gateway(main_ui, mac):
    door_lock_mac = str(main_ui.doorLockNumbercomboBox.currentText())
    protocol = DeleteDoorLockDevices(mac)
    protocol.valid_data = door_lock_mac
    __send_msg(protocol, main_ui)


def delete_to_the_gateway_receive_date_process(main_ui, protocol):
    if protocol.command_status == "00":
        main_ui.doorLockNumbercomboBox.removeItem(protocol.valid_data)


def is_lock_in_the_gateway(main_ui, mac):
    try:
        door_lock_mac = str(main_ui.doorLockNumbercomboBox.currentText())
        print("door_lock_mac =", door_lock_mac)
        protocol = IsLockInTheGateway(mac)
        protocol.valid_data = door_lock_mac
        __send_msg(protocol, main_ui)
    except:
        traceback.print_exc()


def is_lock_in_the_gateway_receive_date_process(main_ui, protocol):
    if protocol.command_status == "00":
        main_ui.isInTheGatewayRadioButton.setChecked(True)
    elif protocol.command_status == "EE":
        main_ui.notInTheGatewayRadioButton.setChecked(True)
    else:
        main_ui.notCheackWhetherIntheGatewayradioButton.setChecked(True)
    # 5秒后将 状态改为 未检测
    threading.Thread(target=__update_radioButton, args=(main_ui.notCheackWhetherIntheGatewayradioButton,)).start()


def __send_msg(protocol, main_ui):
    ip = globalVariable.get_ip(protocol.device_mac)
    protocol.send_msg(ip)
    main_ui.logs(ip=ip, msg=protocol.get_protocol())


def __update_radioButton(radio_button):
    time.sleep(5)
    radio_button.setChecked(True)
