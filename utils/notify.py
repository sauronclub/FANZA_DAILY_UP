import requests
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")


def send_feishu_notification(
    status="success",
    message="",
    data_count=0,
    change_count=0,
    error_message=None
):
    if not FEISHU_WEBHOOK_URL:
        print("[NOTIFY] 未配置飞书 Webhook URL，跳过通知")
        return False

    status_text = "✅ 成功" if status == "success" else "❌ 失败"
    status_color = "green" if status == "success" else "red"

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content_lines = [
        {
            "tag": "text",
            "text": f"**运行状态:** {status_text}"
        },
        {
            "tag": "text",
            "text": f"**运行时间:** {run_time}"
        },
        {
            "tag": "text",
            "text": f"**数据条数:** {data_count} 条"
        }
    ]

    if change_count > 0:
        content_lines.append({
            "tag": "text",
            "text": f"**排名变化:** 检测到 {change_count} 处变化"
        })
    elif status == "success":
        content_lines.append({
            "tag": "text",
            "text": "**排名变化:** 数据无变化"
        })

    if message:
        content_lines.append({
            "tag": "text",
            "text": f"**备注:** {message}"
        })

    if error_message:
        content_lines.append({
            "tag": "text",
            "text": f"**错误信息:** {error_message}"
        })

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"FANZA 排行榜爬虫 - {status_text}",
                    "content": [
                        content_lines
                    ]
                }
            }
        }
    }

    try:
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json=payload,
            timeout=10
        )
        result = response.json()

        if result.get("code") == 0 or result.get("StatusCode") == 0:
            print("[NOTIFY] 飞书通知发送成功")
            return True
        else:
            print(f"[NOTIFY] 飞书通知发送失败: {result}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[NOTIFY] 飞书通知请求异常: {e}")
        return False
