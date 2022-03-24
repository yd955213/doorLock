# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   protocolCommand.py
@Time   :   2022-03-21 9:11
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   : 所有协议的命令字
"""

search_device = "00"
set_communication_parameters = "01"
set_time = "02"
read_time = "03"
add_door_lock = "04"
delete_door_lock = "05"
lock_is_in_gateway = "06"
initialize_the_gateway = "07"
reset_gateway = "08"
read_gateway_record = "09"
get_gateway_record_point = "0A"
set_gateway_wireless_communication_parameters = "0B"
read_gateway_wireless_communication_parameters = "0C"
set_permission = "0D"
read_permission = "0E"
clear_data = "0F"
read_door_lock_state = "10"
incremental_set_permission = "11"
incremental_read_permission = "12"
# reset_gateway 和 lora_reset 有什么区别？
lora_reset = "13"
turn_on_allow_access_network = "14"
turn_off_allow_access_network = "15"
read_gateway_wireless_state = "16"
set_the_daily_communication_times_of_the_door_lock = "17"
read_the_daily_communication_times_of_the_door_lock = "18"
read_the_daily_communication_times_of_all_door_lock = "19"
remote_door = "1A"
read_the_permission_in_the_gateway = "1B"
read_door_id_in_the_gateway = "1C"
automatically_report_record = "3A"
automatically_report_tamper_evident_events = "3B"

initializer_download = "51"
downloading = "52"
download_complete = "53"
#  网关心跳(改单用，标准版没用用到)
gateway_heartbeat = "4A"

read_flash = "1F"


def get_error_command_state(key):
    msg = None
    key = key.upper()
    if key == "00":
        msg = "成功"
    elif key == "12":
        msg = "无此条记录"
    elif key == "22":
        msg = "网关未获取到门锁网络地址"
    elif key == "32":
        msg = "门锁没有返回"
    elif key == "42":
        msg = "门锁返回数据错误"
    elif key == "72":
        msg = "未获取到门锁电池电量"
    elif key == "EE":
        msg = "无此门锁设备"
    elif key == "FF":
        msg = "本地名单已满，名单数量大于60"
    elif key == "DD":
        msg = "此设备已经存在网关列表中"
    # elif key == "":
    #     msg = ""

    return msg
