# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   timesController.py
@Time   :   2022-03-22 13:54
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import time

from PyQt5.QtCore import QDateTime, pyqtSignal, QThread

import globalVariable
from protocol.readTime import ReadTime
from protocol.setTime import SetTime


def get_current_date_time():
    current = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
    return str(current)


class TimesThread(QThread):
    update_date = pyqtSignal(str)
    running = True

    def __init__(self):
        super().__init__()

    def run(self):
        while self.running:
            self.get_current_date_time()
            time.sleep(1)

    def get_current_date_time(self):
        current = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss ddd")
        self.update_date.emit(str(current))


def set_time(main_ui, device_mac):
    data = main_ui.dateTimeLineEdit.text()
    data = data.split(" ")
    data_1 = data[0].split("-")
    data_2 = data[1].split(":")
    if data[2] == "周三":
        data[2] = "03"
    data = data_1[0] + data_1[1] + data_1[2] + data_2[0] + data_2[1] + data_2[2] + data[2]

    set = SetTime(device_mac)
    set.valid_data = data
    ip = globalVariable.get_ip(set.device_mac)
    set.send_msg(ip)
    main_ui.logs(ip, set.get_protocol())


def set_time_receive_date_process(main_ui, protocol):
    pass


def read_time(main_ui, device_mac):
    read = ReadTime(device_mac)
    ip = globalVariable.get_ip(read.device_mac)
    read.send_msg(ip)
    main_ui.logs(ip, read.get_protocol())


def read_time_receive_date_process(main_ui, protocol):
    print(protocol.valid_data)
    #     0xYYYYMMDDhhmmssWW：  BCD格式表示时间。如：0x2008080809193005
    # 表示2008年8月8日星期五9时19分30秒。注WW取值：星期日取0x00，星期六取值0x06。
    date = protocol.valid_data[0:4] + "-" + \
          protocol.valid_data[4:6] + "-" +\
          protocol.valid_data[6:8] + " " +\
          protocol.valid_data[8:10] + ":" +\
          protocol.valid_data[10:12] + ":" +\
          protocol.valid_data[12:14] + " "
    temp = protocol.valid_data[14:16]
    if temp == "00":
        date += "周日"
    elif temp == "01":
        date += "周一"
    elif temp == "02":
        date += "周二"
    elif temp == "03":
        date += "周三"
    elif temp == "04":
        date += "周四"
    elif temp == "05":
        date += "周五"
    elif temp == "06":
        date += "周六"

    main_ui.dateTimeLineEdit.setText(date)

if __name__ == '__main__':
    TimesThread().start()