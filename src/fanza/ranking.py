import logging, requests
from pyquery import PyQuery as pq
from typing import List
from .model import Movie

log = logging.getLogger(__name__)

def fetch_daily(sess: requests.Session, url: str) -> tuple[str, List[Movie]]:
    """返回 (集計期間文本, [Movie, …])"""
    log.info("fetching ranking page …")
    r = sess.get(url, timeout=20)
    r.raise_for_status()
    doc = pq(r.text)
    period = doc("h1.headline.left span.nw").eq(1).text()
    if not period:
        raise ValueError("无法提取集計期間")
    movies: List[Movie] = []
    for td in doc("td.bd-b").items():
        rank = td("span.rank").text()
        href = td("a").attr("href")
        if not href:
            continue
        cid = href.split("cid=")[-1].split("/")[0]
        movies.append({"rank": rank, "id": cid})
    log.info("parsed %s movies, period=%s", len(movies), period)
    return period, movies