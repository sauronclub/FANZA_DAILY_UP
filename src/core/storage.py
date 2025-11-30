import os, json, logging
from datetime import datetime

log = logging.getLogger(__name__)
ROOT = os.getenv("OUTPUT_ROOT")

def write(path: str, data: dict | str, indent=2):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        if isinstance(data, str):
            f.write(data)
        else:
            json.dump(data, f, ensure_ascii=False, indent=indent)
    log.debug("saved -> %s", full)