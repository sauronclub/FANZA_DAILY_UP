#!/usr/bin/env python3
"""
FANZA每日榜单爬虫 - GitHub Actions版本
适配GitHub Actions环境，支持环境变量配置和日志记录
"""

import requests
import json
import os
import time
import random
import logging
import sys
from datetime import datetime
from pyquery import PyQuery as pq
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

# 导入配置和headers（保持原有结构不变）
from config import FANZA_DAILY_URL, FANZA_API_URL, FANZA_VIDEO_URL, ID_PAYLOAD
from HEADERS import headers

# 配置日志
def setup_logging():
    """设置日志记录"""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # 控制台输出
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('scraper.log', encoding='utf-8')
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

@dataclass
class Config:
    """配置类 - 支持环境变量"""
    max_html_retries: int = 3
    max_age_verification_retries: int = 5
    content_check_interval: int = 120  # 秒
    max_content_checks: int = 20
    request_timeout: int = 10
    retry_base_delay: float = 1.0
    output_dir: str = os.getenv('OUTPUT_DIR', './output')
    
    def __post_init__(self):
        """从环境变量覆盖配置"""
        self.max_html_retries = int(os.getenv('MAX_HTML_RETRIES', self.max_html_retries))
        self.content_check_interval = int(os.getenv('CONTENT_CHECK_INTERVAL', self.content_check_interval))
        self.max_content_checks = int(os.getenv('MAX_CONTENT_CHECKS', self.max_content_checks))
        self.request_timeout = int(os.getenv('REQUEST_TIMEOUT', self.request_timeout))
        self.retry_base_delay = float(os.getenv('RETRY_BASE_DELAY', self.retry_base_delay))

config = Config()

