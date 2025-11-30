import os, logging, time
from datetime import datetime
from dotenv import load_dotenv
from src.core import storage
from src.core.session import build_session
from src.fanza import auth, ranking, metadata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)
load_dotenv()  # 本地调试时加载 .env

RANKING_URL = os.getenv("RANKING_URL")
H1_FILE = "h1.txt"  # 用于幂等判断


def main():
    sess = build_session()
    if not auth.age_verify(sess):
        raise RuntimeError("年龄认证失败")

    period, movies = ranking.fetch_daily(sess, RANKING_URL)
    old = ""
    try:
        old = storage.read(H1_FILE)
    except FileNotFoundError:
        pass
    if period == old:
        logging.info("榜单未更新，直接退出")
        return

    date = datetime.strptime(period.split("～")[-1].strip().split()[0], "%Y/%m/%d").strftime("%Y-%m-%d")
    storage.write(H1_FILE, period)  # 记录最新期号
    storage.write(f"{date}/ranking.json", movies)  # 备份榜单
    metadata.fetch_and_save(movies, date)
    logging.info("all done ✅ date=%s", date)


if __name__ == "__main__":
    main()