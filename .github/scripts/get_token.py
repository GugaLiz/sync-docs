# 获取token的脚本 (get_token.py)
import requests

def get_access_token():
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    response = requests.post(
        "https://open.kdocs.cn/oauth/access_token",
        data={
            "client_id": "SX20251113HXLMYW",
            "client_secret": "jVSbQeGbpmBNsAFibSEaAFdAwZuKoYWH",
            "grant_type": "client_credentials"
        }
    )

    if response.status_code == 200:
        token_data = response.json()
        print(f"Access Token: {token_data['access_token']}")
        print(f"Expires in: {token_data['expires_in']} seconds")
        return token_data['access_token']
    else:
        print(f"Failed to get token: {response.text}")
        return None
