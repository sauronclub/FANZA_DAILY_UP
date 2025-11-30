import os, logging, time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from src.core import storage
from src.core.session import build_session
from src.fanza import auth, ranking, metadata

# ---------- 新增：预创建四目录 ----------
REPO_ROOT = Path(__file__).parent.parent   # 仓库根
for d in ("HTML", "DATE", "CID", "H1"):
    (REPO_ROOT / d).mkdir(exist_ok=True)
# ---------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
load_dotenv()

RANKING_URL = os.getenv("RANKING_URL")
H1_FILE     = "H1/h1.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
load_dotenv()  # 本地调试

RANKING_URL = os.getenv("RANKING_URL")
H1_FILE     = "H1/h1.txt"

def main():
    sess = build_session()
    if not auth.age_verify(sess):
        raise RuntimeError("age verify failed")

    period, movies = ranking.fetch_daily(sess, RANKING_URL)

    # 幂等
    old = ""
    try:
        old = storage.read(H1_FILE)
    except FileNotFoundError:
        pass
    if period == old:
        logging.info("ranking not updated  exit")
        return

    date_str = datetime.strptime(
        period.split("～")[-1].strip().split()[0], "%Y/%m/%d"
    ).strftime("%Y-%m-%d")

    # 落盘
    storage.write(H1_FILE, period)
    storage.write(f"DATE/{date_str}.json", movies)
    html_path = f"HTML/fanza_daily_{datetime.now():%Y%m%d%H%M%S}.html"
    storage.write(html_path, "")   # 占位，如需真实 html 把 r.text 写进来
    metadata.fetch_and_save(movies, date_str)

    logging.info("all done  date=%s", date_str)


if __name__ == "__main__":

    main()
