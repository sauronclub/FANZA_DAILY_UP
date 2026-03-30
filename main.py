import sys
import time
from datetime import datetime

from config import COMPARE_RETRY_COUNT, COMPARE_RETRY_INTERVAL
from utils.api import fetch_ranking
from utils.parser import parse_ranking_items
from utils.storage import save_to_json
from utils.compare import is_data_changed, compare_items, load_previous_data


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def main():
    log("=" * 50)
    log("FANZA Daily Ranking Crawler")
    log("=" * 50)

    data_count = 0
    change_count = 0
    exit_code = 0
    error_message = None

    for attempt in range(COMPARE_RETRY_COUNT):
        log(f"第 {attempt + 1}/{COMPARE_RETRY_COUNT} 次尝试")

        data = fetch_ranking()
        if not data:
            log("获取数据失败")
            if attempt < COMPARE_RETRY_COUNT - 1:
                log(f"等待 {COMPARE_RETRY_INTERVAL} 秒后重试...")
                time.sleep(COMPARE_RETRY_INTERVAL)
            continue

        items = parse_ranking_items(data)
        if not items:
            log("解析数据失败")
            if attempt < COMPARE_RETRY_COUNT - 1:
                log(f"等待 {COMPARE_RETRY_INTERVAL} 秒后重试...")
                time.sleep(COMPARE_RETRY_INTERVAL)
            continue

        data_count = len(items)
        old_items = load_previous_data()
        is_changed, changes = compare_items(items, old_items)

        if is_changed:
            change_count = len(changes) if changes else 0
            filepath = save_to_json(items)
            if filepath:
                log("=" * 50)
                log(f"完成! 共处理 {len(items)} 条数据")
                if change_count > 0:
                    log(f"检测到 {change_count} 处排名变化")
                else:
                    log("数据无变化")
                log("=" * 50)
            break
        else:
            if attempt < COMPARE_RETRY_COUNT - 1:
                log(f"等待 {COMPARE_RETRY_INTERVAL} 秒后重试...")
                time.sleep(COMPARE_RETRY_INTERVAL)
            else:
                log("已达最大重试次数，保存当前数据")
                save_to_json(items)
                change_count = 0
                break
    else:
        exit_code = 1
        error_message = "所有重试次数用尽，程序退出"

    from utils.notify import send_feishu_notification
    send_feishu_notification(
        status="success" if exit_code == 0 else "failure",
        data_count=data_count,
        change_count=change_count,
        error_message=error_message
    )

    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
