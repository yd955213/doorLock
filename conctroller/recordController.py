# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   recordController.py
@Time   :   2022-03-24 11:11
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :
"""
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

import globalVariable
from conctroller import common
from conctroller.timesController import get_string_to_time_1
from entity import protocolCommand
from protocol.clearData import ClearData
from protocol.getGatewayRecordPoint import GetGatewayRecordPoint
from protocol.readRecordInfo import ReadRecordInfo
from tools import stringTrans
from tools.logs import logger


def read_record_info(main_ui, device_mas):
    info = ReadRecordInfo(device_mas)
    common.send_msg(info, main_ui)


def read_record_info_receive_date_process(main_ui, protocol):
    if protocol.command_status == "00":
        main_ui.recordPoitineSpinBox.setValue(int(stringTrans.set_string_height_to_low(protocol.valid_data[:8], 2), 16))
        main_ui.readRecordNumbersSpinBox.setValue(
            int(stringTrans.set_string_height_to_low(protocol.valid_data[8:], 2), 16))


def get_the_specified_record(main_ui, device_mas):
    def add_start_point(start_point_1):
        temp = start_point_1
        start_point_1 = hex(temp)[2:]
        start_point_1 = stringTrans.set_string_height_to_low(stringTrans.complement_string(start_point_1, 8))
        return start_point_1, temp + 1

    start_point = main_ui.recordPoitineSpinBox.value()
    numbers = main_ui.readRecordNumbersSpinBox.value()

    for i in range(numbers):
        data = add_start_point(start_point)
        start_point = data[1]
        record = GetGatewayRecordPoint(device_mas)
        record.valid_data = data[0]
        common.send_msg(record, main_ui)


def clear_table(table):
    table.setRowCount(0)


def start_auto_data_collection(main_ui, device_mac):
    try:
        server_port = globalVariable.get_auto_server_port(device_mac)
        auto_port = globalVariable.get_auto_port(device_mac)
        print("server_port =", server_port)
        if server_port is None or str(server_port).upper() == "None".upper():
            server_port = 18089

        if auto_port is None or str(auto_port).upper() == "None".upper():
            auto_port = 18090
        main_ui.auto_udp_server.server_port = server_port
        main_ui.auto_udp_server.device_port = auto_port
        main_ui.auto_udp_server.running_thread = True
        main_ui.auto_udp_server.bind()
        main_ui.auto_udp_server.start()
        main_ui.atuoReceiveDataButton.hide()
        main_ui.stopReceiveDataButton.show()
    except Exception as e:
        traceback.print_exc()
        logger.error(e)


def stop_auto_data_collection(main_ui):
    main_ui.auto_udp_server.running_thread = False
    main_ui.auto_udp_server.quit()
    main_ui.auto_udp_server.close()
    main_ui.atuoReceiveDataButton.show()
    main_ui.stopReceiveDataButton.hide()


def data_collection_receive_data_process(main_ui, protocol):
    __update_record_table(main_ui, protocol)
    __receive(main_ui, protocol)


def __update_record_table(main_ui, protocol):
    try:
        table = main_ui.RecordTableWidget
        row = table.rowCount()
        table.insertRow(row)
        '''
        网关记录号（4字节）：每笔记录的号码，低—>高顺序，更换系统时置零
        门锁记录号（4字节）：每笔记录的号码，低—>高顺序
        卡号（4字节）：IC卡取流水号。
        时间（6字节）：BCD格式表示时间。如：0x080804091930 表示2008年8月4日星期四9时19分30秒。
        开门方式（1字节蓝牙或刷卡）：0用户卡刷卡开门，1蓝牙开门，2反锁记录，3钥匙开门 ，4解除反锁，5应急卡，6超级密码开门， 7房间内开门 8远程开门
        设备号（6个字节）：物理地址（低->高）。
        电池电量一个字节
        网关存储门锁记录时间（6个字节）：BCD格式表示时间
        命令状态：0x12  无此条记录     0x00读取成功
        '''
        row_list = []
        # row_list.append(row + 1)
        # 网关记录号
        row_list.append(int(stringTrans.set_string_height_to_low(protocol.valid_data[0:8]), 16))
        # 设备号
        row_list.append(stringTrans.set_string_height_to_low(protocol.valid_data[38:48]))
        # 门锁记录号
        row_list.append(int(stringTrans.set_string_height_to_low(protocol.valid_data[8:16]), 16))
        # 卡号
        row_list.append(int(stringTrans.set_string_height_to_low(protocol.valid_data[16:24]), 16))
        # 时间
        row_list.append(get_string_to_time_1(protocol.valid_data[24:36]))
        # 开门方式
        open_type = protocol.valid_data[36:38]
        if open_type == "00":
            open_type = "刷卡开门"
        elif open_type == "01":
            open_type = "蓝牙开门"
        elif open_type == "02":
            open_type = "反锁记录"
        elif open_type == "03":
            open_type = "钥匙开门"
        elif open_type == "04":
            open_type = "解除反锁"
        elif open_type == "05":
            open_type = "应急卡"
        elif open_type == "06":
            open_type = "超级密码开门"
        elif open_type == "07":
            open_type = "房间内开门"
        elif open_type == "08":
            open_type = "远程开门"
        row_list.append(open_type)
        # 电池电量: 十六进制转成十进制再除以20等于多少伏
        row_list.append(str(int(protocol.valid_data[50:52], 16) / 20) + "V")
        # 网关存储门锁记录时间
        row_list.append(get_string_to_time_1(protocol.valid_data[52:]))
        for i in range(len(row_list)):
            table.setItem(row, i, QTableWidgetItem(str(row_list[i])))
            # 居中显示
            table.item(row, i).setTextAlignment(Qt.AlignHCenter)
    except Exception as e:
        traceback.print_exc()
        logger.error(e)


def clear_data(main_ui, device_mac):

    clear = ClearData(device_mac)
    if main_ui.listOfNamesClearDataRadioButton.isChecked():
        clear.valid_data = "01"
    elif main_ui.cardRecordClearDataRadioButton.isChecked():
        clear.valid_data = "02"
    common.send_msg(clear, main_ui)


def clear_data_receive_date_process(main_ui, protocol):
    data = "None"
    if protocol.valid_data == "01":
        data = "清除 名单 成功"
    elif protocol.valid_data == "01":
        data = "清除 刷卡记录 成功"
    main_ui.logs(msg=data)


def __receive(main_ui, protocol):
    protocol.heard = "55"
    ip = globalVariable.get_ip(protocol.device_mac)
    data = protocol.get_protocol()
    server = None
    if protocol.command == protocolCommand.get_gateway_record_point:
        server = main_ui.my_udp_server
    elif protocol.command == protocolCommand.automatically_report_record:
        server = main_ui.auto_udp_server

    if server is not None:
        server.send_msg(data, ip)
        main_ui.logs(ip=ip, msg=data)