import sys
import time
from datetime import datetime

from config import COMPARE_RETRY_COUNT, COMPARE_RETRY_INTERVAL
from utils.api import fetch_ranking
from utils.parser import parse_ranking_items
from utils.storage import save_to_json
from utils.compare import is_data_changed


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def main():
    log("=" * 50)
    log("FANZA Daily Ranking Crawler")
    log("=" * 50)
    
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
        
        if is_data_changed(items):
            filepath = save_to_json(items)
            if filepath:
                log("=" * 50)
                log(f"完成! 共处理 {len(items)} 条数据")
                log("=" * 50)
            return 0
        else:
            if attempt < COMPARE_RETRY_COUNT - 1:
                log(f"等待 {COMPARE_RETRY_INTERVAL} 秒后重试...")
                time.sleep(COMPARE_RETRY_INTERVAL)
            else:
                log("已达最大重试次数，保存当前数据")
                save_to_json(items)
                return 0
    
    log("所有重试失败，程序退出")
    return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
