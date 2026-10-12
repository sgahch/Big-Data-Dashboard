"""
测试Coze API - 使用两种不同格式的token
"""
import requests
import json

# 测试配置
API_URL = "https://api.coze.cn/v3/chat"
BOT_ID = "7584448825868189732"

# 两种token
PAT_TOKEN = "pat_GFvRZZ9cCE6CkQufhLmS4vppOLv8424xJmv0MmdiSp3W1mJgkugaHyXtY8wdHyvc"
BOT_TOKEN = "cztei_qcL0IvA41MVJ1CvchE2DBZxXstHGtQgluMzVTQeSmOVFkhQr7PSywIppHdRh23J1U"

def test_token(token_name, token_value):
    """测试指定的token"""
    print(f"\n{'='*60}")
    print(f"测试 {token_name}")
    print(f"Token: {token_value[:20]}...")
    print(f"{'='*60}")
    
    headers = {
        "Authorization": f"Bearer {token_value}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "bot_id": BOT_ID,
        "user_id": "test_user",
        "stream": False,
        "auto_save_history": True,
        "additional_messages": [
            {
                "role": "user",
                "content": "你好",
                "content_type": "text"
            }
        ]
    }
    
    try:
        print(f"\n📤 发送请求到: {API_URL}")
        print(f"📦 Payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📥 响应状态码: {response.status_code}")
        print(f"📄 响应内容:")
        
        try:
            result = response.json()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 判断是否成功
            if response.status_code == 200 and result.get('code') == 0:
                print(f"\n✅ {token_name} 测试成功！")
                messages = result.get('data', {}).get('messages', [])
                for msg in messages:
                    if msg.get('role') == 'assistant' and msg.get('type') == 'answer':
                        print(f"🤖 AI回复: {msg.get('content', '')}")
                return True
            else:
                print(f"\n❌ {token_name} 测试失败！")
                return False
                
        except json.JSONDecodeError:
            print(response.text)
            print(f"\n❌ {token_name} 响应不是有效的JSON")
            return False
            
    except requests.Timeout:
        print(f"\n⏱️ {token_name} 请求超时")
        return False
    except Exception as e:
        print(f"\n❌ {token_name} 发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试Coze API")
    print(f"🎯 Bot ID: {BOT_ID}")
    
    # 测试PAT token
    pat_success = test_token("PAT Token", PAT_TOKEN)
    
    # 测试Bot token
    bot_success = test_token("Bot Token", BOT_TOKEN)
    
    # 总结
    print(f"\n{'='*60}")
    print("📊 测试总结")
    print(f"{'='*60}")
    print(f"PAT Token: {'✅ 成功' if pat_success else '❌ 失败'}")
    print(f"Bot Token: {'✅ 成功' if bot_success else '❌ 失败'}")
    
    if pat_success:
        print("\n💡 建议使用 PAT Token")
    elif bot_success:
        print("\n💡 建议使用 Bot Token")
    else:
        print("\n⚠️ 两种token都失败了，请检查配置")

