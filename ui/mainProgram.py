# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   mainProgram.py
@Time   :   2022-03-21 15:17
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import traceback
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QMainWindow, QButtonGroup, QHeaderView

import globalVariable
from conctroller import deviceInfoController, timesController, doorLockController, networkStateController, \
    recordController, permissionController
from conctroller.doorLockController import download_to_the_gateway, delete_to_the_gateway, is_lock_in_the_gateway, \
    read_all_door_lock_in_the_gateway, read_door_lock_state
from conctroller.initializeController import reset_gateway, reset_lora_communication, restart_devices
from conctroller.networkStateController import allow_connect_to_the_network, turn_off_allow_access_network, \
    read_gateway_wireless_state, read_lora_communication_parameters
from conctroller.permissionController import read_permission, download_permission, delete_permission, \
    incremental_download_permission, incremental_delete_permission, incremental_read_permission
from conctroller.readFlashController import read_flash
from conctroller.recordController import read_record_info, get_the_specified_record, clear_table, \
    start_auto_data_collection, stop_auto_data_collection, clear_data
from conctroller.timesController import TimesThread, read_time, set_time
from conctroller.deviceInfoController import search_device, clicked_table_event, set_network_params
from entity import protocolCommand
from entity.protocolCommand import get_error_command_state
from protocol.common_protocol import Protocol
from tools import stringTrans
from udp.udpSend import MyUpdServer

ui, _ = uic.loadUiType("./ui/doorLock.ui")
# ui, _ = uic.loadUiType("./doorLock.ui")


