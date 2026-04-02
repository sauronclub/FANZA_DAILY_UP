import requests
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL")


class NotifyStatus:
    START = "start"
    WAITING = "waiting"
    SUCCESS = "success"
    NO_CHANGE = "no_change"
    FAILURE = "failure"


def send_feishu_notification(
    status=NotifyStatus.SUCCESS,
    ranking_list=None,
    changes=None,
    wait_info=None,
    error_message=None
):
    if not FEISHU_WEBHOOK_URL:
        print("[NOTIFY] 未配置飞书 Webhook URL，跳过通知")
        return False

    status_config = {
        NotifyStatus.START: ("🔄 开始爬取", "blue"),
        NotifyStatus.WAITING: ("⏳ 等待重试", "orange"),
        NotifyStatus.SUCCESS: ("✅ 爬取成功", "green"),
        NotifyStatus.NO_CHANGE: ("📊 数据无变化", "grey"),
        NotifyStatus.FAILURE: ("❌ 爬取失败", "red"),
    }

    title, color = status_config.get(status, ("📋 通知", "grey"))

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content_rows = []

    if status == NotifyStatus.START:
        content_rows.append([{"tag": "text", "text": title}])
        content_rows.append([{"tag": "text", "text": f"时间: {run_time}"}])
        content_rows.append([{"tag": "text", "text": "正在爬取 FANZA 排行榜数据..."}])

    elif status == NotifyStatus.WAITING:
        content_rows.append([{"tag": "text", "text": title}])
        content_rows.append([{"tag": "text", "text": f"时间: {run_time}"}])
        content_rows.append([{"tag": "text", "text": wait_info}])

    elif status == NotifyStatus.SUCCESS:
        content_rows.append([{"tag": "text", "text": title}])
        content_rows.append([{"tag": "text", "text": f"时间: {run_time}"}])
        if ranking_list:
            content_rows.append([{"tag": "text", "text": "今日排行榜 TOP 20:"}])
            for item in ranking_list:
                rank = item.get("rank", "?")
                title_text = item.get("title", "未知标题")
                content_rows.append([{"tag": "text", "text": f"{rank:02d}、{title_text}"}])

    elif status == NotifyStatus.NO_CHANGE:
        content_rows.append([{"tag": "text", "text": title}])
        content_rows.append([{"tag": "text", "text": f"时间: {run_time}"}])
        if ranking_list:
            content_rows.append([{"tag": "text", "text": "今日排行榜 TOP 20 (与昨日相同):"}])
            for item in ranking_list:
                rank = item.get("rank", "?")
                title_text = item.get("title", "未知标题")
                content_rows.append([{"tag": "text", "text": f"{rank:02d}、{title_text}"}])

    elif status == NotifyStatus.FAILURE:
        content_rows.append([{"tag": "text", "text": title}])
        content_rows.append([{"tag": "text", "text": f"时间: {run_time}"}])
        if error_message:
            content_rows.append([{"tag": "text", "text": f"错误: {error_message}"}])

    if changes:
        content_rows.append([{"tag": "text", "text": "排名变化:"}])
        for change in changes:
            rank = change.get("rank")
            old_title = change.get("old_title", "未知")
            new_title = change.get("new_title", "未知")
            content_rows.append([{"tag": "text", "text": f"第 {rank} 名: {old_title} → {new_title}"}])

    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"FANZA 排行榜爬虫 - {title}",
                    "content": content_rows
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

        if result.get("code") == 0 or result.get("status_code") == 0:
            print("[NOTIFY] 飞书通知发送成功")
            return True
        else:
            print(f"[NOTIFY] 飞书通知发送失败: {result}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[NOTIFY] 飞书通知请求异常: {e}")
        return False
