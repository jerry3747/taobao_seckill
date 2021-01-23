#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import re
import json
import time
import datetime
import requests
import urllib3
import browsercookie
from urllib.parse import *
from seckill.seckill_taobao import ChromeDrive

urllib3.disable_warnings()

session = requests.session()


def get_cookies():
    """
    手动操作浏览器，用browsercookie获取浏览器cookie
    :return:
    """
    ck = browsercookie.chrome()
    for i in ck:
        if 'taobao' in i.domain:
            session.cookies.set(i.name, i.value)

def get_buy_cart():
    """
    获取购物车信息
    :return: 返回提交结算请求的参数
    """
    url = 'https://cart.taobao.com/cart.htm'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0'}
    res = session.get(url, headers = headers, verify = False)
    first_data = re.search('try{var firstData = (.*?);}catch', res.text).group(1)
    s_tag = res.headers['s_tag']
    user_rep = re.search('\|\^taoMainUser:(.*?):\^', s_tag)
    if user_rep:
        user_id = user_rep.group(1)
        print("成功获取购物车信息")
    else:
        print("cookie失效，请重新登陆")
    return first_data, user_id


def parse_cart_data(first_data):
    """
    解析购物车信息
    :param first_data:
    :return:
    """
    first_data = json.loads(first_data)
    if len(first_data['list']) == 0:
        print("购物车是空的")
        return
    cart_id = first_data['list'][0]['bundles'][0]['orders'][0]['cartId']
    cart_params = first_data['list'][0]['bundles'][0]['orders'][0]['cartActiveInfo']['cartBcParams']
    item_id = first_data['list'][0]['bundles'][0]['orders'][0]['itemId']
    sku_id = first_data['list'][0]['bundles'][0]['orders'][0]['skuId']
    seller_id = first_data['list'][0]['bundles'][0]['orders'][0]['sellerId']
    attributes = first_data['list'][0]['bundles'][0]['orders'][0]['toBuyInfo']
    print("成功解析购物车信息")
    return cart_id, item_id, sku_id, seller_id, cart_params, attributes


def confirm_order(cart_id, item_id, sku_id, seller_id, cart_params, attributes):
    """
    发送结算请求
    :param cart_id: 购物车id
    :param item_id: 商品id
    :param sku_id:
    :param seller_id: 卖家id
    :param cart_params: 购物车参数
    :param attributes:
    :return: 返回提交订单需要的参数
    """
    url = 'https://buy.taobao.com/auction/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined'
    headers = {'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
               'origin': 'https://cart.taobao.com', 'content-type': 'application/x-www-form-urlencoded',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
               'sec-fetch-dest': 'document', 'referer': 'https://cart.taobao.com/',
               'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8', }
    data = {"item": f"{cart_id}_{item_id}_1_{sku_id}_{seller_id}_0_0_0_{cart_params}_{quote(str(attributes))}__0",
        "buyer_from": "cart", "source_time": "".join(str(int(time.time() * 1000)))}
    res = session.post(url = url, data = data, headers = headers, verify = False)
    order_data = re.search('orderData= (.*?);\n</script>', res.text).group(1)
    print("成功发送结算请求")
    return order_data


def parse_order_data(order_data):
    """
    解析订单信息
    :param order_data:
    :return:
    """
    order_data = json.loads(order_data)
    endpoint = order_data['endpoint']
    data = order_data['data']
    structure = order_data['hierarchy']['structure']
    hierarchy = order_data['hierarchy']
    linkage = order_data['linkage']
    linkage.pop('url')
    submitref = order_data['data']['submitOrderPC_1']['hidden']['extensionMap']['secretValue']
    sparam1 = order_data['data']['submitOrderPC_1']['hidden']['extensionMap']['sparam1']
    # sparam2 = order_data['data']['submitOrderPC_1']['hidden']['extensionMap']['sparam2']
    input_charset = order_data['data']['submitOrderPC_1']['hidden']['extensionMap']['input_charset']
    event_submit_do_confirm = order_data['data']['submitOrderPC_1']['hidden']['extensionMap']['event_submit_do_confirm']
    print("成功解析订单信息")
    return endpoint, data, structure, hierarchy, linkage, submitref, sparam1, input_charset, event_submit_do_confirm


