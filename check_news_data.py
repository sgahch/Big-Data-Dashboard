#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查数据库中的新闻数据"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')
django.setup()

from apps.news.models import News

def check_news_data():
    """检查新闻数据"""
    print("=" * 60)
    print("检查数据库中的新闻数据")
    print("=" * 60)
    
    # 统计新闻总数
    total_count = News.objects.count()
    print(f"\n📊 新闻总数: {total_count}")
    
    if total_count == 0:
        print("\n❌ 数据库中没有新闻数据！")
        print("\n可能的原因：")
        print("1. 爬虫服务尚未运行")
        print("2. 爬虫任务尚未执行")
        print("3. 爬虫配置有问题")
        return
    
    # 显示最新的 5 条新闻
    print("\n📰 最新的 5 条新闻：")
    print("-" * 60)
    latest_news = News.objects.order_by('-crawl_time')[:5]
    for i, news in enumerate(latest_news, 1):
        print(f"\n{i}. {news.title}")
        print(f"   来源: {news.source}")
        print(f"   地区: {news.region_name}")
        print(f"   爬取时间: {news.crawl_time}")
        if news.url:
            print(f"   URL: {news.url[:80]}...")
    
    # 按来源统计
    print("\n" + "=" * 60)
    print("📈 按来源统计：")
    print("-" * 60)
    from django.db.models import Count
    source_stats = News.objects.values('source').annotate(count=Count('id')).order_by('-count')
    for stat in source_stats:
        print(f"   {stat['source']}: {stat['count']} 条")

if __name__ == '__main__':
    check_news_data()

