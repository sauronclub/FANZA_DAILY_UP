import logging, requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin

log = logging.getLogger(__name__)
ENTRY = "https://video.dmm.co.jp/av/"

def age_verify(sess: requests.Session) -> bool:
    """返回 True 表示已成年可继续"""
    log.info("checking age verification …")
    r = sess.get(ENTRY, timeout=10)
    if "age_check" not in r.url and "年齢認証" not in r.text:
        return True  # 无需认证
    doc = pq(r.text)
    href = doc('a[href*="declared=yes"]').attr("href")
    if not href:
        log.error("未找到成年按钮")
        return False
    url = urljoin(r.url, href)
    sess.get(url, timeout=10)
    log.info("age verification passed")
    return True