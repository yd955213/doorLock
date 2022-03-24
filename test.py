# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   test.py
@Time   :   2022-03-11 16:26
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""

if __name__ == '__main__':
    # data = "2022-03-23 13:03:20 周三"
    # data = data.split(" ")
    # data_1 = data[0].split("-")
    # data_2 = data[1].split(":")
    # if data[2] == "周三":
    #     data[2] = "03"
    # data = data_1[0] + data_1[1]+data_1[2]+data_2[0]+data_2[1]+data_2[2]+data[2]
    # print(data)
    # st = "AA11105978060006000000000001EE0297"
    # print(st[-6: -4])
    st = "test"
    test_dic = {'test': [1, 1, 1]}
    my_list = test_dic.get(st)
    print(my_list)
    if my_list is None:
        my_list = []
    my_list.append(1)
    my_list.append(1)
    my_list.append(1)

    test_dic[st] = my_list
    print(test_dic)
    print(test_dic.get(st))
