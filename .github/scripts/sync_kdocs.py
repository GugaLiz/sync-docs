#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/sync_kdocs_compatible.py

import os
import requests
import sys

def update_kdocs():
    access_token = "jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH"
    document_id = 'cjpVZz0ASxGp'

    if not access_token:
        print("ERROR: KDOCS_ACCESS_TOKEN environment variable is required")
        sys.exit(1)

    try:
        # Read README content
        print("Reading README.md...")
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        print("Content size: " + str(len(content)) + " characters")

        # Prepare API request
        api_url = "https://open.kdocs.cn/api/v1/documents/" + document_id + "/content"
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        payload = {"content": content}

        # Send request
        print("Sending update request...")
        response = requests.put(api_url, headers=headers, json=payload, timeout=30)

        # Check response
        if response.status_code == 200:
            print("SUCCESS: Document updated successfully")
            result = response.json()
            print("Response: " + json.dumps(result))
            sys.exit(0)
        else:
            print("FAILED: API returned status " + str(response.status_code))
            print("Response: " + response.text)
            sys.exit(1)

    except FileNotFoundError:
        print("ERROR: README.md file not found")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print("ERROR: Request failed - " + str(e))
        sys.exit(1)
    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(1)

if __name__ == '__main__':
    update_kdocs()
