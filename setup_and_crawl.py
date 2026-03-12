#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一键设置数据库并启动爬虫"""

import os
import sys
import django
import subprocess

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')
django.setup()

def run_command(description, command):
    """运行命令并显示结果"""
    print("\n" + "=" * 60)
    print(f"📌 {description}")
    print("=" * 60)
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✅ {description} - 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - 失败")
        print(f"错误: {e.stderr}")
        return False

def init_data():
    """初始化基础数据"""
    print("\n" + "=" * 60)
    print("📌 初始化基础数据（地区和标签）")
    print("=" * 60)
    
    try:
        from apps.crawler.tasks import init_regions, init_tags
        
        # 初始化地区
        init_regions()
        print("✅ 地区数据初始化完成")
        
        # 初始化标签
        init_tags()
        print("✅ 标签数据初始化完成")
        
        return True
    except Exception as e:
        print(f"❌ 初始化数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def trigger_crawl():
    """触发爬虫任务"""
    print("\n" + "=" * 60)
    print("📌 开始爬取新闻数据")
    print("=" * 60)
    
    try:
        from apps.crawler.tasks import crawl_all_regions
        
        result = crawl_all_regions()
        
        print("\n" + "=" * 60)
        print("✅ 爬虫任务完成！")
        print("=" * 60)
        print(f"总计爬取: {result.get('total_crawled', 0)} 条")
        print(f"新增数据: {result.get('total_new', 0)} 条")
        print("=" * 60)
        
        return True
    except Exception as e:
        print(f"❌ 爬虫任务失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_news_count():
    """检查新闻数量"""
    print("\n" + "=" * 60)
    print("📌 检查数据库中的新闻数据")
    print("=" * 60)
    
    try:
        from apps.news.models import News
        
        total_count = News.objects.count()
        print(f"📊 新闻总数: {total_count}")
        
        if total_count > 0:
            print("\n📰 最新的 5 条新闻：")
            print("-" * 60)
            latest_news = News.objects.order_by('-created_at')[:5]
            for i, news in enumerate(latest_news, 1):
                print(f"\n{i}. {news.title}")
                print(f"   来源: {news.source}")
                print(f"   时间: {news.created_at}")
        
        return True
    except Exception as e:
        print(f"❌ 检查新闻数据失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 开始设置数据库并启动爬虫服务")
    print("=" * 60)
    
    # 步骤1: 运行数据库迁移
    if not run_command("步骤1: 运行数据库迁移", "python manage.py migrate"):
        print("\n❌ 数据库迁移失败，请检查错误信息")
        sys.exit(1)
    
    # 步骤2: 初始化基础数据
    if not init_data():
        print("\n❌ 初始化数据失败，请检查错误信息")
        sys.exit(1)
    
    # 步骤3: 触发爬虫
    if not trigger_crawl():
        print("\n❌ 爬虫任务失败，请检查错误信息")
        sys.exit(1)
    
    # 步骤4: 检查新闻数量
    check_news_count()
    
    print("\n" + "=" * 60)
    print("🎉 所有步骤完成！")
    print("=" * 60)
    print("\n下一步操作：")
    print("1. 重启Django服务器: python manage.py runserver 0.0.0.0:8000")
    print("2. 访问前端页面查看数据")
    print("=" * 60)

