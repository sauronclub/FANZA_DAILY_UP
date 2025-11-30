import logging, requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin

log = logging.getLogger(__name__)
ENTRY = "https://video.dmm.co.jp/av/"

def age_verify(sess: requests.Session) -> bool:
    r = sess.get(ENTRY, timeout=10)
    if "age_check" not in r.url and "年齢認証" not in r.text:
        return True
    href = pq(r.text)('a[href*="declared=yes"]').attr("href")
    if not href:
        log.error("adult button not found")
        return False
    sess.get(urljoin(r.url, href), timeout=10)
    log.info("age verification passed")
    return True