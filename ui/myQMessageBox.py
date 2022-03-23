# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   myQMessageBox.py
@Time   :   2022-03-23 16:55
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
from PyQt5.QtWidgets import QMessageBox, QPushButton, QWidget


class MyQMessageBox(object):
    message_box = None

    def __init__(self, title, msg):
        self.message_box = QMessageBox()
        self.message_box.setWindowTitle(title)
        self.message_box.setText(msg)
        self.yes = QPushButton("是")
        self.no = QPushButton("否")
        self.message_box.addButton(self.yes, QMessageBox.YesRole)
        self.message_box.addButton(self.no, QMessageBox.NoRole)
        self.message_box.show()
        self.message_box.exec_()

    def clicked_yes_button(self):
        boolean = True if self.message_box.clickedButton() == self.yes else False
        return boolean

    def clicked_no_button(self):
        boolean = True if self.message_box.clickedButton() == self.no else False
        return boolean
