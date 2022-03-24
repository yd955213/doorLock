# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   networkStateController.py
@Time   :   2022-03-24 10:21
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   网关入网状态，lora 通信状态
"""
import traceback

from conctroller import common
from protocol.readGatewayLoraWirelessStates import ReadGatewayLoraWirelessStates
from protocol.readGatewayWirelessCommunicationParameters import ReadGatewayWirelessCommunicationParameters
from protocol.setGatewayWirelessCommunicationParameters import SetGatewayWirelessCommunicationParameters
from protocol.turnOffAllowAccessNetwork import TurnOffAllowAccessNetwork
from protocol.turnOnAllowAccessNetwork import TurnOnAllowAccessNetwork
from tools import stringTrans


def allow_connect_to_the_network(main_ui, device_mac):
    reset = TurnOnAllowAccessNetwork(device_mac)
    common.send_msg(reset, main_ui)


def allow_connect_to_the_network_receive_date_process(main_ui, protocol):
    if protocol.command_status == "00":
        main_ui.isAllowNetworkRadioButton.setChecked(True)
    else:
        main_ui.errorStatusAllowNetworkRadioButton.setChecked(True)


def turn_off_allow_access_network(main_ui, device_mac):
    reset = TurnOffAllowAccessNetwork(device_mac)
    common.send_msg(reset, main_ui)


def turn_off_allow_access_network_receive_date_process(main_ui, protocol):
    print(protocol.command_status)
    if protocol.command_status == "00":
        main_ui.unUseAllowNetWorkRadioButton.setChecked(True)
        print("关闭入网")
    else:
        main_ui.errorStatusAllowNetworkRadioButton.setChecked(True)


def read_gateway_wireless_state(main_ui, device_mac):
    reset = ReadGatewayLoraWirelessStates(device_mac)
    common.send_msg(reset, main_ui)


def read_gateway_wireless_state_receive_date_process(main_ui, protocol):
    if protocol.command_status != "00":
        main_ui.errorStatusAllowNetworkRadioButton.setChecked(True)
        return
    if protocol.valid_data == "00":
        main_ui.unUseAllowNetWorkRadioButton.setChecked(True)
    elif protocol.valid_data == "01":
        main_ui.isCheackAlowNetworkRadioButton.setChecked(True)
    elif protocol.valid_data == "02":
        main_ui.isAllowNetworkRadioButton.setChecked(True)
    # elif protocol.valid_data == "AA":
    else:
        main_ui.errorStatusAllowNetworkRadioButton.setChecked(True)


def set_lora_communication_parameters(main_ui, device_mac):

    '''
    固定头四个字节：0x
    物理信道：1字节，1~26，自组网内必须相同
    网络ID  ：2字节，此值1~FFFE
    网关本地地址：2字节本地网络地址  此值必须大于200即200~FFFE
     不做高低字节 转换
    '''
    data = "AABBDA55"
    physical_channel = main_ui.physical_channelSpinBox.value()
    network_id = main_ui.network_idSpinBox.value()
    gateway_local_address = main_ui.gateway_local_addressSpinBox.value()
    physical_channel = stringTrans.complement_string(hex(physical_channel)[2:], 2)
    network_id = stringTrans.complement_string(hex(network_id)[2:], 4)
    gateway_local_address = stringTrans.complement_string(hex(gateway_local_address)[2:], 4)

    set_g = SetGatewayWirelessCommunicationParameters(device_mac)
    set_g.valid_data = data + physical_channel + network_id + gateway_local_address
    common.send_msg(set_g, main_ui)


def read_lora_communication_parameters(main_ui, device_mac):
    read = ReadGatewayWirelessCommunicationParameters(device_mac)
    common.send_msg(read, main_ui)


def read_lora_communication_parameters_receive_date_process(main_ui, protocol):
    try:
        physical_channel = int(protocol.valid_data[8:10], 16)
        network_id = int(protocol.valid_data[10:14], 16)
        gateway_local_address = int(protocol.valid_data[14:18], 16)
        main_ui.physical_channelSpinBox.setValue(physical_channel)
        main_ui.network_idSpinBox.setValue(network_id)
        main_ui.gateway_local_addressSpinBox.setValue(gateway_local_address)
    except:
        traceback.print_exc()