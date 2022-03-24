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
_all_door_lock = {}


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


def get_auto_port(key):
    """
    获取全局变量中的设备 auto_port 主动通道端口号 （本地端口号）
    :param key:
    :return:
    """
    global _device_info_dic
    dev_info = _device_info_dic.get(key)
    if dev_info is None:
        return "None"
    else:
        return dev_info.auto_port


def get_auto_server_port(key):
    """
    获取全局变量中的设备 auto_server_port 主动通道端口号（远程端口号）
    :param key:
    :return:
    """
    global _device_info_dic
    dev_info = _device_info_dic.get(key)
    if dev_info is None:
        return "None"
    else:
        return dev_info.auto_server_port


def get_all_door_lock():
    global _all_door_lock
    return _all_door_lock


def add_all_door_lock(key, value):
    global _all_door_lock
    _all_door_lock[key] = value


def get_all_door_lock_by_mac(device_mac) -> list:
    """
    获取网关设备中 所有绑定的门锁
    :param device_mac: 网关设备 mac
    :return: list
    """
    global _all_door_lock
    lock_list = _all_door_lock.get(device_mac)
    if lock_list is None:
        return "None"
    else:
        return lock_list


def add_all_door_lock_by_mac(device_mac, lock_mac):
    """
    将门锁设备mac 添加到 网关设备中
    :param device_mac: 网关设备 mac
    :param lock_mac: 门锁设备mac
    """
    global _all_door_lock
    lock_list_temp = _all_door_lock.get(device_mac)
    if lock_list_temp is None:
        lock_list_temp = []
    lock_list_temp.append(lock_mac)
    _all_door_lock[device_mac] = lock_list_temp


def delete_all_door_lock_by_mac(device_mac, lock_mac):
    """
    从网关设备中 删除 门锁设备mac
    :param device_mac: 网关设备 mac
    :param lock_mac: 门锁设备mac
    """
    global _all_door_lock
    lock_list_temp = _all_door_lock.get(device_mac)
    if lock_list_temp is not None:
        lock_list_temp.remove(lock_mac)
