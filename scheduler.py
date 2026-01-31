# -*- coding: utf-8 -*-
"""
定时爬虫调度器
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import atexit
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from urllib.parse import urljoin, urlparse
from typing import List, Dict
from models import (
    init_db, insert_news, get_violation_stats, get_case_stats,
    get_region_stats, get_news, log_crawl, get_all_tags
)

# 地区配置
REGIONS = {
    "xian": {"name": "西安市", "domain": "xian.qinfeng.gov.cn", "path": "scdc.htm"},
    "baoji": {"name": "宝鸡市", "domain": "baoji.qinfeng.gov.cn", "path": "scdc.htm"},
    "xianyang": {"name": "咸阳市", "domain": "xianyang.qinfeng.gov.cn", "path": "scdc.htm"},
    "tongchuan": {"name": "铜川市", "domain": "tongchuan.qinfeng.gov.cn", "path": "scdc.htm"},
    "weinan": {"name": "渭南市", "domain": "weinan.qinfeng.gov.cn", "path": "scdc.htm"},
    "yanan": {"name": "延安市", "domain": "yanan.qinfeng.gov.cn", "path": "scdc.htm"},
    "yulin": {"name": "榆林市", "domain": "yulin.qinfeng.gov.cn", "path": "scdc.htm"},
    "hanzhong": {"name": "汉中市", "domain": "hanzhong.qinfeng.gov.cn", "path": "scdc.htm"},
    "ankang": {"name": "安康市", "domain": "ankang.qinfeng.gov.cn", "path": "scdc.htm"},
    "shangluo": {"name": "商洛市", "domain": "shangluo.qinfeng.gov.cn", "path": "scdc.htm"},
    "yangling": {"name": "杨凌示范区", "domain": "yangling.qinfeng.gov.cn", "path": "scdc.htm"},
}


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }


def crawl_region(region_code: str) -> List[Dict]:
    """爬取单个地区"""
    region = REGIONS.get(region_code)
    if not region:
        return []

    url = f"https://{region['domain']}/{region['path']}"
    news_list = []

    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        seen_urls = set()

        for link in all_links:
            href = link.get('href', '')
            title = link.get_text(strip=True)

            # 过滤新闻链接
            if (href and '.htm' in href and 'info' in href and
                5 <= len(title) <= 100 and
                not any(kw in title.lower() for kw in ['登录', '注册', '关于', '联系我们', '网站地图'])):

                clean_href = href.split('#')[0].split('?')[0]
                if clean_href in seen_urls:
                    continue
                seen_urls.add(clean_href)

                full_url = urljoin(url, href)

                # 提取日期
                date = ""
                parent = link.parent
                if parent:
                    parent_text = parent.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', parent_text)
                    if date_match:
                        date = date_match.group(1).replace('/', '-')

                news_list.append({
                    'title': title,
                    'summary': '',
                    'date': date,
                    'url': full_url,
                    'source': '清风网',
                    'region': region['name'],
                    'menu': '首页',
                    'submenu': '',
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

        return news_list[:50]

    except Exception as e:
        print(f"爬取 {region['name']} 失败: {e}")
        return []


def crawl_all_regions():
    """爬取所有地区"""
    print(f"\n{'='*60}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始定时爬取")
    print('='*60)

    total_new = 0
    total_crawled = 0

    for region_code, region in REGIONS.items():
        print(f"\n📡 爬取 {region['name']}...")

        try:
            news = crawl_region(region_code)
            total_crawled += len(news)

            if news:
                new_count = insert_news(news, region_code)
                total_new += new_count
                print(f"   ✅ 获取 {len(news)} 条，新增 {new_count} 条")

                # 记录日志
                log_crawl(region_code, region['name'], len(news), new_count, 'success')
            else:
                log_crawl(region_code, region['name'], 0, 0, 'empty')

        except Exception as e:
            print(f"   ❌ 失败: {e}")
            log_crawl(region_code, region['name'], 0, 0, 'error', str(e))

    print(f"\n{'='*60}")
    print(f"🎉 爬取完成！总计获取 {total_crawled} 条，新增 {total_new} 条")
    print('='*60)

    return {'total_crawled': total_crawled, 'total_new': total_new}


def start_scheduler():
    """启动调度器"""
    print("\n" + "="*60)
    print("  启动定时爬虫调度器")
    print("="*60)
    print("  定时任务：每4小时自动爬取所有地区最新新闻")
    print("="*60)

    scheduler = BackgroundScheduler()

    # 每4小时执行一次
    scheduler.add_job(
        crawl_all_regions,
        trigger=IntervalTrigger(hours=4),
        id='crawl_all_regions',
        name='爬取所有地区新闻',
        replace_existing=True
    )

    # 每天早上8点执行
    scheduler.add_job(
        crawl_all_regions,
        trigger=CronTrigger(hour=8, minute=0),
        id='crawl_daily',
        name='每天早上8点爬取',
        replace_existing=True
    )

    scheduler.start()

    # 退出时关闭调度器
    atexit.register(lambda: scheduler.shutdown())

    print("\n✅ 调度器已启动！")
    print("   下次爬取时间: " + scheduler.get_job('crawl_all_regions').next_run_time.strftime('%Y-%m-%d %H:%M:%S'))

    return scheduler


# ========== API兼容函数 ==========

def get_stats_data():
    """获取统计图表数据"""
    violation_stats = get_violation_stats()
    case_stats = get_case_stats()
    region_stats = get_region_stats()

    return {
        'violations': violation_stats,
        'cases': case_stats,
        'regions': region_stats
    }


if __name__ == '__main__':
    # 初始化数据库
    init_db()

    # 立即执行一次爬取
    crawl_all_regions()

    # 启动调度器
    start_scheduler()

    # 保持运行
    import time
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 调度器已停止")
