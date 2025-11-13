#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/get_api_info.py

import os
import requests
import json

def get_api_info():
    """获取API相关信息"""
    access_token = "jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH"

    if not access_token:
        print("Please set KDOCS_ACCESS_TOKEN")
        return

    headers = {'Authorization': 'Bearer ' + access_token}

    # 获取用户信息验证token
    user_url = "https://open.kdocs.cn/api/v1/me"
    response = requests.get(user_url, headers=headers)

    print("User info status: " + str(response.status_code))
    if response.status_code == 200:
        print("User: " + json.dumps(response.json(), indent=2))
    else:
        print("User info failed: " + response.text)

    # 获取应用权限
    app_url = "https://open.kdocs.cn/api/v1/applications/me"
    response = requests.get(app_url, headers=headers)

    print("\nApp info status: " + str(response.status_code))
    if response.status_code == 200:
        print("App: " + json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    get_api_info()
