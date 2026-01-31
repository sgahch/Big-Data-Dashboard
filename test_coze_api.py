#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Coze API 测试脚本"""

import requests

COZE_API_TOKEN = 'cztei_qfF1nVgmG1yVYdWAVLupBecY4xFd7mVgNFqhwPp8hLKIYMtMSmFPBkJ4vFzxSXbXD'
COZE_BOT_ID = '7584448825868189732'

# 测试多个可能的API端点
endpoints = [
    ('https://api.coze.cn/v3/chat', 'POST'),
    ('https://api.coze.cn/v1/workflow/run', 'POST'),
    ('https://api.coze.com/v3/chat', 'POST'),
    ('https://api.coze.com/v1/workflow/run', 'POST'),
]

headers = {
    'Authorization': f'Bearer {COZE_API_TOKEN}',
    'Content-Type': 'application/json'
}

print("=" * 60)
print("测试 Coze API 连通性")
print("=" * 60)

# 1. 测试认证
print("\n[1] 测试认证...")
try:
    url = 'https://api.coze.cn/v3/chat'
    resp = requests.get(url.replace('/v3/chat', ''), headers=headers, timeout=10)
    print(f"  基础URL返回: {resp.status_code}")
except Exception as e:
    print(f"  错误: {e}")

# 2. 测试Chat API
print("\n[2] 测试 Chat API...")
for endpoint, method in endpoints:
    try:
        print(f"\n  测试: {method} {endpoint}")

        if 'workflow' in endpoint:
            payload = {
                'workflow_id': COZE_BOT_ID,
                'parameters': {'user_input': 'hello'}
            }
        else:
            payload = {
                'bot_id': COZE_BOT_ID,
                'user_id': 'test_user',
                'stream': False,
                'additional_messages': [
                    {'role': 'user', 'content': 'hello', 'content_type': 'text'}
                ]
            }

        resp = requests.post(endpoint, headers=headers, json=payload, timeout=15)
        print(f"  状态码: {resp.status_code}")
        print(f"  响应: {resp.text[:200]}")

    except requests.exceptions.RequestException as e:
        print(f"  请求失败: {e}")

# 3. 检查Bot配置
print("\n[3] 检查Bot配置...")
print(f"  Bot ID: {COZE_BOT_ID}")
print(f"  Token: {COZE_API_TOKEN[:20]}...")

# 4. 提示
print("\n" + "=" * 60)
print("可能的问题:")
print("1. Bot需要在Coze平台发布为API服务")
print("2. API Token可能需要重新生成")
print("3. Bot ID可能不正确")
print("\n请登录 https://coze.cn 检查:")
print("- Bot是否已发布")
print("- API Token是否有权限")
print("=" * 60)
