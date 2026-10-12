"""
检查环境变量加载情况
"""
import os
from dotenv import load_dotenv

# 加载开发环境配置
load_dotenv('config/.env.dev')

print("=" * 60)
print("环境变量检查")
print("=" * 60)

coze_token = os.getenv('COZE_API_TOKEN', '')
coze_bot_id = os.getenv('COZE_BOT_ID', '')

print(f"COZE_API_TOKEN: {coze_token[:30]}... (长度: {len(coze_token)})")
print(f"COZE_BOT_ID: {coze_bot_id}")
print(f"Token类型: {'PAT' if coze_token.startswith('pat_') else 'Bot Token' if coze_token.startswith('cztei_') else '未知'}")

# 测试API
import requests
import json

print("\n" + "=" * 60)
print("测试Coze API")
print("=" * 60)

headers = {
    "Authorization": f"Bearer {coze_token}",
    "Content-Type": "application/json"
}

payload = {
    "bot_id": coze_bot_id,
    "user_id": "test_user_check",
    "stream": False,
    "auto_save_history": True,
    "additional_messages": [
        {
            "role": "user",
            "content": "测试",
            "content_type": "text"
        }
    ]
}

try:
    response = requests.post(
        "https://api.coze.cn/v3/chat",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result.get('code') == 0:
        print("\n✅ Token验证成功！")
    else:
        print(f"\n❌ Token验证失败！错误码: {result.get('code')}")
        print(f"错误信息: {result.get('msg')}")
        
except Exception as e:
    print(f"\n❌ 请求失败: {str(e)}")

