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


            # 打印影片信息，包含排名、ID、标题和演员，每项信息一行，排行一行、ID一行、标题一行、演员一行（如果有演员）
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
