import os
import json
from datetime import date, timedelta


def get_latest_json_file(output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "TOP")

    if not os.path.exists(output_dir):
        return None

    json_files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
    if not json_files:
        return None

    json_files.sort(reverse=True)

    today_str = date.today().strftime("%Y-%m-%d")
    for f in json_files:
        if today_str in f:
            continue
        return os.path.join(output_dir, f)

    return None


def load_previous_data(output_dir=None):
    filepath = get_latest_json_file(output_dir)
    if not filepath:
        print(f"-"*100)
        print(f"[COMPARE] 未找到历史数据文件")
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"-"*100)
        print(f"[COMPARE] 加载历史数据: {os.path.basename(filepath)}")
        return data
    except Exception as e:
        print(f"[COMPARE] 读取历史数据失败: {e}")
        return None


def compare_items(new_items, old_items):
    if not old_items:
        return True, []

    new_ids = [item.get("id") for item in new_items if item.get("id")]
    old_ids = [item.get("id") for item in old_items if item.get("id")]

    if new_ids == old_ids:
        return False, []

    changes = []
    for i, (new_id, old_id) in enumerate(zip(new_ids, old_ids)):
        if new_id != old_id:
            changes.append({
                "rank": i + 1,
                "old_id": old_id,
                "new_id": new_id
            })

    return True, changes


def is_data_changed(new_items, output_dir=None):
    old_items = load_previous_data(output_dir)
    is_changed, changes = compare_items(new_items, old_items)

    if is_changed:
        if changes:
            print(f"[COMPARE] 检测到 {len(changes)} 处排名变化")
        else:
            print(f"[COMPARE] 首次运行或数据结构变化")
    else:
        print(f"[COMPARE] 数据未变化，与上次相同")

    return is_changed
