#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json

# 设置UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 加载 .env 文件
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from typing import List, Dict
from urllib.parse import urljoin, urlparse, quote

# 导入数据库和调度器模块
from models import (
    init_db, insert_news, get_news, get_violation_stats, get_case_stats,
    get_region_stats, get_all_tags, log_crawl, auto_tagging
)
from scheduler import crawl_all_regions, start_scheduler, REGIONS

app = Flask(__name__)
CORS(app)

# 全局错误处理器
@app.errorhandler(Exception)
def handle_error(e):
    print(f"🔥 全局捕获异常: {e}")
    import traceback
    traceback.print_exc()
    return jsonify({
        'code': -1,
        'message': str(e),
        'data': None
    }), 500


def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }


# ========== 简化的爬取函数 ==========

def crawl_region_simple(region_code: str) -> List[Dict]:
    """简化版爬取单个地区"""
    region = REGIONS.get(region_code)
    if not region:
        return []

    url = f"https://{region['domain']}/{region['path']}"
    news_list = []

    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        seen_urls = set()

        for link in all_links:
            href = link.get('href', '')
            title = link.get_text(strip=True)

            if (href and '.htm' in href and 'info' in href and
                5 <= len(title) <= 100 and
                not any(kw in title.lower() for kw in ['登录', '注册', '关于', '联系我们'])):

                clean_href = href.split('#')[0].split('?')[0]
                if clean_href in seen_urls:
                    continue
                seen_urls.add(clean_href)

                full_url = urljoin(url, href)
                news_list.append({
                    'title': title,
                    'summary': '',
                    'date': '',
                    'url': full_url,
                    'source': '清风网',
                    'region': region['name'],
                    'menu': '首页',
                    'submenu': '',
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

        return news_list[:50]
    except Exception as e:
        print(f"爬取失败: {e}")
        return []


# ========== API路由 ==========

@app.route('/api/news/', methods=['GET'])
@app.route('/api/news', methods=['GET'])
def get_news_api():
    """获取新闻列表"""
    try:
        region = request.args.get('region', 'all')
        limit = int(request.args.get('limit', 50))

        # 如果指定地区，先爬取最新数据
        if region != 'all':
            news = crawl_region_simple(region)
            if news:
                insert_news(news, region)

        # 从数据库获取
        news_list = get_news(limit=limit, region=region)

        return jsonify({
            'code': 0, 'message': 'success',
            'data': news_list,
            'total': len(news_list),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'code': -1, 'message': str(e),
            'data': [], 'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/news/<int:news_id>/info/', methods=['GET'])
def get_news_info(news_id):
    """获取单条新闻详情"""
    try:
        news_list = get_news(limit=1, news_id=news_id)
        if news_list:
            news = news_list[0]
            # 获取相关推荐（同一地区）
            related = get_news(limit=5, region=news.get('region'))
            related = [n for n in related if n.get('id') != news_id]

            return jsonify({
                'code': 0, 'message': 'success',
                'data': {
                    'news': news,
                    'related': related
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'code': -1, 'message': '新闻不存在',
                'data': None
            }), 404
    except Exception as e:
        return jsonify({
            'code': -1, 'message': str(e),
            'data': None
        }), 500


@app.route('/api/news/force-crawl/', methods=['POST'])
@app.route('/api/news/force-crawl', methods=['POST'])
def force_crawl():
    """手动触发爬取"""
    try:
        result = crawl_all_regions()
        return jsonify({
            'code': 0, 'message': 'success',
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'code': -1, 'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/api/stats/violations/', methods=['GET'])
@app.route('/api/stats/violations', methods=['GET'])
def get_violations_stats():
    """获取违规事项分布统计"""
    try:
        stats = get_violation_stats()
        return jsonify({
            'code': 0, 'message': 'success',
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e), 'data': []}), 500


@app.route('/api/stats/cases/', methods=['GET'])
@app.route('/api/stats/cases', methods=['GET'])
def get_cases_stats():
    """获取案件查处统计"""
    try:
        months = int(request.args.get('months', 12))
        stats = get_case_stats(months)
        return jsonify({
            'code': 0, 'message': 'success',
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e), 'data': {}}), 500


@app.route('/api/stats/regions/', methods=['GET'])
@app.route('/api/stats/regions', methods=['GET'])
def get_regions_stats():
    """获取各地区统计"""
    try:
        stats = get_region_stats()
        return jsonify({
            'code': 0, 'message': 'success',
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e), 'data': []}), 500


@app.route('/api/stats/all/', methods=['GET'])
@app.route('/api/stats/all', methods=['GET'])
def get_all_stats():
    """获取所有统计数据"""
    try:
        violations = get_violation_stats()
        cases = get_case_stats()
        regions = get_region_stats()

        return jsonify({
            'code': 0, 'message': 'success',
            'data': {
                'violations': violations,
                'cases': cases,
                'regions': regions
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)}), 500


@app.route('/api/tags/', methods=['GET'])
@app.route('/api/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    try:
        tags = get_all_tags()
        return jsonify({
            'code': 0, 'message': 'success',
            'data': tags,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)}), 500


@app.route('/api/regions/', methods=['GET'])
@app.route('/api/regions', methods=['GET'])
def get_regions():
    """获取地区列表"""
    regions_list = [
        {"code": k, "name": v["name"]} for k, v in REGIONS.items()
    ]
    return jsonify({
        'code': 0, 'message': 'success',
        'data': regions_list
    })


# ========== Coze AI客服代理API ==========

# Coze API 配置
COZE_API_TOKEN = os.environ.get('COZE_API_TOKEN', 'cztei_qB2AFxhYWesY9WyV1VktPi6FRFNm5247CIm4yCrYz8203EeZ4vTVIqpmZo7R0789M')
COZE_BOT_ID = os.environ.get('COZE_BOT_ID', '7584448825868189732')

# 使用官方 SDK cozepy
try:
    from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, Message, ChatEventType
    COZE_SDK_AVAILABLE = True
except ImportError:
    COZE_SDK_AVAILABLE = False
    print("⚠️ cozepy SDK 未安装，AI客服功能不可用")

# 初始化 Coze 客户端
_coze_client = None
def get_coze_client():
    """获取 Coze 客户端单例"""
    global _coze_client
    if _coze_client is None and COZE_SDK_AVAILABLE:
        _coze_client = Coze(
            auth=TokenAuth(token=COZE_API_TOKEN),
            base_url=COZE_CN_BASE_URL
        )
    return _coze_client


@app.route('/api/ai/chat/', methods=['POST', 'OPTIONS'])
@app.route('/api/ai/chat', methods=['POST', 'OPTIONS'])
def coze_chat():
    """Coze AI客服代理API - 使用官方SDK流式响应"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response

    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({
                'code': -1,
                'message': '请求解析失败',
                'data': None
            }), 400

        user_message = data.get('message', '')
        if not user_message:
            return jsonify({
                'code': -1,
                'message': '消息内容不能为空',
                'data': None
            }), 400

        user_id = data.get('user_id', f'user_{int(time.time())}')

        print(f"🤖 AI客服收到问题: {user_message}")

        # 检查 SDK 是否可用
        if not COZE_SDK_AVAILABLE:
            return jsonify({
                'code': -1,
                'message': 'AI客服SDK未安装',
                'data': {'reply': '抱歉，AI服务暂时不可用，请联系管理员安装cozepy SDK。'}
            }), 500

        # 获取 Coze 客户端
        coze = get_coze_client()
        if not coze:
            return jsonify({
                'code': -1,
                'message': 'AI客服初始化失败',
                'data': {'reply': '抱歉，AI服务暂时不可用。'}
            }), 500

        # 使用官方 SDK 调用流式聊天
        ai_reply = ''
        try:
            for event in coze.chat.stream(
                bot_id=COZE_BOT_ID,
                user_id=str(user_id),
                additional_messages=[
                    Message.build_user_question_text(user_message),
                ],
            ):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    content = event.message.content
                    if content:
                        ai_reply += content
                        print(f"✅ 收到消息: {content[:50]}...")

                if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    print(f"✅ AI客服回复完成, 共{len(ai_reply)}字符")
                    break

        except Exception as e:
            print(f"❌ Coze SDK调用错误: {e}")
            return jsonify({
                'code': -1,
                'message': str(e),
                'data': {'reply': f'抱歉，AI服务暂时不可用: {str(e)}'}
            }), 500

        if ai_reply:
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': {'reply': ai_reply},
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'code': -1,
                'message': '未获取到AI回复',
                'data': {'reply': '抱歉，AI服务暂时无响应，请稍后再试。'}
            }), 500

    except Exception as e:
        print(f"❌ AI客服异常: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': -1,
            'message': str(e),
            'data': {'reply': f'抱歉，AI服务暂时不可用: {str(e)}'}
        }), 500


@app.route('/api/ai/health/', methods=['GET'])
@app.route('/api/ai/health', methods=['GET'])
def ai_health():
    """检查AI服务健康状态"""
    try:
        if not COZE_SDK_AVAILABLE:
            return jsonify({
                'code': -1,
                'message': 'cozepy SDK未安装',
                'data': {'status': 'error', 'sdk_available': False}
            }), 500

        coze = get_coze_client()
        if coze:
            return jsonify({
                'code': 0,
                'message': 'success',
                'data': {
                    'status': 'ready',
                    'bot_id': COZE_BOT_ID,
                    'sdk_available': True
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'code': -1,
                'message': 'Coze客户端初始化失败',
                'data': {'status': 'error', 'sdk_available': True}
            }), 500
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': str(e),
            'data': {'status': 'error'}
        }), 500


@app.route('/api/stats/dashboard/', methods=['GET'])
@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard():
    """获取仪表盘数据"""
    try:
        violations = get_violation_stats()
        cases = get_case_stats()
        regions = get_region_stats()
        return jsonify({
            'code': 0, 'message': 'success',
            'data': {
                'violations': violations,
                'cases': cases,
                'regions': regions,
                'recent_news': get_news(limit=10)
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)}), 500


@app.route('/api/stats/monitor/', methods=['GET'])
@app.route('/api/stats/monitor', methods=['GET'])
def get_monitor():
    """获取监控数据"""
    return jsonify({
        'code': 0, 'message': 'success',
        'data': {
            'cpu': 15,
            'memory': 42,
            'disk': 35,
            'network': {'in': 1024, 'out': 2048},
            'uptime': '2d 5h 30m'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/crawl/scheduler/', methods=['GET'])
@app.route('/api/crawl/scheduler', methods=['GET'])
def get_scheduler():
    """获取调度器状态"""
    return jsonify({
        'code': 0, 'message': 'success',
        'data': {
            'enabled': True,
            'interval': 4,
            'unit': 'hours',
            'next_run': '2026-01-30 18:00:00',
            'status': 'running'
        },
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/crawl/control/', methods=['POST'])
@app.route('/api/crawl/control', methods=['POST'])
def crawl_control():
    """爬虫控制"""
    try:
        action = request.json.get('action')
        if action == 'start':
            start_scheduler()
            return jsonify({'code': 0, 'message': '爬虫已启动'})
        elif action == 'stop':
            return jsonify({'code': 0, 'message': '爬虫已停止'})
        else:
            return jsonify({'code': -1, 'message': '未知操作'}), 400
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)}), 500


@app.route('/api/supervision-items/', methods=['GET'])
@app.route('/api/supervision-items', methods=['GET'])
def get_supervision_items():
    """获取监督事项列表"""
    return jsonify({
        'code': 0, 'message': 'success',
        'data': [
            {'id': 1, 'title': '监督检查事项1', 'status': '进行中', 'date': '2024-12-01'},
            {'id': 2, 'title': '监督检查事项2', 'status': '已完成', 'date': '2024-11-28'},
        ],
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/supervision-items/import_excel/', methods=['POST'])
@app.route('/api/supervision-items/import_excel', methods=['POST'])
def import_supervision():
    """导入监督事项"""
    return jsonify({
        'code': 0, 'message': '导入成功',
        'data': {'imported': 5},
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/supervision-items/export_excel/', methods=['GET'])
@app.route('/api/supervision-items/export_excel', methods=['GET'])
def export_supervision():
    """导出监督事项"""
    return jsonify({
        'code': 0, 'message': 'success',
        'data': {'url': '/download/supervision.xlsx'},
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/stats/report/', methods=['POST'])
@app.route('/api/stats/report', methods=['POST'])
def export_report():
    """导出报告（CSV格式）"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        report_type = data.get('type', 'excel')

        # 获取统计数据
        violations = get_violation_stats()
        cases = get_case_stats()
        regions = get_region_stats()
        news_list = get_news(limit=100)

        # 生成CSV内容
        csv_content = "纪检监察数据分析报告\n"
        csv_content += f"生成时间,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # 违规事项统计
        csv_content += "一、违规事项分布\n"
        csv_content += "类型,数量\n"
        for v in violations:
            csv_content += f"{v['name']},{v['value']}\n"
        csv_content += "\n"

        # 案件查处统计
        csv_content += "二、案件查处统计（近12个月）\n"
        csv_content += "月份,数量\n"
        for i, month in enumerate(cases.get('months', [])):
            csv_content += f"{month},{cases.get('values', [0])[i] if i < len(cases.get('values', [])) else 0}\n"
        csv_content += "\n"

        # 地区统计
        csv_content += "三、地区新闻统计\n"
        csv_content += "地区,数量\n"
        for r in regions:
            csv_content += f"{r.get('region', '')},{r.get('count', 0)}\n"
        csv_content += "\n"

        # 新闻列表
        csv_content += "四、新闻列表\n"
        csv_content += "序号,标题,日期,地区,来源,标签\n"
        for i, news in enumerate(news_list, start=1):
            title = (news.get('title', '') or '').replace(',', '，').replace('\n', ' ')
            tags = (news.get('tags', '') or '').replace(',', '，')
            csv_content += f"{i},{title},{news.get('date', '')},{news.get('region', '')},{news.get('source', '')},{tags}\n"

        # 返回CSV文件
        from flask import Response
        response = Response(csv_content, mimetype='text/csv; charset=utf-8')
        # 使用纯UTF-8编码的文件名（RFC 5987标准，只用filename*避免latin-1编码问题）
        filename = f"纪检监察报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        encoded_filename = quote(filename, safe='')
        response.headers['Content-Disposition'] = f"attachment; filename*=utf-8''{encoded_filename}"
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': -1,
            'message': str(e),
            'data': None
        }), 500


