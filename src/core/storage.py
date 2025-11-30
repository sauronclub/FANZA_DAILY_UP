import os, json, logging
from pathlib import Path

log = logging.getLogger(__name__)
ROOT = Path(os.getenv("OUTPUT_ROOT"))

def write(path: str, data: dict | str, indent: int | None = 2):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        full.write_text(data, encoding="utf-8")
    else:
        full.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")
    log.debug("saved -> %s", full)

def read(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        raise FileNotFoundError(full)
    return full.read_text(encoding="utf-8")