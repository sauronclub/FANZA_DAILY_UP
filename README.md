# FANZA每日榜单爬虫 - GitHub Actions版本

这是一个适配GitHub Actions自动运行的FANZA每日榜单爬虫工具。

## 功能特点

- 🔄 自动每日运行（UTC 2:00 / 日本时间 11:00）
- 📊 获取FANZA每日榜单数据
- 💾 保存HTML页面、电影列表和详细信息
- 🔧 保持原有的ID_PAYLOAD和headers生成方法不变
- 📋 完善的日志记录和错误处理
- 🚀 支持手动触发运行

## 文件结构

```
.
├── .github/workflows/daily-scraper.yml  # GitHub Actions工作流配置
├── main.py                              # 主爬虫程序（GitHub Actions优化版）
├── config.py                           # 配置文件（保持原有结构）
├── HEADERS.py                          # Headers生成模块（保持原有结构）
├── requirements.txt                    # Python依赖包列表
└── README.md                          # 说明文档
```

## 使用方法

### 1. 部署到GitHub仓库

1. Fork这个仓库或创建新仓库
2. 将所有文件上传到仓库
3. 确保文件结构正确

### 2. 配置GitHub Actions

工作流文件已经配置完成，位于 `.github/workflows/daily-scraper.yml`。

工作流会自动：
- 每天UTC时间2点运行
- 安装必要的Python依赖
- 运行爬虫程序
- 提交结果到仓库
- 上传运行结果作为artifacts

### 3. 环境变量配置

可以在GitHub仓库的Settings > Secrets and variables > Actions中设置以下环境变量：

- `LOG_LEVEL`: 日志级别（默认：INFO）
- `OUTPUT_DIR`: 输出目录（默认：./output）
- `MAX_HTML_RETRIES`: HTML获取重试次数（默认：3）
- `CONTENT_CHECK_INTERVAL`: 内容检查间隔秒数（默认：120）
- `MAX_CONTENT_CHECKS`: 最大内容检查次数（默认：20）
- `REQUEST_TIMEOUT`: 请求超时时间秒数（默认：10）

### 4. 手动运行

1. 进入GitHub仓库的Actions标签页
2. 选择"FANZA Daily Scraper"工作流
3. 点击"Run workflow"按钮

## 输出数据

爬虫会生成以下文件：

### 1. HTML文件
- 路径：`output/HTML/fanza_daily_{timestamp}.html`
- 内容：每日榜单页面的完整HTML

### 2. 电影列表
- 路径：`output/DATE/{date}.json`
- 内容：榜单电影的基本信息（排名和ID）

### 3. 电影详情
- 路径：`output/CID/{date}/{rank}_{movie_id}.json`
- 内容：每部电影的详细信息

### 4. 集計期間记录
- 路径：`output/H1/h1.txt`
- 内容：当前的集計期間信息

### 5. 日志文件
- 路径：`scraper.log`
- 内容：运行过程中的详细日志

## 开发说明

### 保持的原有功能
- ✅ ID_PAYLOAD数据结构完全不变
- ✅ headers生成方法保持原有逻辑
- ✅ 年龄验证流程
- ✅ 数据解析逻辑

### GitHub Actions适配
- 🆕 环境变量配置支持
- 🆕 结构化日志记录
- 🆕 错误处理和重试机制
- 🆕 自动提交结果
- 🆕 artifacts上传

### 自定义修改

如果需要修改爬虫行为，可以编辑：
- `main.py`: 主要逻辑和配置
- `config.py`: URL和payload配置
- `HEADERS.py`: 请求头生成逻辑
- `.github/workflows/daily-scraper.yml`: 工作流配置

## 注意事项

1. **网络限制**：确保GitHub Actions能够访问FANZA网站
2. **频率限制**：爬虫内置了延迟机制避免请求过快
3. **数据存储**：结果会自动提交到仓库，注意仓库大小限制
4. **隐私保护**：不要在日志中输出敏感信息

## 故障排除

### 常见问题

1. **运行失败**
   - 检查GitHub Actions日志
   - 验证网络连接
   - 检查环境变量配置

2. **数据获取失败**
   - 检查FANZA网站是否可访问
   - 验证年龄验证是否通过
   - 查看详细日志信息

3. **提交失败**
   - 检查GitHub Token权限
   - 验证仓库写入权限
   - 检查文件路径是否正确

### 日志查看

1. 进入GitHub仓库的Actions标签页
2. 选择对应的工作流运行
3. 查看步骤日志和artifacts

## 许可证

本项目仅供学习和研究使用。请遵守相关网站的使用条款和法律法规。