import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GRAPHQL_API_URL = os.getenv("GRAPHQL_API_URL")
HEADER_KEY_VALUE_URL = os.getenv("HEADER_KEY_VALUE_URL")
PAYLOAD_DAILY_URL = os.getenv("PAYLOAD_DAILY_URL")
HEADER_KEY = os.getenv("HEADER_KEY")

MAX_RETRIES = 3
RETRY_INTERVAL = 3
REQUEST_TIMEOUT = 15
CACHE_EXPIRE_SECONDS = 3600

COMPARE_RETRY_COUNT = 5
COMPARE_RETRY_INTERVAL = 300

HEADERS_TEMPLATE = {
    "accept": "application/graphql-response+json, application/graphql+json, application/json, text/event-stream, multipart/mixed",
    "accept-language": "ja-JP",
    "content-type": "application/json",
    "cookie": "age_check_done=1; ckcy=1",
    "origin": "https://video.dmm.co.jp",
    "referer": "https://video.dmm.co.jp/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
}


def build_headers(header_key_value):
    headers = HEADERS_TEMPLATE.copy()
    if HEADER_KEY and header_key_value:
        headers[HEADER_KEY] = header_key_value
    return headers
