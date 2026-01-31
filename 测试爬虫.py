# -*- coding: utf-8 -*-
"""清风网爬虫测试脚本"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 陕西各地区配置
REGIONS = {
    "xian": {"name": "西安市", "url": "https://xian.qinfeng.gov.cn/scdc.htm"},
    "baoji": {"name": "宝鸡市", "url": "https://baoji.qinfeng.gov.cn/scdc.htm"},
    "xianyang": {"name": "咸阳市", "url": "https://xianyang.qinfeng.gov.cn/scdc.htm"},
    "yanan": {"name": "延安市", "url": "https://yanan.qinfeng.gov.cn/scdc.htm"},
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def crawl_region(region_code):
    """爬取单个地区"""
    region = REGIONS[region_code]
    print(f"\n{'='*50}")
    print(f"爬取: {region['name']} - {region['url']}")
    print('='*50)

    try:
        response = requests.get(region['url'], headers=headers, timeout=15)
        response.encoding = 'utf-8'
        print(f"状态码: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找所有新闻链接
        all_links = soup.find_all('a', href=True)
        news_links = []

        for link in all_links:
            href = link.get('href', '')
            title = link.get_text(strip=True)

            # 过滤有效新闻链接
            if (href and '.htm' in href and
                'info' in href and
                len(title) >= 5 and len(title) <= 80 and
                not any(kw in title.lower() for kw in ['登录', '注册', '关于', '联系我们', '网站地图'])):

                full_url = urljoin(region['url'], href)
                news_links.append({
                    'title': title,
                    'url': full_url
                })

        # 去重
        seen = set()
        unique_news = []
        for news in news_links:
            if news['url'] not in seen:
                seen.add(news['url'])
                unique_news.append(news)

        print(f"找到 {len(unique_news)} 条新闻")

        # 显示前5条
        for i, news in enumerate(unique_news[:5], 1):
            print(f"  {i}. {news['title'][:40]}...")
            print(f"     {news['url']}")

        return unique_news

    except Exception as e:
        print(f"错误: {e}")
        return []

if __name__ == "__main__":
    print("清风网爬虫测试")
    print("="*50)

    # 测试西安
    xian_news = crawl_region("xian")

    # 测试宝鸡
    baoji_news = crawl_region("baoji")

    print("\n" + "="*50)
    print("测试完成!")
    print(f"西安: {len(xian_news)} 条")
    print(f"宝鸡: {len(baoji_news)} 条")
