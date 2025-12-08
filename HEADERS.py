"""
HEADERS.py
自动拉取日本随机代理 IP 并生成完整请求头。
主程序只需：
    from HEADERS import headers
即可拿到带 X-Forwarded-For 的 headers。
"""
import os
import requests
import json
import random

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Cookie': 'age_check_done=1; ckcy=1',
#     'X-Forwarded-For': IP # 模拟来自日本的请求
# }



# ----------- 内部逻辑 -----------
# API_KEY = os.getenv("KEY_ENDPOINT")   # 远程接口，由环境变量注入
API_KEY = "https://raw.githubusercontent.com/sauronclub/global-ip-ranges/refs/heads/main/random_jp_ips.json"


def fetch_key_pool() -> list[str]:
    """拉取远程 KEY 池，失败直接抛异常，避免带着空 KEY 继续跑。"""
    try:
        resp = requests.get(
            API_KEY,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "token": "00000000",
                "key": "854624254"
            },
            timeout=10)
        resp.raise_for_status()
        return json.loads(resp.text)
    except Exception as e:
        raise RuntimeError(f"[HEADERS] 获取 KEY 池失败: {e}") from e


def build_headers(value: str) -> dict:
    """根据给定 IP 字符串生成完整 headers。"""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "ja-JP",
        "content-type": "application/json",
        #-------------------------------------------------
        # cookie 选择
        #--------测试使用
        # "cookie": "ckcy=1; age_check_done=1",
        #--------正式使用
        # "cookie": os.getenv("COOKIE"),
        #-------------------------------------------------

        "fanza-device": "BROWSER",
        "origin": "https://video.dmm.co.jp",
        "priority": "u=1, i",
        "referer": "https://video.dmm.co.jp/",
        "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }

    #-------------------------------------------------
    #--------测试使用
    xf_key = "X-Forwarded-For"
    #--------正式使用
    # xf_key = os.getenv("XF_HEADER")  # X-Forwarded-For
    #-------------------------------------------------

    headers[xf_key] = value
    return headers


# ----------- 模块级唯一执行点 -----------
KEY_POOL = fetch_key_pool()                   # 导入时只拉一次
HEADERS = build_headers(random.choice(KEY_POOL))  # 随机选一个 KEY 字符串

# ----------- 对外唯一接口 -----------
headers = HEADERS
print(headers)