@app.route('/api/news/export/', methods=['GET'])
@app.route('/api/news/export', methods=['GET'])
def export_news():
    """导出新闻列表（CSV格式）"""
    try:
        # 获取参数
        region = request.args.get('region', 'all')
        limit = int(request.args.get('limit', 500))

        # 获取新闻数据
        news_list = get_news(limit=limit, region=region)

        # 生成CSV内容
        csv_content = "清风网新闻数据导出\n"
        csv_content += f"生成时间,{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        csv_content += f"总数量,{len(news_list)}\n\n"

        csv_content += "序号,标题,日期,地区,来源,菜单,子菜单,标签,URL\n"
        for i, news in enumerate(news_list, start=1):
            title = (news.get('title', '') or '').replace(',', '，').replace('\n', ' ').replace('"', '"')
            tags = (news.get('tags', '') or '').replace(',', '，')
            url = news.get('url', '') or ''
            csv_content += f"{i},{title},{news.get('date', '')},{news.get('region', '')},{news.get('source', '')},{news.get('menu', '')},{news.get('submenu', '')},{tags},{url}\n"

        # 返回CSV文件
        from flask import Response
        response = Response(csv_content, mimetype='text/csv; charset=utf-8')
        # 使用纯UTF-8编码的文件名（RFC 5987标准，只用filename*避免latin-1编码问题）
        region_name = 'all' if region == 'all' else region
        filename = f"清风网新闻_{region_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        encoded_filename = quote(filename, safe='')
        response.headers['Content-Disposition'] = f"attachment; filename*=utf-8''{encoded_filename}"
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'

        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': -1,
            'message': str(e),
            'data': None
        }), 500


