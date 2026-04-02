import sys
import time
from datetime import datetime

from config import COMPARE_RETRY_COUNT, COMPARE_RETRY_INTERVAL
from utils.api import fetch_ranking
from utils.parser import parse_ranking_items
from utils.storage import save_to_json
from utils.compare import is_data_changed, compare_items, load_previous_data
from utils.notify import send_feishu_notification, NotifyStatus


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def format_ranking_list(items):
    ranking_list = []
    for item in items:
        rank = item.get("rank", "?")
        content = item.get("content", {})
        title = content.get("title", "未知标题")
        ranking_list.append({"rank": rank, "title": title})
    return ranking_list


def main():
    log("=" * 50)
    log("FANZA Daily Ranking Crawler")
    log("=" * 50)

    send_feishu_notification(status=NotifyStatus.START)
    log("[NOTIFY] 已发送开始通知")

    exit_code = 0
    error_message = None

    for attempt in range(COMPARE_RETRY_COUNT):
        log(f"第 {attempt + 1}/{COMPARE_RETRY_COUNT} 次尝试")

        data = fetch_ranking()
        if not data:
            log("获取数据失败")
            if attempt < COMPARE_RETRY_COUNT - 1:
                wait_msg = f"数据获取失败，{COMPARE_RETRY_INTERVAL} 秒后重试... ({attempt + 1}/{COMPARE_RETRY_COUNT})"
                log(wait_msg)
                send_feishu_notification(status=NotifyStatus.WAITING, wait_info=wait_msg)
                time.sleep(COMPARE_RETRY_INTERVAL)
            continue

        items = parse_ranking_items(data)
        if not items:
            log("解析数据失败")
            if attempt < COMPARE_RETRY_COUNT - 1:
                wait_msg = f"数据解析失败，{COMPARE_RETRY_INTERVAL} 秒后重试... ({attempt + 1}/{COMPARE_RETRY_COUNT})"
                log(wait_msg)
                send_feishu_notification(status=NotifyStatus.WAITING, wait_info=wait_msg)
                time.sleep(COMPARE_RETRY_INTERVAL)
            continue

        old_items = load_previous_data()
        is_changed, changes = compare_items(items, old_items)

        if is_changed:
            filepath = save_to_json(items)
            if filepath:
                ranking_list = format_ranking_list(items)
                log("=" * 50)
                log(f"完成! 共处理 {len(items)} 条数据")

                if changes:
                    log(f"检测到 {len(changes)} 处排名变化")
                    send_feishu_notification(
                        status=NotifyStatus.SUCCESS,
                        ranking_list=ranking_list,
                        changes=changes
                    )
                else:
                    log("首次运行或数据结构变化")
                    send_feishu_notification(
                        status=NotifyStatus.SUCCESS,
                        ranking_list=ranking_list
                    )
                log("=" * 50)
            break
        else:
            if attempt < COMPARE_RETRY_COUNT - 1:
                wait_msg = f"数据无变化，{COMPARE_RETRY_INTERVAL} 秒后重试... ({attempt + 1}/{COMPARE_RETRY_COUNT})"
                log(wait_msg)
                send_feishu_notification(status=NotifyStatus.WAITING, wait_info=wait_msg)
                time.sleep(COMPARE_RETRY_INTERVAL)
            else:
                log("已达最大重试次数，保存当前数据")
                save_to_json(items)
                ranking_list = format_ranking_list(items)
                send_feishu_notification(
                    status=NotifyStatus.NO_CHANGE,
                    ranking_list=ranking_list
                )
                break
    else:
        exit_code = 1
        error_message = "所有重试次数用尽，程序退出"
        send_feishu_notification(
            status=NotifyStatus.FAILURE,
            error_message=error_message
        )

    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
