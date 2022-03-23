# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   globalVariable.py
@Time   :   2022-03-11 13:00
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   本程序定义的所有全局变量
"""
from entity import DeviceInfo

_device_info_dic = {}
_my_udp_server = None
# _main_ui = None


def set_device_info_dic(key, value):
    global _device_info_dic
    _device_info_dic[key] = value


def get_device_info_dic_value(key) -> DeviceInfo:
    global _device_info_dic
    try:
        return _device_info_dic[key]
    except:
        return None


def set_my_udp_server(udp_server):
    global _my_udp_server
    _my_udp_server = udp_server


def get_my_udp_server():
    global _my_udp_server
    return _my_udp_server


# def set_main_ui(main_ui):
#     global _main_ui
#     _main_ui = main_ui
#
#
# def get_main_ui():
#     global _main_ui
#     return _main_ui

def get_ip(key):
    """
    获取全局变量中的设备ip
    :param key:
    :return:
    """
    global _device_info_dic
    dev_info = _device_info_dic.get(key)
    if dev_info is None:
        return "None"
    else:
        return dev_info.ip


def get_port(key):
    """
    获取全局变量中的设备port
    :param key:
    :return:
    """
    global _device_info_dic
    dev_info = _device_info_dic.get(key)
    if dev_info is None:
        return "None"
    else:
        return dev_info.command_port
