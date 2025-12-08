# 输出数据示例

## 1. 电影列表文件 (DATE/{date}.json)

```json
[
  {
    "rank": "1",
    "id": "h_068sbbbw00168"
  },
  {
    "rank": "2", 
    "id": "h_068sbbbw00169"
  },
  {
    "rank": "3",
    "id": "h_068sbbbw00170"
  }
]
```

## 2. 电影详情文件 (CID/{date}/{rank}_{movie_id}.json)

```json
{
  "data": {
    "ppvContent": {
      "id": "h_068sbbbw00168",
      "floor": "videoa",
      "title": "作品タイトル",
      "isExclusiveDelivery": true,
      "releaseStatus": "ON_SALE",
      "description": "作品説明文...",
      "packageImage": {
        "largeUrl": "https://example.com/image.jpg",
        "mediumUrl": "https://example.com/image_m.jpg",
        "__typename": "PackageImage"
      },
      "products": [
        {
          "id": "product_123",
          "productType": "RENTAL",
          "salesMethod": "STREAMING",
          "resolution": "HD",
          "duration": 120,
          "isHd": true,
          "__typename": "Product"
        }
      ],
      "performers": [
        {
          "id": "performer_456",
          "name": " performer name ",
          "ruby": "performer ruby",
          "__typename": "Performer"
        }
      ],
      "tags": [
        {
          "id": "tag_789",
          "name": "tag name",
          "__typename": "Tag"
        }
      ]
    },
    "reviewSummary": {
      "reviewCount": 150,
      "averageRating": 4.2,
      "__typename": "ReviewSummary"
    }
  }
}
```

## 3. 集計期間文件 (H1/h1.txt)

```
集計期間：2024年12月01日～2024年12月01日
```

## 4. HTML文件 (HTML/fanza_daily_{timestamp}.html)

完整的FANZA每日榜单页面HTML内容，包含：
- 页面标题和元数据
- 榜单表格结构
- 电影排名信息
- 样式和脚本

## 5. 日志文件 (scraper.log)

```
2024-12-08 10:00:00 - INFO - FANZA每日榜单爬虫启动 - GitHub Actions版本
2024-12-08 10:00:01 - INFO - 正在创建会话并进行年龄验证...
2024-12-08 10:00:03 - INFO - 年龄验证已完成
2024-12-08 10:00:05 - INFO - 正在获取每日榜单内容 (尝试 1/3)...
2024-12-08 10:00:07 - INFO - 成功获取内容，状态码: 200
```

## 数据更新频率

- **自动运行**: 每天UTC 2:00 (日本时间11:00)
- **手动触发**: 可以随时通过GitHub Actions页面手动运行
- **数据保留**: 每次运行都会生成新的文件，保留历史数据

## 数据使用说明

1. **电影列表**: 用于获取当日榜单的基本信息
2. **电影详情**: 包含完整的作品信息、演员、标签等
3. **HTML文件**: 用于验证数据完整性或重新解析
4. **日志文件**: 用于排查问题和监控运行状态

## 数据格式注意事项

- 所有JSON文件使用UTF-8编码
- 日期格式为 YYYY-MM-DD
- 排名使用零填充 (01, 02, 03...)
- 文件名中的特殊字符已处理