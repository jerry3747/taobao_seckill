#!/usr/bin/env python3
# encoding=utf-8
import http
import os

import requests


def get_useragent_data(filename: str="./useragents.txt") -> list:

    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        with open(user_agents_file, 'r', encoding='utf-8') as reader:
            data = [_.strip() for _ in reader.readlines()]
    except Exception:
        data = ["Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"]
    return data


def notify_user(msg: str):
    print(msg)

    token = os.getenv("TOKEN")
    if not token:
        return

    rs = requests.post(url="https://sre24.com/api/v1/push", json=dict(
        token=token,
        msg=msg,
    )).json()
    assert rs["code"] == http.HTTPStatus.ACCEPTED, rs
