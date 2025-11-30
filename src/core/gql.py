import requests, logging, os
from typing import Dict, Any

log = logging.getLogger(__name__)
GQL_URL = os.getenv("GQL_URL")

# 精简后的查询，够用即可
QUERY = """
query($id:ID!){ppvContent(id:$id){
  id title packageImage{largeUrl} actresses{id name}
  reviewSummary{average total}
}}
"""

def fetch_detail(sess: requests.Session, cid: str) -> Dict[str, Any]:
    resp = sess.post(
        GQL_URL,
        json={"query": QUERY, "variables": {"id": cid}},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]["ppvContent"]