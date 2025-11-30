import os, random, requests, logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

log = logging.getLogger(__name__)

def _rand_ip() -> str:
    try:
        return random.choice(requests.get(os.getenv("JP_IP_LIST_URL"), timeout=10).json())
    except Exception as e:
        log.warning("IP pool fail: %s", e)
        return "133.3.3.3"

def build_session() -> requests.Session:
    sess = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    sess.mount("https://", HTTPAdapter(max_retries=retry))
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": os.getenv("FANZA_COOKIE"),
        "X-Forwarded-For": _rand_ip(),
    })
    return sess