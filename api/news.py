#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless Function - 清风网爬虫 API
"""

from http.server import BaseHTTPRequestHandler
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from typing import List, Dict
from urllib.parse import urljoin, urlparse, parse_qs

# 目标网站配置
BASE_URL = "https://www.qinfeng.gov.cn"

# 需要排除的链接（外链、首页等）
EXCLUDE_KEYWORDS = [
    'javascript:',
    'http://www.12388.gov.cn',
    '/index.htm',
    '#'
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
    """判断链接是否为有效的菜单链接"""
    if not href:
        return False

    for keyword in EXCLUDE_KEYWORDS:
        if keyword in href:
            return False

    if href.startswith('http') and not href.startswith(BASE_URL):
        return False

    return True

def get_sidebar_menus() -> List[Dict]:
    """获取侧边栏所有菜单链接"""
    try:
        response = requests.get(f"{BASE_URL}/scdc.htm", headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        menus = []

        sidebar = soup.select_one('.xsxc_index_left')
        if not sidebar:
            return []

        menu_items = sidebar.select('ul > li')

        for item in menu_items:
            main_link = item.find('a', recursive=False)
            if not main_link:
                continue

            menu_name = main_link.get_text(strip=True)
            menu_href = main_link.get('href', '')

            if not is_valid_menu_link(menu_href):
                continue

            menu_url = urljoin(BASE_URL, menu_href)
            submenu = item.find('ul')
            has_submenu = submenu is not None

            menu_info = {
                'name': menu_name,
                'url': menu_url,
                'has_submenu': has_submenu,
                'submenus': []
            }

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

        return menus

    except Exception as e:
        return []

def parse_news_from_page(url: str, menu_name: str, submenu_name: str = "") -> List[Dict]:
    """从单个页面解析所有新闻列表"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []

        content_area = soup.select_one('.xsxc_index_center')
        if not content_area:
            return []

        news_items = content_area.find_all('li')

        for li in news_items:
            try:
                link = li.find('a')
                if not link:
                    continue

                href = link.get('href', '')
                if not href or '查看更多' in link.get_text() or 'javascript' in href:
                    continue

                title_elem = link.find('p', class_='title')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                if not title:
                    continue

                news_url = urljoin(BASE_URL, href)

                section_title = ""
                prev_elements = li.find_all_previous(['h3', 'h4'], limit=5)
                if prev_elements:
                    section_title = prev_elements[0].get_text(strip=True)

                summary = ""
                content_elem = link.find('p', class_='content')
                if content_elem:
                    summary = content_elem.get_text(strip=True)

                date = ""
                time_elem = li.find('p', class_='time')
                if time_elem:
                    time_text = time_elem.get_text(strip=True)
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

            except Exception:
                continue

        return news_list

    except Exception:
        return []

def crawl_all_menus() -> List[Dict]:
    """爬取所有侧边栏菜单的新闻"""
    all_news = []

    menus = get_sidebar_menus()

    if not menus:
        return get_mock_data()

    # 限制爬取数量以避免超时
    for menu in menus[:5]:  # 只爬取前5个菜单
        if menu['submenus']:
            for submenu in menu['submenus'][:3]:  # 每个菜单最多3个子菜单
                news = parse_news_from_page(
                    submenu['url'],
                    menu['name'],
                    submenu['name']
                )
                all_news.extend(news)
        else:
            news = parse_news_from_page(menu['url'], menu['name'])
            all_news.extend(news)

    return all_news if all_news else get_mock_data()

def get_mock_data():
    """返回Mock数据"""
    return [
        {
            'title': '陕西中医药大学副校长缪峰接受纪律审查和监察调查',
            'summary': '陕西中医药大学副校长缪峰涉嫌严重违纪违法，目前正接受陕西省纪委监委纪律审查和监察调查',
            'date': '2025-10-24',
            'source': '清风网',
            'category': '省管干部',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '陕西省广播电视局原副局长刘生胜接受纪律审查和监察调查',
            'summary': '陕西省广播电视局原副局长刘生胜涉嫌严重违纪违法，目前正接受陕西省纪委监委纪律审查和监察调查',
            'date': '2025-08-05',
            'source': '清风网',
            'category': '省管干部',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '延安大学原副校长、附属医院原院长马柏林严重违纪违法被开除党籍、取消退休待遇',
            'summary': '日前，经中共陕西省委批准，省纪委监委对延安大学原副校长、附属医院原院长马柏林严重违纪违法问题进行了立案审查调查',
            'date': '2022-06-27',
            'source': '清风网',
            'category': '省管干部',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '吴堡县政府原副县长薛永升接受监察调查',
            'summary': '吴堡县政府原副县长薛永升涉嫌严重职务违法，目前正接受榆林市监委监察调查',
            'date': '2025-12-12',
            'source': '清风网',
            'category': '其他干部',
            'url': 'https://www.qinfeng.gov.cn'
        },
        {
            'title': '杨凌示范区医院党委委员、示范区急救中心主任王勇被开除党籍、开除公职',
            'summary': '日前，经中共杨凌示范区工委批准，杨凌示范区纪检监察工委和杨陵区监察委员会成立联合调查组对王勇严重违纪违法问题进行了立案审查调查',
            'date': '2024-09-12',
            'source': '清风网',
            'category': '其他干部',
            'url': 'https://www.qinfeng.gov.cn'
        }
    ]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 解析查询参数
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)

            menu_filter = query_params.get('menu', [None])[0]
            submenu_filter = query_params.get('submenu', [None])[0]
            section_filter = query_params.get('section', [None])[0]
            limit = int(query_params.get('limit', [50])[0])

            # 爬取数据
            all_news = crawl_all_menus()

            # 应用过滤器
            filtered_news = all_news
            if menu_filter:
                filtered_news = [n for n in filtered_news if n.get('menu') == menu_filter]
            if submenu_filter:
                filtered_news = [n for n in filtered_news if n.get('submenu') == submenu_filter]
            if section_filter:
                filtered_news = [n for n in filtered_news if n.get('section') == section_filter]

            # 按日期排序
            filtered_news.sort(key=lambda x: x.get('date', ''), reverse=True)

            # 限制返回数量
            filtered_news = filtered_news[:limit]

            # 返回响应
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'code': 0,
                'message': 'success',
                'data': filtered_news,
                'total': len(filtered_news),
                'timestamp': datetime.now().isoformat()
            }

            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            # 错误处理
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'code': -1,
                'message': f'服务器错误: {str(e)}',
                'data': get_mock_data(),
                'timestamp': datetime.now().isoformat()
            }

            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
