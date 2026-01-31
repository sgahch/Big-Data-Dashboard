# -*- coding: utf-8 -*-
import logging
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from django.conf import settings
from django.db import transaction

logger = logging.getLogger(__name__)

# 地区配置
REGIONS = {
    'xian': {'name': '西安市', 'domain': 'xian.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'baoji': {'name': '宝鸡市', 'domain': 'baoji.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'xianyang': {'name': '咸阳市', 'domain': 'xianyang.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'tongchuan': {'name': '铜川市', 'domain': 'tongchuan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'weinan': {'name': '渭南市', 'domain': 'weinan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yanan': {'name': '延安市', 'domain': 'yanan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yulin': {'name': '榆林市', 'domain': 'yulin.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'hanzhong': {'name': '汉中市', 'domain': 'hanzhong.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'ankang': {'name': '安康市', 'domain': 'ankang.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'shangluo': {'name': '商洛市', 'domain': 'shangluo.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yangling': {'name': '杨凌示范区', 'domain': 'yangling.qinfeng.gov.cn', 'path': 'scdc.htm'},
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def crawl_region(region_code: str):
    """爬取单个地区"""
    from apps.news.models import Region, News, Tag, CrawlLog

    region_config = REGIONS.get(region_code)
    if not region_config:
        return {'total': 0, 'new': 0, 'status': 'error', 'error': '未知地区'}

    start_time = time.time()
    url = f"https://{region_config['domain']}/{region_config['path']}"
    news_list = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            raise Exception(f'HTTP {response.status_code}')

        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        seen_urls = set()

        for link in all_links:
            href = link.get('href', '')
            title = link.get_text(strip=True)

            # 过滤有效新闻链接
            if (href and '.htm' in href and 'info' in href and
                5 <= len(title) <= 100 and
                not any(kw in title.lower() for kw in ['登录', '注册', '关于', '联系我们', '网站地图'])):

                clean_href = href.split('#')[0].split('?')[0]
                if clean_href in seen_urls:
                    continue
                seen_urls.add(clean_href)

                full_url = urljoin(url, href)

                # 提取日期
                date = None
                parent = link.parent
                if parent:
                    parent_text = parent.get_text(strip=True)
                    import re
                    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', parent_text)
                    if date_match:
                        try:
                            date = datetime.strptime(date_match.group(1).replace('/', '-'), '%Y-%m-%d').date()
                        except:
                            pass

                news_list.append({
                    'title': title,
                    'summary': '',
                    'url': full_url,
                    'date': date,
                    'region_name': region_config['name'],
                })

        # 保存到数据库
        with transaction.atomic():
            new_count = 0
            region_obj = Region.objects.filter(code=region_code).first()

            for news_data in news_list[:100]:
                # 检查是否已存在
                if News.objects.filter(url=news_data['url']).exists():
                    continue

                # 自动打标签
                tag_names = auto_tagging(news_data['title'])
                tags = Tag.objects.filter(name__in=tag_names)

                news = News.objects.create(
                    title=news_data['title'],
                    summary=news_data['summary'],
                    url=news_data['url'],
                    date=news_data['date'],
                    source='清风网',
                    region=region_obj,
                    region_name=news_data['region_name'],
                    menu='首页',
                    tag_names=','.join(tag_names),
                )
                news.tags.set(tags)
                new_count += 1

        duration = time.time() - start_time

        # 记录日志
        CrawlLog.objects.create(
            region=region_obj,
            region_name=region_config['name'],
            total_crawled=len(news_list),
            new_count=new_count,
            status='success' if new_count > 0 else 'empty',
            duration=duration
        )

        logger.info(f'爬取 {region_config["name"]}: {len(news_list)} 条, 新增 {new_count} 条')

        return {
            'total': len(news_list),
            'new': new_count,
            'status': 'success' if new_count > 0 else 'empty',
            'duration': duration
        }

    except Exception as e:
        logger.exception(f'爬取 {region_config["name"]} 失败')
        duration = time.time() - start_time

        CrawlLog.objects.create(
            region=Region.objects.filter(code=region_code).first(),
            region_name=region_config['name'],
            total_crawled=0,
            new_count=0,
            status='error',
            error_message=str(e),
            duration=duration
        )

        return {'total': 0, 'new': 0, 'status': 'error', 'error': str(e)}


def auto_tagging(text: str):
    """自动打标签"""
    from apps.news.models import Tag

    tags = Tag.objects.filter(is_auto=True, is_active=True)
    matched = []

    for tag in tags:
        keywords = tag.get_keywords_list()
        for keyword in keywords:
            if keyword and keyword in text:
                matched.append(tag.name)
                break

    return list(set(matched))[:5]  # 最多5个标签


def crawl_all_regions():
    """爬取所有地区"""
    results = {}
    total_new = 0
    total_crawled = 0

    for region_code in REGIONS:
        result = crawl_region(region_code)
        results[region_code] = result
        total_new += result.get('new', 0)
        total_crawled += result.get('total', 0)

    logger.info(f'爬取完成: 总计爬取 {total_crawled} 条, 新增 {total_new} 条')

    return {
        'results': results,
        'total_crawled': total_crawled,
        'total_new': total_new
    }
