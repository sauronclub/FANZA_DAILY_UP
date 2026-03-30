import requests
import time
from datetime import datetime

from config import PAYLOAD_DAILY_URL, MAX_RETRIES, RETRY_INTERVAL, REQUEST_TIMEOUT, CACHE_EXPIRE_SECONDS


_cache = {
    "payload": None,
    "last_fetch": None
}


def _fetch_payload():
    global _cache

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                PAYLOAD_DAILY_URL,
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                _cache["payload"] = response.json()
                _cache["last_fetch"] = datetime.now()
                print(f"[PAYLOAD] 获取Payload成功")
                return True
            else:
                print(f"[PAYLOAD] 获取失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[PAYLOAD] 请求异常 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_INTERVAL)

    return False


def payload_daily():
    global _cache

    now = datetime.now()

    if (not _cache["payload"] or
        not _cache["last_fetch"] or
        (now - _cache["last_fetch"]).total_seconds() >= CACHE_EXPIRE_SECONDS):
        _fetch_payload()

    return _cache["payload"]