class MainProgram(QMainWindow, ui):
    get_date_thread = TimesThread()
    my_udp_server = MyUpdServer()
    auto_udp_server = MyUpdServer(server_port_1=18089, device_port_1=18090)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.not_show_ui()
        self.__default()
        self.button_events()
        self.table_events()
        self.start_receive_thread()
        self.date_thread()

    def start_receive_thread(self):
        self.my_udp_server.bind()
        self.my_udp_server.receive_data_change.connect(self.data_processing)
        self.my_udp_server.start()
        globalVariable.set_my_udp_server(self.my_udp_server)

    def data_processing(self, ip, receive_data):
        try:
            # print("receive_data =", receive_data)

            self.logs(ip, receive_data, send_type="receive")
            if receive_data is not None and len(receive_data) >= 22:
                p = Protocol()
                p.split_data(receive_data)
                check_sum = stringTrans.get_check_sum(receive_data[0: -4]).upper()
                if p.check_sum.upper() == check_sum:
                    self.logs(msg="\t和校验正确")
                else:
                    self.logs(msg="\t和校验错误；预期：{}， 实际：{}".format(check_sum, p.check_sum.upper()))
                print("receive_data =", receive_data)
                # if p.command_status == "00":
                #     self.logs(msg="\t命令执行成功")
                if p.command == protocolCommand.search_device:
                    deviceInfoController.search_device_receive_data_process(self, p)
                elif p.command == protocolCommand.set_communication_parameters:
                    deviceInfoController.set_communication_parameters_receive_data_process(self, p)
                elif p.command == protocolCommand.read_time:
                    timesController.read_time_receive_date_process(self, p)
                elif p.command == protocolCommand.set_time:
                    timesController.set_time_receive_date_process(self, p)
                elif p.command == protocolCommand.add_door_lock:
                    doorLockController.download_to_the_gateway_receive_date_process(self, p)
                elif p.command == protocolCommand.delete_door_lock:
                    doorLockController.delete_to_the_gateway_receive_date_process(self, p)
                elif p.command == protocolCommand.lock_is_in_gateway:
                    doorLockController.is_lock_in_the_gateway_receive_date_process(self, p)
                elif p.command == protocolCommand.turn_on_allow_access_network:
                    networkStateController.allow_connect_to_the_network_receive_date_process(self, p)
                elif p.command == protocolCommand.turn_off_allow_access_network:
                    networkStateController.turn_off_allow_access_network_receive_date_process(self, p)
                elif p.command == protocolCommand.read_gateway_wireless_state:
                    networkStateController.read_gateway_wireless_state_receive_date_process(self, p)
                elif p.command == protocolCommand.read_gateway_record:
                    recordController.read_record_info_receive_date_process(self, p)
                elif p.command == protocolCommand.get_gateway_record_point or \
                        p.command == protocolCommand.automatically_report_record:
                    recordController.data_collection_receive_data_process(self, p)
                elif p.command == protocolCommand.read_door_id_in_the_gateway:
                    doorLockController.read_all_door_lock_in_the_gateway_receive_date_process(self, p)
                elif p.command == protocolCommand.read_gateway_wireless_communication_parameters:
                    networkStateController.read_lora_communication_parameters_receive_date_process(self, p)
                elif p.command == protocolCommand.read_door_lock_state:
                    doorLockController.read_door_lock_state_receive_date_process(self, p)
                elif p.command == protocolCommand.read_permission or \
                        p.command == protocolCommand.incremental_read_permission:
                    permissionController.read_permission_receive_date_process(self, p)
                elif p.command == protocolCommand.clear_data:
                    recordController.clear_data_receive_date_process(self, p)

                # else:
                self.logs(msg="\t命令状态： " + get_error_command_state(p.command_status))
            else:
                self.logs(msg="\t无效返回, 数据长度不正常")
            self.logs()
        except:
            traceback.print_exc()
        finally:
            p = None

    def date_thread(self):
        self.get_date_thread.update_date.connect(self.update_time_line_edit)
        # 打开界面时 dateTimeLineEdit 文本款输入 当前打开时间
        self.get_date_thread.get_current_date_time()

    def update_time_line_edit(self, date):
        self.dateTimeLineEdit.setText(date)

    def start_or_stop_time_thread(self):
        if self.getLocalTimeRadioButton.isChecked():
            self.get_date_thread.running = True
            self.get_date_thread.start()
        else:
            self.get_date_thread.running = False
            self.get_date_thread.quit()

    def __default(self):
        """
        界面组件的一些默认值
        :return:
        """
        # self.tableWidget.resizeColumnsToContents()
        self.deviceNetworkTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.deviceNetworkTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 列宽自动分配
        # self.RecordTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.RecordTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.RecordTableWidget.setColumnWidth(0, 90)
        self.RecordTableWidget.setColumnWidth(1, 90)
        self.RecordTableWidget.setColumnWidth(2, 90)
        self.RecordTableWidget.setColumnWidth(3, 120)
        self.RecordTableWidget.setColumnWidth(4, 180)
        self.RecordTableWidget.setColumnWidth(5, 90)
        self.RecordTableWidget.setColumnWidth(6, 90)
        self.RecordTableWidget.horizontalHeader().setStretchLastSection(True)
        bg_1 = QButtonGroup(self)
        bg_1.addButton(self.k2_A_RadioButton)
        bg_1.addButton(self.K2_B_RadioButton)
        bg_1.addButton(self.K4_RadioButton)
        bg_1.addButton(self.lock_RadioButton)
        self.lock_RadioButton.setChecked(True)

        bg_2 = QButtonGroup(self)
        bg_2.addButton(self.peerToPeerRadioButton)
        bg_2.addButton(self.broadcastRadioButton)
        self.peerToPeerRadioButton.setChecked(True)

        bg_3 = QButtonGroup(self)
        bg_3.addButton(self.isInTheGatewayRadioButton)
        bg_3.addButton(self.notInTheGatewayRadioButton)
        bg_3.addButton(self.notCheackWhetherIntheGatewayradioButton)
        self.notCheackWhetherIntheGatewayradioButton.setChecked(True)

        bg_4 = QButtonGroup(self)
        bg_4.addButton(self.hasAuthorityRadioButton)
        bg_4.addButton(self.noAuthorityradioButton)

        bg_5 = QButtonGroup(self)
        bg_5.addButton(self.listOfNamesClearDataRadioButton)
        bg_5.addButton(self.cardRecordClearDataRadioButton)

    def not_show_ui(self):
        """
        界面启动时，不进行加载的UI 图标
        :return:
        """
        self.stopReceiveDataButton.hide()

    def change_button_1_to_2(self):
        self.atuoReceiveDataButton.hide()
        self.stopReceiveDataButton.show()

    def change_button_2_to_1(self):
        self.atuoReceiveDataButton.show()
        self.stopReceiveDataButton.hide()

    def table_events(self):
        self.deviceNetworkTable.clicked.connect(lambda: clicked_table_event(self))
        self.doorLockNumbercomboBox.currentIndexChanged.connect(self.__doorLockNumberComboBoxChanged)

    def __doorLockNumberComboBoxChanged(self):
        self.batteryPowerLineEdit.setText("")
        self.doorLockVensonLineEdit.setText("")

    def button_events(self):
        """
        界面上所有buttons 事件处理
        :return:
        """
        self.atuoReceiveDataButton.clicked.connect(self.change_button_1_to_2)
        self.stopReceiveDataButton.clicked.connect(self.change_button_2_to_1)
        self.searchButton.clicked.connect(lambda: search_device(self))
        self.setNetworkButton.clicked.connect(lambda: set_network_params(self))
        self.getLocalTimeRadioButton.toggled.connect(self.start_or_stop_time_thread)
        self.readTimeButton.clicked.connect(lambda: read_time(self, self.get_device_mac()))
        self.setTimeButton.clicked.connect(lambda: set_time(self, self.get_device_mac()))
        self.downloadToTheGatewayButton.clicked.connect(lambda: download_to_the_gateway(self, self.get_device_mac()))
        self.delteFormTheGatewayButton.clicked.connect(lambda: delete_to_the_gateway(self, self.get_device_mac()))
        self.isExistsInTheGatewaytButton.clicked.connect(lambda: is_lock_in_the_gateway(self, self.get_device_mac()))
        self.gatewayRestoreFactoryButton.clicked.connect(lambda: reset_gateway(self, self.get_device_mac()))
        self.resetGatewayLoraCommunicationButton.clicked.connect(lambda: reset_lora_communication(self, self.get_device_mac()))
        self.restartGatewyButton.clicked.connect(lambda: restart_devices(self, self.get_device_mac()))
        self.openAllowConnectToTheNetworkButton.clicked.connect(lambda: allow_connect_to_the_network(self, self.get_device_mac()))
        self.closeAllowConnectToTheNetworkButton.clicked.connect(lambda: turn_off_allow_access_network(self, self.get_device_mac()))
        self.readIsAlowConnectNetworkStatus.clicked.connect(lambda: read_gateway_wireless_state(self, self.get_device_mac()))
        self.readFlashButton.clicked.connect(lambda: read_flash(self, self.get_device_mac()))
        self.readRecordButton.clicked.connect(lambda: read_record_info(self, self.get_device_mac()))
        self.bCButton.clicked.connect(lambda: get_the_specified_record(self, self.get_device_mac()))
        self.clearRecordTableButton.clicked.connect(lambda: clear_table(self.RecordTableWidget))
        self.atuoReceiveDataButton.clicked.connect(lambda: start_auto_data_collection(self, self.get_device_mac()))
        self.stopReceiveDataButton.clicked.connect(lambda: stop_auto_data_collection(self))
        self.read_door_id_in_the_gateway_push_button.clicked.connect(lambda: read_all_door_lock_in_the_gateway(self, self.get_device_mac()))
        self.readLoraCommunicationParamaresPushButton.clicked.connect(lambda: read_lora_communication_parameters(self, self.get_device_mac()))
        self.readLoraCommunicationParamaresPushButton.clicked.connect(lambda: read_lora_communication_parameters(self, self.get_device_mac()))

        self.downloarAuthorityButton.clicked.connect(lambda: download_permission(self, self.get_device_mac()))
        self.deleteAuthorityButton.clicked.connect(lambda: delete_permission(self, self.get_device_mac()))
        self.readAuthorityButton.clicked.connect(lambda: read_permission(self, self.get_device_mac()))
        self.downloadAuthorityIncrementalButton.clicked.connect(lambda: incremental_download_permission(self, self.get_device_mac()))
        self.deleteAuthorityIncrementalButton.clicked.connect(lambda: incremental_delete_permission(self, self.get_device_mac()))
        self.readAuthorityIncrementalButton.clicked.connect(lambda: incremental_read_permission(self, self.get_device_mac()))
        self.claerDataButton.clicked.connect(lambda: clear_data(self, self.get_device_mac()))
        self.readDoorLockStatusButton.clicked.connect(lambda: read_door_lock_state(self, self.get_device_mac()))

    def logs(self, ip=None, msg=None, send_type="send"):
        self.logsTextEdit.moveCursor(QTextCursor.End)
        if ip is None and msg is None:
            self.logsTextEdit.append("")
            return
        if ip is None and msg is not None:
            self.logsTextEdit.append(msg)
            return
        if send_type == "send":
            data = timesController.get_current_date_time() + "（{}）发送数据：{}".format(str(ip), str(msg))
        else:
            data = timesController.get_current_date_time() + "（{}）返回数据：\n\t{}".format(str(ip), str(msg))
        self.logsTextEdit.append(data)

    def get_device_mac(self):
        return self.macLineEdit.text()

    def get_door_lock_mac(self):
        return self.doorLockNumbercomboBox.currentText()

    def closeEvent(self, event):
        # print("关闭窗口")
        self.my_udp_server.running_thread = False
        self.my_udp_server.close()
        self.my_udp_server.quit()
        self.auto_udp_server.running_thread = False
        self.auto_udp_server.close()
        self.auto_udp_server.quit()


if __name__ == '__main__':
    app = QApplication([])
    window = MainProgram()
    window.show()
    app.exec_()
