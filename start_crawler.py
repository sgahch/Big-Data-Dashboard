#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动清风网爬虫服务
"""

import sys
import os

# 确保导入正确的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler_server import app

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 清风网爬虫服务（完全重构版 v3.0）已启动")
    print("=" * 80)
    print(f"📡 API地址:")
    print(f"   - 所有新闻: http://localhost:5000/api/news")
    print(f"   - 按菜单过滤: http://localhost:5000/api/news?menu=省管干部")
    print(f"   - 菜单列表: http://localhost:5000/api/menus")
    print(f"   - 健康检查: http://localhost:5000/health")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5000, debug=False)

