# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   logs.py
@Time   :   2022-03-11 12:39
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""

import logging.handlers
import os
import re


"""
logging 配置
"""
filename = '../log'
if not os.path.exists(filename):
    os.makedirs(filename)

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.handlers.TimedRotatingFileHandler(filename='{}/default.log'.format(filename), when='S', interval=10,
                                                    backupCount=2)
# 设置日志文件后缀，以当前时间作为日志文件后缀名。
handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
handler.suffix = "%Y-%m-%d_%H.log"
handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")
logger.addHandler(handler)
# # 创建输出到控制台的输出流
# console = logging.StreamHandler()
# # 设置日志等级
# console.setLevel(logging.INFO)
# # 设置日志格式
# console.setFormatter(formatter)
# 添加到logger输出
# logger.addHandler(console)
