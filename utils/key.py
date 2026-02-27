import random
import requests
import time
from datetime import datetime, timedelta

from config import HEADER_KEY_VALUE_URL, MAX_RETRIES, RETRY_INTERVAL, REQUEST_TIMEOUT, CACHE_EXPIRE_SECONDS


_cache = {
    "keys": [],
    "last_fetch": None
}


def _fetch_keys():
    global _cache
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                HEADER_KEY_VALUE_URL,
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                _cache["keys"] = response.json()
                _cache["last_fetch"] = datetime.now()
                print(f"[KEY] 获取KEY列表成功")
                return True
            else:
                print(f"[KEY] 获取失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[KEY] 请求异常 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
        
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_INTERVAL)
    
    return False


def header_key_value():
    global _cache
    
    now = datetime.now()
    
    if (not _cache["keys"] or 
        not _cache["last_fetch"] or 
        (now - _cache["last_fetch"]).total_seconds() >= CACHE_EXPIRE_SECONDS):
        _fetch_keys()
    
    if _cache["keys"]:
        return random.choice(_cache["keys"])
    return None


def clear_cache():
    global _cache
    _cache = {"keys": [], "last_fetch": None}


if __name__ == "__main__":
    print(header_key_value())
