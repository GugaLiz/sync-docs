#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/sync_kdocs_correct.py

import os
import requests
import sys

def update_kdocs():
    access_token = "jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH"
    document_id = 'cjpVZz0ASxGp'

    if not access_token:
        print("ERROR: KDOCS_ACCESS_TOKEN is required")
        sys.exit(1)

    try:
        # Read README content
        print("Reading README.md...")
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        print("Content size: " + str(len(content)) + " characters")

        # 正确的API端点 - 根据官方文档
        # 方法1: 使用文件更新接口
        api_url = "https://open.kdocs.cn/api/v1/files/" + document_id + "/content"

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

        # 根据金山文档API文档构建正确的payload
        payload = {
            "content": content,
            "format": "markdown"  # 指定内容格式
        }

        print("Sending update request to: " + api_url)
        response = requests.put(api_url, headers=headers, json=payload, timeout=30)

        # Check response
        print("Response status: " + str(response.status_code))

        if response.status_code == 200:
            print("SUCCESS: Document updated successfully")
            sys.exit(0)
        elif response.status_code == 404:
            print("ERROR: 404 - Endpoint not found. Trying alternative endpoints...")
            # 尝试其他可能的端点
            try_alternative_endpoints(access_token, document_id, content)
        else:
            print("Response: " + response.text)
            sys.exit(1)

    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(1)

def try_alternative_endpoints(access_token, document_id, content):
    """尝试其他可能的API端点"""
    endpoints = [
        "https://open.kdocs.cn/api/v1/documents/" + document_id,
        "https://open.kdocs.cn/api/v1/words/" + document_id + "/content",
        "https://open.kdocs.cn/api/v1/documents/" + document_id + "/versions",
    ]

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    payload = {"content": content}

    for endpoint in endpoints:
        print("Trying: " + endpoint)
        try:
            # 先尝试GET请求测试端点
            test_response = requests.get(endpoint, headers=headers, timeout=10)
            print("GET " + str(test_response.status_code))

            if test_response.status_code == 200:
                # 端点存在，尝试PUT更新
                update_response = requests.put(endpoint, headers=headers, json=payload, timeout=30)
                print("PUT " + str(update_response.status_code))
                if update_response.status_code == 200:
                    print("SUCCESS with endpoint: " + endpoint)
                    return True
        except Exception as e:
            print("Error with " + endpoint + ": " + str(e))

    return False

if __name__ == '__main__':
    update_kdocs()
