#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'


str = """
content-length	62018
cache-control	max-age=0
upgrade-insecure-requests	1
origin	https://buy.taobao.com
content-type	application/x-www-form-urlencoded
user-agent	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
accept	text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
sec-fetch-site	same-origin
sec-fetch-mode	navigate
sec-fetch-user	?1
sec-fetch-dest	document
referer	https://buy.taobao.com/auction/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined
accept-encoding	gzip, deflate, br
accept-language	zh-CN,zh;q=0.9,en;q=0.8
"""

def change_str_to_json(str):
    """
    格式化json数据，直接从抓包数据里面copy参数，替换掉str
    :param str:
    :return:
    """
    str_list = str.split('\n')
    json_data = {}
    for str in str_list:
        if str:
            data = str.split('\t')
            json_data[data[0]] = data[1]
    return json_data

def change_str_to_list(str):
    str_list = str.split('\n')
    data = []
    for str in str_list:
        data.append(str)
    return data


if __name__ == "__main__":
    st= change_str_to_json(str)
    print(st)
    # st = change_str_to_list(str)
    # print(st)

