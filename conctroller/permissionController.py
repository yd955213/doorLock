# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   permissionController.py
@Time   :   2022-03-24 16:38
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from conctroller import common
from protocol.downloadPermission import DownloadPermission
from protocol.incrementalDownloadPermission import IncrementalDownloadPermission
from protocol.incrementalReadPermission import IncrementalReadPermission
from protocol.readPermission import ReadPermission
from tools import stringTrans


def download_permission(main_ui, device_mac):
    numbers = int(main_ui.numbersSpinBox.value())
    card_no = int(main_ui.cardNembeSpinBox.value())

    download = DownloadPermission(device_mac)
    download.valid_data = main_ui.get_door_lock_mac() + __get_download_permission_data(card_no, numbers)
    download.valid_data_length = int(len(download.valid_data)/2)
    common.send_msg(download, main_ui)


def delete_permission(main_ui, device_mac):
    numbers = int(main_ui.numbersSpinBox.value())
    card_no = int(main_ui.cardNembeSpinBox.value())

    download = DownloadPermission(device_mac)
    download.valid_data = main_ui.get_door_lock_mac() + __get_download_permission_data(card_no, numbers, type="0")
    download.valid_data_length = int(len(download.valid_data)/2)
    common.send_msg(download, main_ui)


def read_permission(main_ui, device_mac):
    read = ReadPermission(device_mac)
    read.valid_data = main_ui.get_door_lock_mac()
    common.send_msg(read, main_ui)


def incremental_download_permission(main_ui, device_mac):
    numbers = int(main_ui.numbersSpinBox.value())
    card_no = int(main_ui.cardNembeSpinBox.value())

    download = IncrementalDownloadPermission(device_mac)
    download.valid_data = main_ui.get_door_lock_mac() + __get_download_permission_data(card_no, numbers)
    download.valid_data_length = int(len(download.valid_data)/2)
    common.send_msg(download, main_ui)


def incremental_delete_permission(main_ui, device_mac):
    numbers = int(main_ui.numbersSpinBox.value())
    card_no = int(main_ui.cardNembeSpinBox.value())

    download = IncrementalDownloadPermission(device_mac)
    download.valid_data = main_ui.get_door_lock_mac() + __get_download_permission_data(card_no, numbers, type="0")
    download.valid_data_length = int(len(download.valid_data)/2)
    common.send_msg(download, main_ui)


def incremental_read_permission(main_ui, device_mac):
    read = IncrementalReadPermission(device_mac)
    read.valid_data = main_ui.get_door_lock_mac()
    common.send_msg(read, main_ui)


def read_permission_receive_date_process(main_ui, protocol):
    data = "\t门锁地址号："
    exclusions = stringTrans.complement_string("F", 8, "F")
    if protocol.command_status == "00":
        length = int(protocol.valid_data[12:14], 16)
        data += protocol.valid_data[:12] + "  名单数量：" + str(length) + "\n"
        valid_data = protocol.valid_data[14:]
        for i in range(length):
            permission = valid_data[16 * i:16 * (i + 1)]
            if permission[:8] != exclusions:
                data += "\t卡号："+str(int(stringTrans.set_string_height_to_low(permission[:8]), 16))
                if permission[8:10] == "00":
                    data += "  删除\n"
                elif permission[8:10] == "01\n":
                    data += "  增加\t"
                else:
                    data += "  未定义（{}）\n".format(permission[8:10])
    main_ui.logs(msg=data)


def __get_download_permission_data(card_no, numbers, type="1"):
    data = ""
    for i in range(numbers):
        temp = card_no + i
        temp = stringTrans.set_string_height_to_low(stringTrans.complement_string(hex(temp)[2:], 8))
        data += temp
        if type == "1":
            # 增加权限
            data += "01"
        else:
            # 删除权限
            data += "00"
        data += "BBBBBB"
    return data
