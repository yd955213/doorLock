# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   common.py
@Time   :   2022-03-23 16:52
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import globalVariable


def send_msg(protocol, main_ui):
    ip = globalVariable.get_ip(protocol.device_mac)
    protocol.send_msg(ip)
    main_ui.logs(ip=ip, msg=protocol.get_protocol())