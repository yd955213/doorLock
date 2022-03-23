# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   deviceInfoController.py
@Time   :   2022-03-11 13:58
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   搜索设备 设置网络参数
"""
import traceback

from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

import globalVariable
from entity import DeviceInfo
from protocol.searchDevice import SearchDevice
from protocol.setNetworkParams import SetNetworkParams
from tools import stringTrans
from tools.stringTrans import get_String_to_ip, set_string_height_to_low


def search_device(main_ui):
    # global main_ui
    ip = None
    try:
        main_ui.deviceNetworkTable.setRowCount(0)
        if main_ui.broadcastRadioButton.isChecked():
            ip = None
        if main_ui.peerToPeerRadioButton.isChecked():
            ip = main_ui.ipLineEdit.text()
        s = SearchDevice("FFFFFF")
        s.send_msg(ip=ip)
        main_ui.logs(ip, s.get_protocol())
    except Exception as e:
        traceback.print_exc()


def set_network_params(main_ui):
    mac = main_ui.macLineEdit.text()
    ip = main_ui.ipLineEdit.text()
    remote_ip = main_ui.remoteIpLineEdit.text()
    subnet_mask = main_ui.subnetMaskLineEdit.text()
    gateway = main_ui.gatewayLineEdit.text()
    if len(mac) == 0:
        QMessageBox.warning(main_ui, "网络参数输入错误", "MAC地址不能为空")
        return
    if len(ip) == 0:
        QMessageBox.warning(main_ui, "网络参数输入错误", "ip地址不能为空")
        return
    if len(remote_ip) == 0:
        QMessageBox.warning(main_ui, "网络参数输入错误", "远程地址不能为空")
        return
    if len(gateway) == 0:
        QMessageBox.warning(main_ui, "网络参数输入错误", "网关地址不能为空")
        return
    if len(subnet_mask) == 0:
        QMessageBox.warning(main_ui, "网络参数输入错误", "子网掩码不能为空")
        return
    # 合成设置通讯参数 的有效数据
    '''
        0xMMMMMMMM:子网掩码。例如：0xFFFFFF00代表255.255.255.0
        0xGGGGGGGG:网关参数。例如：0xC0A8FE01代表：192.168.254.1
        0xLLLLLLLL: 网关本地IP地址
        0xRRRRRRRR:网关远程IP地址
        BBBB:网关主动上报本地端口bbbb：网关主动上报远程端口
        IIII：网关指令通道本地端口iiii:网关指令通道远程端口
        EEEE:预留本地端口eeee:预留远程端口
    '''
    try:
        device_info = globalVariable.get_device_info_dic_value(mac)
        valid_data = stringTrans.get_ip_to_string(subnet_mask) + \
                     stringTrans.get_ip_to_string(gateway) + \
                     stringTrans.get_ip_to_string(ip) + \
                     stringTrans.get_ip_to_string(remote_ip) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.auto_port)[2:], 4)) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.auto_server_port)[2:], 4)) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.command_port)[2:], 4)) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.command_server_port)[2:], 4)) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.reserved_local_port)[2:], 4)) + \
                     stringTrans.set_string_height_to_low(
                         stringTrans.complement_string(hex(device_info.reserved_remote_port)[2:], 4))

        protocol = SetNetworkParams(mac)
        protocol.valid_data = valid_data

        main_ui.logs(globalVariable.get_ip(mac), protocol.get_protocol())
        protocol.send_msg(ip=globalVariable.get_ip(mac), port=globalVariable.get_port(mac))
    except:
        traceback.print_exc()


def update_table(main_ui, device_info):
    if device_info is None:
        return

    try:

        row = main_ui.deviceNetworkTable.rowCount()
        main_ui.deviceNetworkTable.insertRow(row)
        main_ui.deviceNetworkTable.setItem(row, 0, QTableWidgetItem(device_info.device_mac))
        main_ui.deviceNetworkTable.setItem(row, 1, QTableWidgetItem(device_info.ip))
        main_ui.deviceNetworkTable.setItem(row, 2, QTableWidgetItem(device_info.soft_version))
        main_ui.deviceNetworkTable.setItem(row, 3, QTableWidgetItem(device_info.hard_version))
        if row == 0 and device_info is not None:
            __update_device_info_line_edits(main_ui, device_info)
    except:
        traceback.print_exc()


def search_device_receive_data_process(main_ui, protocol=None):
    if protocol is None:
        return
    try:
        device_info = DeviceInfo()
        device_info.device_mac = protocol.device_mac
        device_info.hard_version = protocol.valid_data[:4]
        device_info.soft_version = protocol.valid_data[4:10]
        device_info.subnet_mask = get_String_to_ip(protocol.valid_data[10:18])
        device_info.gateway = get_String_to_ip(protocol.valid_data[18:26])
        device_info.ip = get_String_to_ip(protocol.valid_data[26:34])
        device_info.server_ip = get_String_to_ip(protocol.valid_data[34:42])
        device_info.auto_port = int(set_string_height_to_low(protocol.valid_data[42:46]), 16)
        device_info.auto_server_port = int(set_string_height_to_low(protocol.valid_data[46:50]), 16)
        device_info.command_port = int(set_string_height_to_low(protocol.valid_data[50:54]), 16)
        device_info.command_server_port = int(set_string_height_to_low(protocol.valid_data[54:58]), 16)
        device_info.reserved_local_port = int(set_string_height_to_low(protocol.valid_data[58:62]), 16)
        device_info.reserved_remote_port = int(set_string_height_to_low(protocol.valid_data[62:66]), 16)
        globalVariable.set_device_info_dic(device_info.device_mac, device_info)

        update_table(main_ui, device_info)
    except:
        traceback.print_exc()


def set_communication_parameters_receive_data_process(main_ui, protocol):
    if protocol.command_status == "00":
        # 命令执行成功， 修改全局参数
        device_info = globalVariable.get_device_info_dic_value(protocol.device_mac)
        device_info.subnet_mask = get_String_to_ip(protocol.valid_data[0:8])
        device_info.gateway = get_String_to_ip(protocol.valid_data[8:16])
        device_info.ip = get_String_to_ip(protocol.valid_data[16:24])
        device_info.server_ip = get_String_to_ip(protocol.valid_data[24:32])
        device_info.auto_port = int(set_string_height_to_low(protocol.valid_data[32:36]), 16)
        device_info.auto_server_port = int(set_string_height_to_low(protocol.valid_data[36:40]), 16)
        device_info.command_port = int(set_string_height_to_low(protocol.valid_data[40:44]), 16)
        device_info.command_server_port = int(set_string_height_to_low(protocol.valid_data[44:48]), 16)
        device_info.reserved_local_port = int(set_string_height_to_low(protocol.valid_data[48:52]), 16)
        device_info.reserved_remote_port = int(set_string_height_to_low(protocol.valid_data[52:56]), 16)


def clicked_table_event(main_ui):
    try:

        row = main_ui.deviceNetworkTable.currentRow()
        device_mac = main_ui.deviceNetworkTable.item(row, 0).text()
        device_info = globalVariable.get_device_info_dic_value(device_mac)
        __update_device_info_line_edits(main_ui, device_info)
    except:
        traceback.print_exc()


def __update_device_info_line_edits(main_ui, device_info):
    try:
        main_ui.macLineEdit.setText(device_info.device_mac)
        main_ui.ipLineEdit.setText(device_info.ip)
        main_ui.remoteIpLineEdit.setText(device_info.server_ip)
        main_ui.gatewayLineEdit.setText(device_info.gateway)
        main_ui.subnetMaskLineEdit.setText(device_info.subnet_mask)
    except:
        traceback.print_exc()

