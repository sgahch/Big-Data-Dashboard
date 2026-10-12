#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多源新闻爬虫示例脚本
用于演示从多个新闻源采集数据
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from news_sources_config import NEWS_SOURCES, get_enabled_sources

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def crawl_qingfeng(region='西安', max_pages=1):
    """爬取清风网数据"""
    print(f"\n[清风网] 开始爬取 {region} 数据...")
    
    try:
        if region not in NEWS_SOURCES['清风网']['regions']:
            print(f"  ✗ 地区 {region} 不在清风网配置中")
            return []
        
        url = NEWS_SOURCES['清风网']['regions'][region]
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('.news-list li') or soup.select('.list-item')
        
        results = []
        for item in news_items[:10]:  # 限制10条
            title_elem = item.select_one('a')
            if title_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'source': '清风网',
                    'region': region,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
        
        print(f"  ✓ 成功爬取 {len(results)} 条数据")
        return results
        
    except Exception as e:
        print(f"  ✗ 爬取失败: {str(e)}")
        return []

def crawl_ccdi(max_items=10):
    """爬取中央纪委国家监委网站（示例，实际需要根据网站结构调整）"""
    print(f"\n[中央纪委国家监委] 开始爬取数据...")
    
    try:
        # 这里仅作演示，实际网站可能需要不同的解析方式
        url = "https://www.ccdi.gov.cn/scdc/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        
        # 由于网站结构可能复杂，这里返回模拟数据用于演示
        print(f"  ⚠ 网站结构复杂，返回模拟数据用于演示")
        results = [
            {
                'title': f'中央纪委通报案例 {i+1}',
                'url': 'https://www.ccdi.gov.cn/',
                'source': '中央纪委国家监委网站',
                'region': '全国',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            for i in range(5)
        ]
        
        print(f"  ✓ 返回 {len(results)} 条演示数据")
        return results
        
    except Exception as e:
        print(f"  ✗ 爬取失败: {str(e)}")
        return []

def crawl_all_sources():
    """爬取所有启用的新闻源"""
    print("=" * 60)
    print("开始多源新闻采集")
    print("=" * 60)
    
    all_results = []
    enabled_sources = get_enabled_sources()
    
    # 爬取清风网
    if '清风网' in enabled_sources:
        for region in ['西安', '宝鸡', '咸阳']:
            results = crawl_qingfeng(region, max_pages=1)
            all_results.extend(results)
            time.sleep(1)  # 避免请求过快
    
    # 爬取中央纪委（演示）
    if '中央纪委国家监委网站' in enabled_sources:
        results = crawl_ccdi()
        all_results.extend(results)
    
    # 其他新闻源（暂时返回演示数据）
    for source_name in ['陕西省纪委监委', '人民网-反腐倡廉', '新华网-反腐']:
        if source_name in enabled_sources:
            print(f"\n[{source_name}] 暂未实现爬虫，返回演示数据")
            all_results.append({
                'title': f'{source_name}示例新闻',
                'url': enabled_sources[source_name]['base_url'],
                'source': source_name,
                'region': '全国',
                'date': datetime.now().strftime('%Y-%m-%d')
            })
    
    print("\n" + "=" * 60)
    print(f"采集完成！共获取 {len(all_results)} 条新闻")
    print("=" * 60)
    
    return all_results

if __name__ == '__main__':
    # 执行采集
    results = crawl_all_sources()
    
    # 保存结果
    output_file = 'multi_source_news.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    
    # 显示前5条
    print("\n前5条新闻预览：")
    for i, item in enumerate(results[:5], 1):
        print(f"{i}. [{item['source']}] {item['title']}")

