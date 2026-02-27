import requests
import time

from config import GRAPHQL_API_URL, MAX_RETRIES, RETRY_INTERVAL, REQUEST_TIMEOUT, build_headers
from utils.key import header_key_value
from utils.payload import payload_daily


def fetch_ranking():
    key_value = header_key_value()
    if not key_value:
        print("[API] 获取KEY失败，无法继续")
        return None
    
    headers = build_headers(key_value)
    pay_load = payload_daily()
    if not pay_load:
        print("[API] 获取Payload失败，无法继续")
        return None
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"[API] 第 {attempt + 1} 次请求...")
            response = requests.post(
                GRAPHQL_API_URL,
                headers=headers,
                json=pay_load,
                timeout=REQUEST_TIMEOUT
            )
            print(f"[API] 状态码: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[API] 响应内容: {response.text[:500]}")
        except requests.exceptions.RequestException as e:
            print(f"[API] 请求异常: {e}")
        
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_INTERVAL)
    
    print("[API] 所有重试失败")
    return None
