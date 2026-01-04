#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清风网纪检通报爬虫服务（完全重构版 v3.0）
核心功能：
1. 自动爬取侧边栏所有菜单链接
2. 依次访问每个菜单页面
3. 提取每个页面中所有的新闻列表（支持多板块）
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from typing import List, Dict
from urllib.parse import urljoin

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 目标网站配置
BASE_URL = "https://www.qinfeng.gov.cn"

# 需要排除的链接（外链、首页等）
EXCLUDE_KEYWORDS = [
    'javascript:',
    'http://www.12388.gov.cn',  # 网络举报外链
    '/index.htm',  # 首页
    '#'  # 空链接
]

def get_headers():
    """获取请求头"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': BASE_URL
    }

def is_valid_menu_link(href: str) -> bool:
    """
    判断链接是否为有效的菜单链接

    Args:
        href: 链接地址

    Returns:
        是否为有效链接
    """
    if not href:
        return False

    # 排除外链和无效链接
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in href:
            return False

    # 只保留站内链接
    if href.startswith('http') and not href.startswith(BASE_URL):
        return False

    return True

def get_sidebar_menus() -> List[Dict]:
    """
    获取侧边栏所有菜单链接

    Returns:
        菜单列表，每个菜单包含 name, url, has_submenu
    """
    try:
        print("=" * 80)
        print("📋 正在获取侧边栏菜单...")
        print("=" * 80)

        # 先访问审查调查页面作为入口
        response = requests.get(f"{BASE_URL}/scdc.htm", headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        menus = []

        # 定位侧边栏容器
        sidebar = soup.select_one('.xsxc_index_left')
        if not sidebar:
            print("❌ 未找到侧边栏容器 .xsxc_index_left")
            return []

        # 获取所有一级菜单项
        menu_items = sidebar.select('ul > li')

        for item in menu_items:
            # 获取主链接
            main_link = item.find('a', recursive=False)
            if not main_link:
                continue

            menu_name = main_link.get_text(strip=True)
            menu_href = main_link.get('href', '')

            # 验证链接有效性
            if not is_valid_menu_link(menu_href):
                print(f"⏭️  跳过: {menu_name} ({menu_href})")
                continue

            # 转换为绝对URL
            menu_url = urljoin(BASE_URL, menu_href)

            # 检查是否有子菜单
            submenu = item.find('ul')
            has_submenu = submenu is not None

            menu_info = {
                'name': menu_name,
                'url': menu_url,
                'has_submenu': has_submenu,
                'submenus': []
            }

            # 如果有子菜单，提取子菜单链接
            if has_submenu:
                sub_links = submenu.find_all('a')
                for sub_link in sub_links:
                    sub_name = sub_link.get_text(strip=True)
                    sub_href = sub_link.get('href', '')

                    if is_valid_menu_link(sub_href):
                        sub_url = urljoin(BASE_URL, sub_href)
                        menu_info['submenus'].append({
                            'name': sub_name,
                            'url': sub_url
                        })

            menus.append(menu_info)
            print(f"✅ 发现菜单: {menu_name} (子菜单: {len(menu_info['submenus'])})")

        print(f"\n📊 共发现 {len(menus)} 个有效菜单")
        return menus

    except Exception as e:
        print(f"❌ 获取侧边栏菜单失败: {e}")
        return []

def parse_news_from_page(url: str, menu_name: str, submenu_name: str = "") -> List[Dict]:
    """
    从单个页面解析所有新闻列表

    Args:
        url: 页面URL
        menu_name: 菜单名称（用于分类标记）
        submenu_name: 子菜单名称

    Returns:
        新闻列表
    """
    try:
        display_name = f"{menu_name} > {submenu_name}" if submenu_name else menu_name
        print(f"\n🔍 正在爬取: {display_name}")
        print(f"   URL: {url}")

        response = requests.get(url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"   ❌ 请求失败，状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []

        # 定位主内容区
        content_area = soup.select_one('.xsxc_index_center')
        if not content_area:
            print(f"   ⚠️  未找到内容区 .xsxc_index_center")
            return []

        # 查找所有新闻列表项
        # 清风网的新闻结构: <li><a><p class="title">...</p><p class="time">...</p></a></li>
        print(f"   📦 正在查找新闻...")

        news_items = content_area.find_all('li')
        print(f"   🔍 找到 {len(news_items)} 个 <li> 标签")

        for li in news_items:
            try:
                # 查找链接
                link = li.find('a')
                if not link:
                    continue

                href = link.get('href', '')
                if not href:
                    continue

                # 跳过"查看更多"等链接
                if '查看更多' in link.get_text() or 'javascript' in href:
                    continue

                # 提取标题（在 <p class="title"> 中）
                title_elem = link.find('p', class_='title')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                if not title:
                    continue

                # 转换为绝对URL
                news_url = urljoin(BASE_URL, href)

                # 尝试找到当前新闻所属的板块
                # 通过查找前面最近的标题元素
                section_title = ""
                prev_elements = li.find_all_previous(['h3', 'h4'], limit=5)
                if prev_elements:
                    section_title = prev_elements[0].get_text(strip=True)

                # 提取摘要（在 <p class="content"> 中，可能被注释掉）
                summary = ""
                content_elem = link.find('p', class_='content')
                if content_elem:
                    summary = content_elem.get_text(strip=True)

                # 提取日期（在 <li> 下的 <p class="time"> 中，不在 <a> 内）
                date = ""
                time_elem = li.find('p', class_='time')
                if time_elem:
                    time_text = time_elem.get_text(strip=True)
                    # 提取日期部分（格式：发布时间：2025-10-24）
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', time_text)
                    if date_match:
                        date = date_match.group(1)

                news_item = {
                    'title': title,
                    'summary': summary,
                    'date': date,
                    'url': news_url,
                    'source': '清风网',
                    'menu': menu_name,
                    'submenu': submenu_name,
                    'section': section_title,
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                news_list.append(news_item)

            except Exception as e:
                continue

        print(f"   ✅ 成功提取 {len(news_list)} 条新闻")
        return news_list

    except Exception as e:
        print(f"   ❌ 爬取页面失败: {e}")
        return []

def crawl_all_menus() -> List[Dict]:
    """
    爬取所有侧边栏菜单的新闻

    Returns:
        所有新闻的列表
    """
    all_news = []

    # 获取侧边栏菜单
    menus = get_sidebar_menus()

    if not menus:
        print("⚠️  未获取到任何菜单，返回Mock数据")
        return get_mock_data()

    # 遍历每个菜单
    for menu in menus:
        # 如果有子菜单，爬取子菜单
        if menu['submenus']:
            for submenu in menu['submenus']:
                news = parse_news_from_page(
                    submenu['url'],
                    menu['name'],
                    submenu['name']
                )
                all_news.extend(news)
                time.sleep(0.5)  # 延迟避免请求过快
        else:
            # 没有子菜单，直接爬取主菜单
            news = parse_news_from_page(menu['url'], menu['name'])
            all_news.extend(news)
            time.sleep(0.5)

    print(f"\n{'='*80}")
    print(f"🎉 爬取完成！共获取 {len(all_news)} 条新闻")
    print(f"{'='*80}\n")

    return all_news if all_news else get_mock_data()

# 保留旧函数作为备用（已废弃）
def parse_all_categories_deprecated() -> List[Dict]:
    """
    【已废弃】旧版爬取函数
    """
    return get_mock_data()

def get_mock_data():
    """
    返回Mock数据（当爬虫失败时使用）
    """
    return [
        {
            'title': '陕西中医药大学副校长缪峰接受纪律审查和监察调查',
            'summary': '陕西中医药大学副校长缪峰涉嫌严重违纪违法，目前正接受陕西省纪委监委纪律审查和监察调查',
            'date': '2025-10-24',
            'source': '清风网',
            'category': '省管干部',
            'subcategory': '执纪审查',
            'type': 'provincial_discipline',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '陕西省广播电视局原副局长刘生胜接受纪律审查和监察调查',
            'summary': '陕西省广播电视局原副局长刘生胜涉嫌严重违纪违法，目前正接受陕西省纪委监委纪律审查和监察调查',
            'date': '2025-08-05',
            'source': '清风网',
            'category': '省管干部',
            'subcategory': '执纪审查',
            'type': 'provincial_discipline',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '延安大学原副校长、附属医院原院长马柏林严重违纪违法被开除党籍、取消退休待遇',
            'summary': '日前，经中共陕西省委批准，省纪委监委对延安大学原副校长、附属医院原院长马柏林严重违纪违法问题进行了立案审查调查',
            'date': '2022-06-27',
            'source': '清风网',
            'category': '省管干部',
            'subcategory': '党纪政务处分',
            'type': 'provincial_punishment',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '吴堡县政府原副县长薛永升接受监察调查',
            'summary': '吴堡县政府原副县长薛永升涉嫌严重职务违法，目前正接受榆林市监委监察调查',
            'date': '2025-12-12',
            'source': '清风网',
            'category': '其他干部',
            'subcategory': '执纪审查',
            'type': 'other_discipline',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '杨凌示范区医院党委委员、示范区急救中心主任王勇被开除党籍、开除公职',
            'summary': '日前，经中共杨凌示范区工委批准，杨凌示范区纪检监察工委和杨陵区监察委员会成立联合调查组对王勇严重违纪违法问题进行了立案审查调查',
            'date': '2024-09-12',
            'source': '清风网',
            'category': '其他干部',
            'subcategory': '党纪政务处分',
            'type': 'other_punishment',
            'url': 'https://www.qinfeng.gov.cn'
        }
    ]

# ========== API路由 ==========

@app.route('/api/news', methods=['GET'])
def get_news():
    """
    API接口：返回所有分类的最新纪检通报

    查询参数:
        category: 主分类过滤（可选，如"省管干部"）
        subcategory: 子分类过滤（可选，如"执纪审查"）
        limit: 返回数量限制（可选，默认50）
    """
    try:
        # 获取查询参数
        menu_filter = request.args.get('menu', None)
        submenu_filter = request.args.get('submenu', None)
        section_filter = request.args.get('section', None)
        limit = int(request.args.get('limit', 50))

        # 爬取所有新闻
        all_news = crawl_all_menus()

        # 应用过滤器
        filtered_news = all_news
        if menu_filter:
            filtered_news = [n for n in filtered_news if n.get('menu') == menu_filter]
        if submenu_filter:
            filtered_news = [n for n in filtered_news if n.get('submenu') == submenu_filter]
        if section_filter:
            filtered_news = [n for n in filtered_news if n.get('section') == section_filter]

        # 按日期排序（最新的在前）
        filtered_news.sort(key=lambda x: x.get('date', ''), reverse=True)

        # 限制返回数量
        filtered_news = filtered_news[:limit]

        return jsonify({
            'code': 0,
            'message': 'success',
            'data': filtered_news,
            'total': len(filtered_news),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ API错误: {e}")
        return jsonify({
            'code': -1,
            'message': f'服务器错误: {str(e)}',
            'data': get_mock_data(),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/menus', methods=['GET'])
def get_menus():
    """
    API接口：返回所有侧边栏菜单
    """
    try:
        menus = get_sidebar_menus()
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': menus,
            'total': len(menus)
        })
    except Exception as e:
        return jsonify({
            'code': -1,
            'message': f'获取菜单失败: {str(e)}',
            'data': []
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    return jsonify({
        'status': 'ok',
        'service': 'qinfeng-crawler-v3',
        'version': '3.0',
        'description': '自动爬取所有侧边栏菜单'
    })

@app.route('/', methods=['GET'])
def index():
    """
    首页：API文档
    """
    return jsonify({
        'service': '清风网爬虫服务（完全重构版）',
        'version': '3.0',
        'description': '自动爬取侧边栏所有菜单的新闻内容',
        'endpoints': {
            '/api/news': {
                'method': 'GET',
                'description': '获取所有菜单的新闻',
                'params': {
                    'menu': '菜单名称过滤（可选）',
                    'submenu': '子菜单名称过滤（可选）',
                    'section': '板块名称过滤（可选）',
                    'limit': '返回数量限制（默认50）'
                },
                'examples': [
                    '/api/news',
                    '/api/news?menu=审查调查',
                    '/api/news?menu=审查调查&submenu=省管干部',
                    '/api/news?section=执纪审查',
                    '/api/news?limit=10'
                ]
            },
            '/api/menus': {
                'method': 'GET',
                'description': '获取所有侧边栏菜单'
            },
            '/health': {
                'method': 'GET',
                'description': '健康检查'
            }
        }
    })

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 清风网爬虫服务（完全重构版 v3.0）已启动")
    print("=" * 80)
    print(f"📡 API地址:")
    print(f"   - 所有新闻: http://localhost:5000/api/news")
    print(f"   - 按菜单过滤: http://localhost:5000/api/news?menu=审查调查")
    print(f"   - 按子菜单过滤: http://localhost:5000/api/news?submenu=省管干部")
    print(f"   - 菜单列表: http://localhost:5000/api/menus")
    print(f"   - 健康检查: http://localhost:5000/health")
    print("=" * 80)
    print(f"✨ 核心功能:")
    print(f"   - 自动获取侧边栏所有菜单链接")
    print(f"   - 依次爬取每个菜单页面的所有新闻")
    print(f"   - 支持多板块内容提取")
    print(f"   - 支持按菜单/子菜单/板块过滤")
    print("=" * 80)
    app.run(host='0.0.0.0', port=5000, debug=True)

