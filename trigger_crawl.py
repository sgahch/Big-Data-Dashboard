#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""手动触发爬虫任务"""

import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')
django.setup()

from apps.crawler.tasks import crawl_all_regions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    print("=" * 60)
    print("开始手动触发爬虫任务")
    print("=" * 60)
    
    try:
        result = crawl_all_regions()
        
        print("\n" + "=" * 60)
        print("爬虫任务完成！")
        print("=" * 60)
        print(f"总计爬取: {result.get('total_crawled', 0)} 条")
        print(f"新增数据: {result.get('total_new', 0)} 条")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 爬虫任务失败: {e}")
        import traceback
        traceback.print_exc()

