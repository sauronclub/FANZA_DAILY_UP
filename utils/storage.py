import os
import json
from datetime import date


def save_to_json(items, output_dir=None):
    if not items:
        print("[STORAGE] 无数据可保存")
        return None
    
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "..", "TOP")
    
    os.makedirs(output_dir, exist_ok=True)
    
    today = date.today().strftime("%Y-%m-%d")
    filename = f"rank_top{len(items)}_{today}.json"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"[STORAGE] 文件已保存: {filepath}")
        return filepath
    except Exception as e:
        print(f"[STORAGE] 保存失败: {e}")
        return None
