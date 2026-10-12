"""
AI聊天视图 - 调用Coze API
"""
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os

logger = logging.getLogger(__name__)

# Coze API配置
COZE_API_URL = os.getenv('COZE_API_URL', 'https://api.coze.cn/v3/chat')
COZE_BOT_ID = os.getenv('COZE_BOT_ID', '')
COZE_API_KEY = os.getenv('COZE_API_TOKEN', '')  # 使用COZE_API_TOKEN


@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """
    AI聊天接口
    """
    try:
        # 调试：打印当前使用的配置
        logger.info(f'Coze配置检查:')
        logger.info(f'  API URL: {COZE_API_URL}')
        logger.info(f'  Bot ID: {COZE_BOT_ID}')
        logger.info(f'  Token前缀: {COZE_API_KEY[:20] if COZE_API_KEY else "未配置"}...')
        logger.info(f'  Token长度: {len(COZE_API_KEY)}')

        # 解析请求数据
        data = json.loads(request.body)
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')

        if not user_message:
            return JsonResponse({
                'code': 400,
                'message': '消息不能为空',
                'data': None
            }, status=400)

        # 检查Coze配置
        if not COZE_BOT_ID or not COZE_API_KEY:
            logger.warning('Coze API未配置，返回默认回复')
            return JsonResponse({
                'code': 0,
                'message': '成功',
                'data': {
                    'reply': '您好！AI服务正在配置中，请稍后再试。如需帮助，请联系管理员。'
                }
            })

        # 调用Coze API
        headers = {
            'Authorization': f'Bearer {COZE_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'bot_id': COZE_BOT_ID,
            'user_id': user_id,
            'stream': False,
            'auto_save_history': True,
            'additional_messages': [
                {
                    'role': 'user',
                    'content': user_message,
                    'content_type': 'text'
                }
            ]
        }

        logger.info(f'调用Coze API: user_id={user_id}, message={user_message}')

        response = requests.post(
            COZE_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f'Coze API错误: {response.status_code} - {response.text}')
            return JsonResponse({
                'code': 500,
                'message': f'AI服务错误: {response.status_code}',
                'data': None
            }, status=500)

        result = response.json()
        logger.info(f'Coze API响应: {result}')

        # 解析Coze响应
        if result.get('code') == 0:
            data = result.get('data', {})
            conversation_id = data.get('conversation_id')
            chat_id = data.get('id')
            status = data.get('status')

            logger.info(f'对话状态: {status}, chat_id: {chat_id}')

            # 如果状态是in_progress，需要轮询获取结果
            if status == 'in_progress' and chat_id and conversation_id:
                # 轮询获取对话结果（最多等待10秒）
                import time
                max_attempts = 10
                for attempt in range(max_attempts):
                    time.sleep(1)  # 等待1秒

                    # 获取对话详情
                    retrieve_url = f"https://api.coze.cn/v3/chat/retrieve"
                    retrieve_params = {
                        'conversation_id': conversation_id,
                        'chat_id': chat_id
                    }

                    retrieve_response = requests.get(
                        retrieve_url,
                        headers=headers,
                        params=retrieve_params,
                        timeout=10
                    )

                    if retrieve_response.status_code == 200:
                        retrieve_result = retrieve_response.json()
                        if retrieve_result.get('code') == 0:
                            retrieve_data = retrieve_result.get('data', {})
                            retrieve_status = retrieve_data.get('status')

                            logger.info(f'轮询 {attempt+1}/{max_attempts}: 状态={retrieve_status}')

                            if retrieve_status == 'completed':
                                # 获取消息列表
                                messages_url = f"https://api.coze.cn/v3/chat/message/list"
                                messages_params = {
                                    'conversation_id': conversation_id,
                                    'chat_id': chat_id
                                }

                                messages_response = requests.get(
                                    messages_url,
                                    headers=headers,
                                    params=messages_params,
                                    timeout=10
                                )

                                if messages_response.status_code == 200:
                                    messages_result = messages_response.json()
                                    if messages_result.get('code') == 0:
                                        messages = messages_result.get('data', [])
                                        # 获取最后一条AI回复
                                        ai_reply = ''
                                        for msg in reversed(messages):
                                            if msg.get('role') == 'assistant' and msg.get('type') == 'answer':
                                                ai_reply = msg.get('content', '')
                                                break

                                        if ai_reply:
                                            return JsonResponse({
                                                'code': 0,
                                                'message': '成功',
                                                'data': {
                                                    'reply': ai_reply
                                                }
                                            })
                                break
                            elif retrieve_status == 'failed':
                                logger.error(f'对话失败: {retrieve_data}')
                                break

                # 如果轮询超时，返回默认回复
                return JsonResponse({
                    'code': 0,
                    'message': '成功',
                    'data': {
                        'reply': '抱歉，AI正在思考中，请稍后再试。'
                    }
                })

            # 如果直接返回了消息
            messages = data.get('messages', [])
            if messages:
                ai_reply = ''
                for msg in reversed(messages):
                    if msg.get('role') == 'assistant' and msg.get('type') == 'answer':
                        ai_reply = msg.get('content', '')
                        break

                if ai_reply:
                    return JsonResponse({
                        'code': 0,
                        'message': '成功',
                        'data': {
                            'reply': ai_reply
                        }
                    })

            # 没有找到回复
            return JsonResponse({
                'code': 0,
                'message': '成功',
                'data': {
                    'reply': '抱歉，我现在无法回答您的问题。'
                }
            })
        else:
            logger.error(f'Coze返回错误: {result}')
            return JsonResponse({
                'code': 500,
                'message': 'AI服务返回错误',
                'data': None
            }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({
            'code': 400,
            'message': '请求数据格式错误',
            'data': None
        }, status=400)
    except requests.Timeout:
        logger.error('Coze API超时')
        return JsonResponse({
            'code': 504,
            'message': 'AI服务超时，请稍后再试',
            'data': None
        }, status=504)
    except Exception as e:
        logger.error(f'AI聊天错误: {str(e)}', exc_info=True)
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': None
        }, status=500)


@require_http_methods(["GET"])
def health(request):
    """
    健康检查接口
    """
    is_configured = bool(COZE_BOT_ID and COZE_API_KEY)
    return JsonResponse({
        'code': 0,
        'message': '成功',
        'data': {
            'status': 'ok' if is_configured else 'not_configured',
            'coze_configured': is_configured
        }
    })

