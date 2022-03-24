# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   readFlashController.py
@Time   :   2022-03-24 10:58
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from conctroller import common
from protocol.readFlash import ReadFlash
from tools import stringTrans


def read_flash(main_ui, device_mac):
    type_param = main_ui.readFlashParamsComboBox.currentIndex()
    print(type_param)
    if type_param == 0:
        type_param = "01"
    elif type_param == 1:
        type_param = "02"
    elif type_param == 2:
        type_param = "03"
    elif type_param == 3:
        type_param = "04"
    type_param = stringTrans.complement_string(type_param, 2)

    block_num = main_ui.readFlashblockSpinBox.text()
    block_num= stringTrans.complement_string(block_num, 4)

    r_flash = ReadFlash(device_mac)
    r_flash.valid_data = type_param + block_num

    common.send_msg(r_flash, main_ui)


def read_flash_receive_date_process(main_ui, protocol):
    pass