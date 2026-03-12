#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试MySQL数据库连接"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env.development')

# 从环境变量获取数据库配置
db_config = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '123456'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4'
}

try:
    # 尝试连接到MySQL服务器
    connection = pymysql.connect(**db_config)
    print("✅ 成功连接到MySQL服务器")
    
    # 检查数据库是否存在
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES LIKE 'supervision'")
        result = cursor.fetchone()
        if result:
            print("✅ 数据库 'supervision' 存在")
        else:
            print("❌ 数据库 'supervision' 不存在")
            # 尝试创建数据库
            try:
                cursor.execute("CREATE DATABASE supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print("✅ 数据库 'supervision' 已创建")
            except Exception as e:
                print(f"❌ 创建数据库失败: {e}")
    
    connection.close()
except Exception as e:
    print(f"❌ 连接MySQL服务器失败: {e}")
    print("请确保：")
    print("1. MySQL服务正在运行")
    print("2. 用户名和密码正确")
    print("3. MySQL允许root用户从localhost连接")