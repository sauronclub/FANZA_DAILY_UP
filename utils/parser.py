def parse_ranking_items(data):
    if not data:
        return []

    try:
        items = data.get("data", {}).get("ppvContentRanking", {}).get("items", [])
        print(f"[PARSER] 解析到 {len(items)} 条影片数据")

        for item in items:
            video_id = item.get("id")
            rank = item.get("rank")
            content = item.get("content", {})
            title = content.get("title")
            actresses = content.get("actresses", [])
            actresses_name = [a.get("name") for a in actresses if a.get("name")]

            print(f"-"*100)
            print(f"排名: {rank}")
            print(f"ID: {video_id}")
            print(f"标题: {title}")
            if actresses_name:
                print(f"演员: {', '.join(actresses_name)}")
        return items
    except Exception as e:
        print(f"[PARSER] 解析异常: {e}")
        return []