def submit_order(order_data, item_id, user_id):
    """
    发送提交订单请求
    :param order_data:订单参数
    :param item_id: 商品id
    :param user_id: 用户id
    :return:
    """
    token = session.cookies['_tb_token_']
    endpoint, data, structure, hierarchy, linkage, submitref, sparam1, input_charset, event_submit_do_confirm = parse_order_data(
        order_data)
    url = f'https://buy.taobao.com/auction/confirm_order.htm?x-itemid={item_id}&x-uid={user_id}&submitref={submitref}&sparam1={sparam1}'
    new_data = parse_submit_data(data)
    form_data = {'action': '/order/multiTerminalSubmitOrderAction', '_tb_token_': token, 'event_submit_do_confirm': '1',
        'praper_alipay_cashier_domain': 'cashierrz54', 'input_charset': 'utf-8',
        'endpoint': quote(json.dumps(endpoint)), 'data': quote(json.dumps(new_data)),
        'hierarchy': quote(json.dumps({"structure": structure})), 'linkage': quote(json.dumps(linkage)), }
    headers = {'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1', 'origin': 'https://buy.taobao.com',
               'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate', 'sec-fetch-user': '?1',
               'sec-fetch-dest': 'document',
               'referer': 'https://buy.taobao.com/auction/order/confirm_order.htm?spm=a1z0d.6639537.0.0.undefined',
               'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    res = session.post(url = url, data = form_data, headers = headers, verify = False)
    if res.status_code == 200:
        print('成功提交订单')


def parse_submit_data(data):
    new_data = {}
    for k, v in data.items():
        if v.get('submit') == 'true' or v.get('submit'):
            new_data[k] = v
    return new_data


def run_with_selenium_cookie():
    """
    通过selenium模拟浏览器登陆，获取cookie并发送请求
    :return:
    """
    seckill_time = '2021-01-23 15:05:00'
    seckill_time_obj = datetime.datetime.strptime(seckill_time, '%Y-%m-%d %H:%M:%S')
    ChromeDrive(seckill_time = seckill_time).keep_wait()
    with open('./cookies.txt', 'r', encoding = 'utf-8') as f:
        data = f.read()
    cookies = json.loads(data)
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    first_data, user_id = get_buy_cart()
    while True:
        current_time = datetime.datetime.now()
        print("开始抢购")
        if current_time >= seckill_time_obj:
            try:
                cart_id, item_id, sku_id, seller_id, cart_params, attributes = parse_cart_data(first_data)
            except TypeError as e:
                print(e)
                break
            else:
                order_data = confirm_order(cart_id, item_id, sku_id, seller_id, cart_params, attributes)
                submit_order(order_data, item_id, user_id)
                break
        time.sleep(0.1)


def run_with_browsercookie():
    """
    手动打开浏览器并登陆淘宝，然后用browsercookie获取淘宝页面的cookie，

    :return:
    """
    seckill_time = '2021-01-23 16:40:00'
    seckill_time_obj = datetime.datetime.strptime(seckill_time, '%Y-%m-%d %H:%M:%S')
    get_cookies()
    first_data, user_id = get_buy_cart()
    while True:
        current_time = datetime.datetime.now()
        if (seckill_time_obj - current_time).seconds > 180:
            print('等待中......')
            time.sleep(60)
        if current_time >= seckill_time_obj:
            try:
                cart_id, item_id, sku_id, seller_id, cart_params, attributes = parse_cart_data(first_data)
            except TypeError as e:
                print(e)
                break
            else:
                order_data = confirm_order(cart_id, item_id, sku_id, seller_id, cart_params, attributes)
                submit_order(order_data, item_id, user_id)
                break


if __name__ == '__main__':
    run_with_browsercookie()
    pass
