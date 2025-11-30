import os, logging, concurrent.futures
from typing import List
from ..core import gql, storage
from .model import Movie

log = logging.getLogger(__name__)
MAX_W = int(os.getenv("MAX_WORKERS") or 5)

def fetch_and_save(movies: List[Movie], date: str):
    from ..core.session import build_session
    sess = build_session()

    def job(m: Movie):
        try:
            data = gql.fetch_detail(sess, m["id"])
            storage.write(f"CID/{date}/{int(m['rank']):02d}_{m['id']}.json", data)
            return True
        except Exception as e:
            log.warning("fail on %s: %s", m["id"], e)
            return False

    with concurrent.futures.ThreadPoolExecutor(MAX_W) as exe:
        ok = sum(exe.map(job, movies))
    log.info("metadata finished  %s/%s", ok, len(movies))