class FanzaScraper:
    """FANZA爬虫主类 - GitHub Actions优化版"""
    
    def __init__(self):
        self.session: Optional[requests.Session] = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.dirs = self._setup_directories()
        logger.info(f"初始化爬虫，输出目录: {config.output_dir}")
        
    def _setup_directories(self) -> Dict[str, str]:
        """设置并创建必要的目录"""
        dirs = {
            'html': os.path.join(config.output_dir, "HTML"),
            'date': os.path.join(config.output_dir, "DATE"),
            'h1': os.path.join(config.output_dir, "H1"),
            'cid': os.path.join(config.output_dir, "CID"),
            'logs': os.path.join(config.output_dir, "logs")
        }
        
        for dir_path in dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            logger.debug(f"创建目录: {dir_path}")
        
        return dirs
    
    def initialize_session(self) -> bool:
        """初始化会话并进行年龄验证"""
        self.session = requests.Session()
        
        try:
            logger.info("正在创建会话并进行年龄验证...")
            response = self.session.get(
                FANZA_VIDEO_URL, 
                headers=headers, 
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            if self._needs_age_verification(response):
                return self._handle_age_verification(response)
            
            logger.info("年龄验证已完成")
            return True
            
        except Exception as e:
            logger.error(f"会话初始化失败: {str(e)}")
            return False
    
    def _needs_age_verification(self, response: requests.Response) -> bool:
        """检查是否需要年龄验证"""
        return "age_check" in response.url or "年齢認証" in response.text
    
    def _handle_age_verification(self, response: requests.Response) -> bool:
        """处理年龄验证流程"""
        logger.info("检测到年龄验证页面，正在处理...")
        
        try:
            doc = pq(response.text)
            yes_button = doc('a[href*="declared=yes"]')
            
            if not yes_button:
                logger.error("未找到年龄验证按钮")
                return False
            
            verification_url = yes_button.attr('href')
            if verification_url and not verification_url.startswith('http'):
                verification_url = urljoin(response.url, verification_url)
            
            logger.info("正在提交年龄验证...")
            verify_response = self.session.get(
                verification_url, 
                headers=headers, 
                timeout=config.request_timeout
            )
            verify_response.raise_for_status()
            
            logger.info("年龄验证成功")
            return True
            
        except Exception as e:
            logger.error(f"年龄验证失败: {str(e)}")
            return False
    
    def fetch_daily_html(self) -> Optional[str]:
        """获取每日榜单HTML内容"""
        for attempt in range(config.max_html_retries):
            try:
                logger.info(f"正在获取每日榜单内容 (尝试 {attempt + 1}/{config.max_html_retries})...")
                
                response = self.session.get(
                    FANZA_DAILY_URL,
                    headers=headers,
                    timeout=config.request_timeout
                )
                response.raise_for_status()
                
                if self._is_valid_content(response.text):
                    logger.info(f"成功获取内容，状态码: {response.status_code}")
                    return response.text
                
                logger.warning("获取到无效内容（可能是年龄验证页面）")
                if attempt < config.max_html_retries - 1:
                    delay = config.retry_base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"等待 {delay:.1f} 秒后重试...")
                    time.sleep(delay)
                
            except Exception as e:
                logger.error(f"第 {attempt + 1} 次尝试失败: {str(e)}")
                if attempt < config.max_html_retries - 1:
                    delay = config.retry_base_delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
        
        logger.error("获取HTML内容失败")
        return None
    
    def _is_valid_content(self, html_content: str) -> bool:
        """验证内容是否有效"""
        if not html_content:
            return False
        
        try:
            doc = pq(html_content)
            page_title = doc('title').text()
            
            # 检查是否为年龄验证页面
            if "年齢認証" in page_title or "age_check" in page_title:
                logger.warning(f"检测到年龄验证页面: {page_title}")
                return False
            
            # 检查是否包含必要的元素
            period_span = doc('h1.headline.left span.nw').eq(1)
            if not period_span.text():
                logger.warning("未找到集計期間信息")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"内容验证失败: {str(e)}")
            return False
    
    def extract_page_info(self, html_content: str) -> Tuple[Optional[str], Optional[str], Optional[pq], Optional[str]]:
        """提取页面信息，返回（集計期間文本，页面标题，PyQuery对象，格式化日期）"""
        try:
            doc = pq(html_content)
            page_title = doc('title').text()
            
            # 提取集計期間
            period_span = doc('h1.headline.left span.nw').eq(1)
            period_text = period_span.text()
            
            if not period_text:
                logger.error("无法提取集計期間信息")
                return None, None, None, None
            
            # 提取并转换结束日期
            span_date = None
            try:
                end_date_str = period_text.split("：")[-1].split("～")[-1].strip().split(" ")[0]
                span_date = end_date_str.replace("/", "-")
                
                # 简单校验日期格式
                if len(span_date) != 10 or span_date.count("-") != 2:
                    raise ValueError(f"日期格式异常: {span_date}")
                
            except Exception as e:
                logger.warning(f"日期提取/转换失败: {str(e)}，原始文本: {period_text}")
                span_date = None
            
            logger.info(f"页面标题: {page_title}")
            logger.info(f"页面集計期間: {period_text}")
            if span_date:
                logger.info(f"提取到格式化日期: {span_date}")
            else:
                logger.info("未提取到有效日期，将使用当前系统日期")
            
            return period_text, page_title, doc, span_date
            
        except Exception as e:
            logger.error(f"提取页面信息失败: {str(e)}")
            return None, None, None, None
    
    def save_html_file(self, html_content: str, period_text: str, page_title: str, doc: pq) -> bool:
        """保存HTML文件"""
        try:
            # 检查是否需要保存
            if self._should_skip_saving(page_title):
                logger.warning("页面内容不适合保存，跳过")
                return False
            
            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(self.dirs['html'], f'fanza_daily_{timestamp}.html')
            
            content_to_save = str(doc) if doc else html_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_to_save)
            
            logger.info(f"HTML文件已保存: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存HTML文件失败: {str(e)}")
            return False
    
    def _should_skip_saving(self, page_title: str) -> bool:
        """检查是否应该跳过保存"""
        skip_keywords = ["年齢認証", "地域"]
        return any(keyword in page_title for keyword in skip_keywords)
    
    def parse_movie_list(self, doc: pq) -> List[Dict[str, str]]:
        """解析电影列表"""
        try:
            movie_items = doc('td.bd-b')
            movie_list = []
            
            for item in movie_items:
                rank = pq(item)('span.rank').text()
                movie_link = pq(item)('a').attr('href')
                
                if movie_link:
                    movie_id = movie_link.split('cid=')[-1].split('/')[0]
                    movie_list.append({
                        "rank": rank,
                        "id": movie_id
                    })
            
            logger.info(f"解析到 {len(movie_list)} 部电影")
            return movie_list
            
        except Exception as e:
            logger.error(f"解析电影列表失败: {str(e)}")
            return []
    
    def save_movie_list(self, movie_list: List[Dict[str, str]], date_str: str) -> bool:
        """保存电影列表到文件"""
        try:
            file_path = os.path.join(self.dirs['date'], f"{date_str}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(movie_list, f, ensure_ascii=False, indent=2)
            
            logger.info(f"电影列表已保存: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存电影列表失败: {str(e)}")
            return False
    
    def get_movie_details(self, movie_id: str) -> Optional[Dict]:
        """获取电影详情"""
        try:
            payload = ID_PAYLOAD.copy()
            payload["variables"] = {
                "id": movie_id,
                "isLoggedIn": False,
                "isAmateur": False,
                "isAnime": False,
                "isAv": True,
                "isCinema": False,
                "isSP": False,
                "shouldFetchRelatedTags": False,
                "isPhase4_2Released": False
            }
            
            response = self.session.post(
                FANZA_API_URL,
                headers=headers,
                json=payload,
                timeout=config.request_timeout
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"获取电影 {movie_id} 详情失败: {str(e)}")
            return None
    
    def save_movie_details(self, movie_details: Dict, rank: str, movie_id: str, date_str: str) -> bool:
        """保存电影详情"""
        try:
            cid_dir = os.path.join(self.dirs['cid'], date_str)
            os.makedirs(cid_dir, exist_ok=True)
            
            file_name = f"{str(rank).zfill(2)}_{movie_id}.json"
            file_path = os.path.join(cid_dir, file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(movie_details, f, ensure_ascii=False, indent=2)
            
            logger.info(f"已保存电影详情: {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"保存电影详情失败: {str(e)}")
            return False
    
    def get_previous_period(self) -> str:
        """获取之前的集計期間"""
        h1_file = os.path.join(self.dirs['h1'], "h1.txt")
        try:
            with open(h1_file, encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return ""
    
    def save_current_period(self, period_text: str) -> bool:
        """保存当前集計期間"""
        try:
            h1_file = os.path.join(self.dirs['h1'], "h1.txt")
            with open(h1_file, "w", encoding="utf-8") as f:
                f.write(period_text)
            return True
        except Exception as e:
            logger.error(f"保存集計期間失败: {str(e)}")
            return False

def main():
    """主函数 - GitHub Actions优化版"""
    logger.info("=" * 60)
    logger.info(" FANZA每日榜单爬虫启动 - GitHub Actions版本")
    logger.info("=" * 60)
    
    # 检查是否在GitHub Actions环境中运行
    is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
    if is_github_actions:
        logger.info("检测到GitHub Actions环境")
    
    scraper = FanzaScraper()
    
    # 初始化
    if not scraper.initialize_session():
        logger.error("程序初始化失败，退出")
        sys.exit(1)
    
    previous_period = scraper.get_previous_period()
    logger.info(f"上次集計期間: {previous_period if previous_period else '无记录'}")
    
    # 内容检查循环
    for check_count in range(config.max_content_checks):
        logger.info(f"\n>>> 第 {check_count + 1} 次内容检查")
        
        # 获取HTML内容
        html_content = scraper.fetch_daily_html()
        if not html_content:
            logger.error("无法获取HTML内容，退出")
            sys.exit(1)
        
        # 提取页面信息
        period_text, page_title, doc, span_date = scraper.extract_page_info(html_content)
        if not all([period_text, page_title, doc]):
            logger.error("页面信息提取失败，退出")
            sys.exit(1)
        
        logger.info(f"当前集計期間: {period_text}")
        
        # 保存HTML文件
        scraper.save_html_file(html_content, period_text, page_title, doc)
        
        # 检查内容是否变化
        if period_text == previous_period:
            logger.info(f"内容未变化，等待 {config.content_check_interval} 秒后重试")
            time.sleep(config.content_check_interval)
            continue
        
        # 内容已更新，处理新内容
        logger.info("🎉 检测到新内容，开始处理...")
        
        # 解析电影列表
        movie_list = scraper.parse_movie_list(doc)
        if not movie_list:
            logger.warning("电影列表为空，跳过")
            break
        
        # 确定最终使用的日期
        final_date = span_date if span_date else time.strftime("%Y-%m-%d")
        
        # 保存电影列表
        scraper.save_movie_list(movie_list, final_date)
        
        # 保存新的集計期間
        scraper.save_current_period(period_text)
        
        # 获取并保存每部电影的详情
        success_count = 0
        for i, movie in enumerate(movie_list):
            movie_id = movie["id"]
            rank = movie["rank"]
            
            logger.info(f"正在获取电影 {movie_id} 的详情... ({i+1}/{len(movie_list)})")
            details = scraper.get_movie_details(movie_id)
            
            if details:
                if scraper.save_movie_details(details, rank, movie_id, final_date):
                    success_count += 1
            
            # 添加小延迟避免请求过快
            time.sleep(0.5)
        
        logger.info(f"✅ 处理完成！成功获取 {success_count}/{len(movie_list)} 部电影详情")
        logger.info(f"📅 数据存储日期：{final_date}")
        
        # GitHub Actions环境中只运行一次
        if is_github_actions:
            break
        
        return
    
    logger.info("达到最大检查次数，内容无变化，任务结束")

if __name__ == "__main__":
    main()