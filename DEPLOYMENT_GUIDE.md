# GitHub Actions 部署指南

## 快速部署步骤

### 1. 准备GitHub仓库

1. 在GitHub上创建新仓库
2. 将本目录下的所有文件上传到仓库

```bash
# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: FANZA scraper for GitHub Actions"

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 推送到GitHub
git push -u origin main
```

### 2. 启用GitHub Actions

1. 进入GitHub仓库页面
2. 点击 "Actions" 标签
3. 如果提示，启用GitHub Actions

### 3. 配置环境变量（可选）

如果需要自定义配置，可以设置环境变量：

1. 进入仓库的 Settings > Secrets and variables > Actions
2. 添加以下变量（可选）：
   - `LOG_LEVEL`: 日志级别 (DEBUG, INFO, WARNING, ERROR)
   - `OUTPUT_DIR`: 输出目录路径
   - `REQUEST_TIMEOUT`: 请求超时时间
   - `MAX_CONTENT_CHECKS`: 最大内容检查次数

### 4. 测试运行

1. 进入Actions标签页
2. 选择 "FANZA Daily Scraper" 工作流
3. 点击 "Run workflow" 手动触发一次

## 验证部署成功

### 检查工作流运行
- 工作流应该成功完成（绿色勾选标记）
- 检查运行日志确认没有错误

### 检查输出文件
- 确认 `output/` 目录被创建
- 检查是否有HTML、JSON等文件生成
- 查看提交历史确认数据被正确提交

### 检查定时运行
- 工作流会在每天UTC 2:00自动运行
- 可以在Actions页面查看定时运行情况

## 故障排除

### 工作流运行失败
1. 检查工作流日志
2. 验证网络连接是否正常
3. 检查依赖包是否正确安装

### 数据获取失败
1. 检查目标网站是否可访问
2. 验证headers是否正确生成
3. 查看详细日志信息

### 提交失败
1. 检查GitHub Token权限
2. 验证仓库写入权限
3. 检查文件路径是否正确

## 自定义配置

### 修改运行时间
编辑 `.github/workflows/daily-scraper.yml` 中的cron表达式：

```yaml
schedule:
  - cron: '0 2 * * *'  # 每天UTC 2点
```

### 修改输出结构
编辑 `main.py` 中的 `Config` 类和目录设置。

### 添加新功能
在保持原有ID_PAYLOAD和headers生成方法不变的前提下，可以自由修改其他逻辑。

## 监控和维护

### 监控运行状态
- 定期检查Actions运行状态
- 查看运行日志和artifacts
- 监控仓库大小（大量数据可能影响性能）

### 数据管理
- 定期清理旧的artifacts
- 考虑数据保留策略
- 监控存储使用情况

### 更新维护
- 定期更新依赖包版本
- 监控目标网站结构变化
- 根据需求调整爬虫逻辑

## 注意事项

1. **遵守法规**：确保使用方式符合相关法律法规
2. **网站条款**：尊重目标网站的使用条款
3. **请求频率**：已内置延迟机制，避免过于频繁的请求
4. **数据隐私**：不要在日志或提交中包含敏感信息
5. **仓库大小**：大量数据可能导致仓库变大，考虑定期清理

## 技术支持

如有问题，可以：
1. 查看GitHub Actions日志
2. 检查工作流配置文件
3. 验证代码逻辑
4. 查看测试脚本输出