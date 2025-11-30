# Fanza Crawler - GitHub Actions 修复版

## 修复的问题

### 1. 目录结构问题
- **原问题**: 代码文件直接放在根目录，但导入路径使用了`src.`前缀
- **修复**: 按照RD.md的规范创建了正确的目录结构：
  ```
  src/
  ├── core/
  │   ├── session.py
  │   ├── gql.py
  │   └── storage.py
  ├── fanza/
  │   ├── auth.py
  │   ├── ranking.py
  │   ├── metadata.py
  │   └── model.py
  └── main.py
  ```

### 2. 缺少依赖文件
- **原问题**: 缺少`requirements.txt`文件，导致GitHub Actions的`pip install`步骤失败
- **修复**: 添加了`requirements.txt`包含必要的依赖包：
  - `requests`: HTTP请求库
  - `python-dotenv`: 环境变量管理
  - `beautifulsoup4`: HTML解析
  - `lxml`: XML/HTML解析器

### 3. GitHub Actions配置改进
- **新增**: 创建输出目录的步骤(`mkdir -p HTML DATE CID H1`)
- **新增**: pip缓存配置，加快构建速度
- **优化**: 改进了artifact上传路径配置
- **修复**: 确保工作目录设置正确

### 4. 环境变量配置
- **新增**: `.env.example`文件，提供环境变量配置模板
- **说明**: 需要在GitHub仓库的Settings > Secrets and variables中配置：
  - `FANZA_COOKIE`: 必需的认证cookie
  - `JP_IP_LIST_URL`: 日本IP列表URL
  - `RANKING_URL`: 排行榜URL
  - `GQL_URL`: GraphQL API地址
  - `MAX_WORKERS`: 最大工作线程数

## 使用方法

### 本地测试
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件填入必要的值

# 运行爬虫
cd src && python main.py
```

### GitHub Actions部署
1. Fork此仓库
2. 在GitHub仓库的Settings > Secrets and variables中配置环境变量
3. Actions会自动按UTC 14:30每日运行，或手动触发

## 输出文件
程序会生成以下输出：
- `HTML/`: HTML格式结果文件
- `DATE/`: JSON格式数据文件
- `CID/`: 内容ID相关文件
- `H1/`: 标题信息文件

## 注意事项
- 确保`FANZA_COOKIE`是有效且最新的
- 检查目标网站的服务条款，确保爬虫行为符合规定
- 建议设置合理的请求间隔，避免对目标服务器造成过大压力