@app.route('/api/news/<int:news_id>/correct/', methods=['POST'])
@app.route('/api/news/<int:news_id>/correct', methods=['POST'])
def correct_news(news_id):
    """修正文章"""
    try:
        data = request.json
        return jsonify({
            'code': 0, 'message': 'success',
            'data': {'id': news_id, 'corrected': True},
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'code': -1, 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'qinfeng-crawler-db',
        'version': '5.0',
        'database': 'SQLite',
        'ai_service': 'coze'
    })


@app.route('/', methods=['GET'])
def index():
    return send_file('index.html')


# 静态文件路由 - 只匹配非 API 路径
@app.route('/<path:filename>', methods=['GET'])
def serve_static(filename):
    # 排除 API 路径
    if filename.startswith('api/'):
        return jsonify({'error': 'Not Found'}), 404
    return send_from_directory('.', filename)


if __name__ == '__main__':
    print("=" * 60)
    print("  清风网爬虫服务 v5.0（数据库版）")
    print("=" * 60)
    print("  访问地址: http://localhost:5000/")
    print("  API接口:")
    print("    - GET /api/news           # 获取新闻")
    print("    - POST /api/news/force-crawl  # 手动触发爬取")
    print("    - GET /api/stats/violations   # 违规事项统计")
    print("    - GET /api/stats/cases        # 案件查处统计")
    print("    - GET /api/stats/regions      # 地区统计")
    print("    - GET /api/stats/all          # 所有统计")
    print("    - GET /api/tags               # 标签列表")
    print("=" * 60)

    # 初始化数据库
    init_db()

    # 启动定时调度器
    start_scheduler()

    # 启动服务
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
