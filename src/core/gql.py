import os, requests, logging
from typing import Dict, Any

log = logging.getLogger(__name__)
URL = os.getenv("GQL_URL")

QUERY = """
query($id:ID!){ppvContent(id:$id){
  id title packageImage{largeUrl} actresses{id name}
  reviewSummary{average total}
}}
"""

def fetch_detail(sess: requests.Session, cid: str) -> Dict[str, Any]:
    resp = sess.post(URL, json={"query": QUERY, "variables": {"id": cid}}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]["ppvContent"]