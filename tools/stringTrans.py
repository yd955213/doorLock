# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   stringTrans.py
@Time   :   2022-03-11 11:39
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import math


def string_to_hex_list(string="", step=2) -> list:
    """
    将16进制字符串装换为16进制列表
    :param string:
    :param step：步长 默认2， 表示step个字符串为一个新的字符串
    :return:
    """
    length = len(string)
    '''
    补齐字符串，防止可能的 、错误的 参数传入导致出错
    '''
    if not length % 2 == 0:
        string = "0" + string
        length += 1
    hex_list = []
    length = math.ceil(length / step)
    for i in range(0, length):
        hex_list.append(string[step * i: step * (i + 1)])
    return hex_list


def set_string_height_to_low(strings, step=2) -> str:
    """
    将字符串每step个字符为一组，倒序排序
    :param strings:
    :param step:步长 默认2
    :return:
    """
    str_list = string_to_hex_list(str(strings), step)
    str_list = str_list[::-1]
    strings = ""
    for st in str_list:
        strings += st
    return strings


def complement_string(strings="", length=2, fill_param="0", back_ward=False) -> str:
    """
    填充字符串长度,大于该长度则取后length位的字符串, 若length小于等于0，返回原字符串
    :param strings: 字符串
    :param length: 目标字符串长度
    :param fill_param: 填充数据，默认0，该参数长度只能为1，否则导致字符串长度错误
    :param back_ward: True: 字符串后面补零， False: 字符串前面补零
    :return:
    """
    strings = str(strings)
    if length <= 0:
        return strings

    st_length = len(strings)
    le = length - st_length
    if le > 0:
        for i in range(0, le):
            if back_ward:
                strings = strings + fill_param
            else:
                strings = fill_param + strings
        else:
            # 防止有逗比输入fill_param的长度超过1 ，这里做一个处理
            if back_ward:
                strings = strings[:length]
            else:
                strings = strings[len(strings) - length:]
    elif le < 0:
        # 取后length位的字符串
        strings = strings[-le:]
    return strings


def get_check_sum(date=""):
    data = string_to_hex_list(date)
    total = 0
    try:
        for i in data:
            total += int(i, 16)
        total = str(hex(total))
    except Exception as e1:
        return "和校验字符串转换出错，请检查协议\t" + e1.__str__()
    # 去掉转换生成的 0x
    # print(total)
    total = total[2:]
    total = complement_string(total, 4)
    return total.upper()


def get_ip_to_string(data):
    ip = data.split(".")
    ip_temp = ""
    for i in ip:
        ip_temp += complement_string(hex(int(i))[2:], 2)
    return ip_temp.upper()


def get_String_to_ip(data):
    ip_list = string_to_hex_list(data)
    ip = ""
    for i in ip_list:
        ip += str(int(i, 16)) + "."
    return ip[:-1]


if __name__ == '__main__':
    print(get_ip_to_string("192.168.254.1"))
    print(get_String_to_ip("C0A8FE01"))
