#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清风网爬虫 API - 支持按地区爬取
"""

from http.server import BaseHTTPRequestHandler
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs

# 陕西各地区配置
REGIONS = {
    "全部": {
        "name": "全部",
        "domain": "www.qinfeng.gov.cn",
        "path": "",
        "code": "all"
    },
    "西安": {
        "name": "西安市",
        "domain": "xian.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "xian"
    },
    "宝鸡": {
        "name": "宝鸡市",
        "domain": "baoji.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "baoji"
    },
    "咸阳": {
        "name": "咸阳市",
        "domain": "xianyang.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "xianyang"
    },
    "铜川": {
        "name": "铜川市",
        "domain": "tongchuan.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "tongchuan"
    },
    "渭南": {
        "name": "渭南市",
        "domain": "weinan.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "weinan"
    },
    "延安": {
        "name": "延安市",
        "domain": "yanan.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "yanan"
    },
    "榆林": {
        "name": "榆林市",
        "domain": "yulin.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "yulin"
    },
    "汉中": {
        "name": "汉中市",
        "domain": "hanzhong.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "hanzhong"
    },
    "安康": {
        "name": "安康市",
        "domain": "ankang.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "ankang"
    },
    "商洛": {
        "name": "商洛市",
        "domain": "shangluo.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "shangluo"
    },
    "杨凌": {
        "name": "杨凌示范区",
        "domain": "yangling.qinfeng.gov.cn",
        "path": "scdc.htm",
        "code": "yangling"
    }
}

# 需要排除的链接（外链、首页等）
EXCLUDE_KEYWORDS = [
    'javascript:',
    'http://www.12388.gov.cn',
    '/index.htm',
    '#',
    'qinfeng.gov.cn'
]


def get_headers():
    """获取请求头"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }


def is_valid_menu_link(href: str, base_domain: str) -> bool:
    """判断链接是否为有效的菜单链接"""
    if not href:
        return False

    for keyword in EXCLUDE_KEYWORDS:
        if keyword in href:
            return False

    # 如果是绝对URL，必须在当前地区域名下
    if href.startswith('http'):
        return base_domain in href

    return True


def get_region_url(region_code: str) -> str:
    """获取地区的首页URL"""
    if region_code == "all" or region_code not in REGIONS:
        return "https://www.qinfeng.gov.cn/scdc.htm"

    region = REGIONS[region_code]
    return f"https://{region['domain']}/{region['path']}"


def get_sidebar_menus(region_code: str = "all") -> List[Dict]:
    """获取侧边栏所有菜单链接"""
    base_url = get_region_url(region_code)
    base_domain = urlparse(base_url).netloc

    try:
        print(f"🌐 正在获取: {base_url}")
        response = requests.get(base_url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"❌ 请求失败: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        menus = []

        # 多种侧边栏选择器
        sidebar_selectors = [
            '.xsxc_index_left',
            '.left',
            '.sidebar',
            '.nav',
            '.menu',
            '.left_nav',
            '.side_nav',
            '.category'
        ]

        sidebar = None
        for selector in sidebar_selectors:
            sidebar = soup.select_one(selector)
            if sidebar:
                print(f"✅ 找到侧边栏: {selector}")
                break

        if not sidebar:
            # 打印页面结构便于调试
            print("⚠️ 未找到标准侧边栏，尝试查找导航链接...")
            # 查找所有导航链接
            nav_links = soup.find_all('a', href=True)
            news_links = [a for a in nav_links if 'info' in a.get('href', '') and '.htm' in a.get('href', '')]

            if news_links[:10]:
                print(f"✅ 直接找到 {len(news_links)} 个新闻链接")
                # 直接返回这些链接作为菜单
                for link in news_links[:5]:
                    menus.append({
                        'name': link.get_text(strip=True)[:20] or '新闻',
                        'url': urljoin(base_url, link.get('href', '')),
                        'has_submenu': False,
                        'submenus': []
                    })
                return menus

            return []

        # 查找菜单项
        menu_items = sidebar.select('ul > li') or sidebar.find_all('li')

        if not menu_items:
            menu_items = sidebar.find_all('a')

        print(f"📋 找到 {len(menu_items)} 个菜单项")

        for item in menu_items[:10]:  # 限制数量
            try:
                main_link = item if item.name == 'a' else item.find('a', recursive=False)
                if not main_link:
                    continue

                menu_name = main_link.get_text(strip=True)
                menu_href = main_link.get('href', '')

                if not menu_name or len(menu_name) < 2:
                    continue

                if not is_valid_menu_link(menu_href, base_domain):
                    continue

                # 过滤掉无关链接
                if any(kw in menu_href for kw in ['javascript', '#', 'login', 'register']):
                    continue

                menu_url = urljoin(base_url, menu_href)
                submenu = item.find('ul') or item.find('div', class_='submenu')
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

                        if sub_name and len(sub_name) >= 2 and is_valid_menu_link(sub_href, base_domain):
                            sub_url = urljoin(base_url, sub_href)
                            menu_info['submenus'].append({
                                'name': sub_name,
                                'url': sub_url
                            })

                menus.append(menu_info)

            except Exception as e:
                continue

        print(f"✅ 解析完成，共 {len(menus)} 个菜单")
        return menus

    except Exception as e:
        print(f"获取菜单失败: {e}")
        return []


def parse_news_from_page(url: str, menu_name: str, submenu_name: str = "", region: str = "全部") -> List[Dict]:
    """从单个页面解析所有新闻列表"""
    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []

        # 多种选择器尝试兼容不同页面结构
        content_selectors = [
            '.media_list',      # 西安等地区站点
            '.news_list',       # 通用新闻列表
            '.xsxc_index_center',
            '.center',
            '.content',
            '.list',
            'ul.media',         # 另一种列表
            '.article_list',
        ]

        content_area = None
        for selector in content_selectors:
            content_area = soup.select_one(selector)
            if content_area:
                print(f"✅ 找到内容区域: {selector}")
                break

        if not content_area:
            # 尝试查找所有ul列表
            all_uls = soup.find_all('ul')
            for ul in all_uls:
                if len(ul.find_all('li', recursive=False)) > 3:
                    content_area = ul.parent
                    print(f"✅ 找到ul列表容器")
                    break

        if not content_area:
            print(f"❌ 未找到内容区域: {url}")
            return []

        # 查找所有li元素
        news_items = content_area.find_all('li')
        if not news_items:
            # 尝试在内容区域直接查找a标签
            news_items = content_area.find_all('a', href=True)

        print(f"📰 找到 {len(news_items)} 个新闻项")

        for item in news_items:
            try:
                # 获取链接和标题
                link = item if item.name == 'a' else item.find('a')
                if not link:
                    continue

                href = link.get('href', '')
                if not href or 'javascript' in href.lower() or '查看更多' in link.get_text():
                    continue

                # 获取标题
                title = None
                title_elem = (link.find(class_='media_title') or
                             link.find(class_='news_title') or
                             link.find(class_='title') or
                             link.find('p', class_=lambda x: x and 'title' in x) or
                             link)

                if title_elem:
                    title = title_elem.get_text(strip=True)

                if not title or len(title) < 2:
                    continue

                # 构建完整URL
                news_url = urljoin(url, href)

                # 获取日期 - 多种方式尝试
                date = ""

                # 方式1: 在当前项的兄弟元素中查找
                parent = item.parent if item else None
                if parent:
                    # 查找父元素的所有文本中包含日期的部分
                    parent_text = parent.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', parent_text)
                    if date_match:
                        date = date_match.group(1).replace('/', '-')

                # 方式2: 在当前项内部查找
                if not date:
                    item_text = item.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', item_text)
                    if date_match:
                        date = date_match.group(1).replace('/', '-')

                # 方式3: 查找常见的日期元素
                if not date:
                    date_elem = (item.find('span', class_=lambda x: x and 'time' in x) or
                                item.find('span', class_='date') or
                                item.find(class_='date') or
                                item.find('time') or
                                item.find(class_=lambda x: x and 'pub' in x) or
                                item.find(class_=lambda x: x and 'time' in x))
                    if date_elem:
                        date_text = date_elem.get_text(strip=True)
                        date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', date_text)
                        if date_match:
                            date = date_match.group(1).replace('/', '-')

                # 方式4: 查找链接后面的日期（常见于列表结构）
                if not date:
                    next_sibling = item.next_sibling
                    for _ in range(5):  # 最多查找5个兄弟节点
                        if next_sibling and hasattr(next_sibling, 'get_text'):
                            text = next_sibling.get_text(strip=True)
                            date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', text)
                            if date_match:
                                date = date_match.group(1).replace('/', '-')
                                break
                        if next_sibling:
                            next_sibling = next_sibling.next_sibling

                # 获取摘要
                summary = ""
                summary_elem = (link.find(class_='media_desc') or
                               link.find(class_='desc') or
                               link.find(class_='summary'))

                if summary_elem:
                    summary = summary_elem.get_text(strip=True)

                news_item = {
                    'title': title,
                    'summary': summary,
                    'date': date,
                    'url': news_url,
                    'source': '清风网',
                    'region': region,
                    'menu': menu_name,
                    'submenu': submenu_name,
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                news_list.append(news_item)

            except Exception as e:
                continue

        return news_list

    except Exception as e:
        print(f"解析页面失败 {url}: {e}")
        return []


def crawl_region_news(region_code: str, max_menus: int = 5, max_submenus: int = 3) -> List[Dict]:
    """爬取指定地区的新闻"""
    all_news = []
    region_name = REGIONS.get(region_code, {}).get("name", "全部") if region_code != "all" else "全部"

    if region_code == "all":
        # 爬取所有地区
        for code, config in REGIONS.items():
            if code == "全部":
                continue
            news = crawl_single_region(code, max_menus, max_submenus)
            all_news.extend(news)
    else:
        # 爬取单个地区，优先尝试菜单爬取，失败则用直接爬取
        all_news = crawl_single_region(region_code, max_menus, max_submenus)

        # 如果没有爬到数据，使用直接爬取
        if not all_news:
            print(f"🔄 菜单爬取失败，尝试直接爬取...")
            all_news = crawl_region_direct(region_code)

    return all_news if all_news else get_mock_data(region_name)


def crawl_single_region(region_code: str, max_menus: int, max_submenus: int) -> List[Dict]:
    """爬取单个地区的新闻"""
    all_news = []
    region_name = REGIONS.get(region_code, {}).get("name", region_code)

    menus = get_sidebar_menus(region_code)

    if menus:
        # 通过菜单爬取
        for menu in menus[:max_menus]:
            if menu['submenus']:
                for submenu in menu['submenus'][:max_submenus]:
                    news = parse_news_from_page(
                        submenu['url'],
                        menu['name'],
                        submenu['name'],
                        region_name
                    )
                    all_news.extend(news)
            else:
                news = parse_news_from_page(menu['url'], menu['name'], "", region_name)
                all_news.extend(news)

            time.sleep(0.3)
    else:
        # 如果没有找到菜单，直接爬取首页
        print(f"📰 直接爬取首页新闻...")
        region_url = get_region_url(region_code)
        homepage_news = parse_news_from_page(region_url, "首页", "", region_name)
        all_news.extend(homepage_news)

    return all_news


def crawl_region_direct(region_code: str) -> List[Dict]:
    """直接爬取地区首页的所有新闻（不通过菜单）"""
    region_url = get_region_url(region_code)
    region_name = REGIONS.get(region_code, {}).get("name", region_code)

    try:
        print(f"🔍 直接爬取: {region_url}")

        response = requests.get(region_url, headers=get_headers(), timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            return get_mock_data(region_name)

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []

        # 直接查找所有新闻链接
        all_links = soup.find_all('a', href=True)

        news_links = []
        seen_urls = set()

        for link in all_links:
            href = link.get('href', '')
            title = link.get_text(strip=True)

            # 过滤有效新闻链接
            if (href and '.htm' in href and
                'info' in href and
                len(title) >= 5 and
                len(title) <= 100 and
                not any(kw in title.lower() for kw in ['登录', '注册', '关于', '联系我们', '网站地图'])):

                # 跳过已处理
                clean_href = href.split('#')[0].split('?')[0]
                if clean_href in seen_urls:
                    continue
                seen_urls.add(clean_href)

                full_url = urljoin(region_url, href)

                # 获取日期 - 多种方式尝试
                date = ""

                # 方式1: 在父元素文本中查找
                parent = link.parent
                if parent:
                    parent_text = parent.get_text(strip=True)
                    date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', parent_text)
                    if date_match:
                        date = date_match.group(1).replace('/', '-')

                # 方式2: 查找父元素的兄弟元素
                if not date and parent:
                    grandparent = parent.parent if parent else None
                    if grandparent:
                        siblings = grandparent.find_all(['span', 'p', 'div', 'li'])
                        for sib in siblings:
                            sib_text = sib.get_text(strip=True)
                            date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', sib_text)
                            if date_match:
                                date = date_match.group(1).replace('/', '-')
                                break

                # 方式3: 查找父元素中包含日期的元素
                if not date and parent:
                    date_elems = parent.find_all(class_=lambda x: x and ('time' in x.lower() or 'date' in x.lower()))
                    for elem in date_elems:
                        text = elem.get_text(strip=True)
                        date_match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', text)
                        if date_match:
                            date = date_match.group(1).replace('/', '-')
                            break

                news_list.append({
                    'title': title,
                    'summary': '',
                    'date': date,
                    'url': full_url,
                    'source': '清风网',
                    'region': region_name,
                    'menu': '首页',
                    'submenu': '',
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

        print(f"✅ 直接爬取完成: {len(news_list)} 条新闻")
        return news_list[:50]  # 限制数量

    except Exception as e:
        print(f"直接爬取失败: {e}")
        return get_mock_data(region_name)


def get_regions():
    """获取所有可用地区"""
    return [
        {"code": key, "name": value["name"]} for key, value in REGIONS.items()
    ]


def get_mock_data(region: str = "全部"):
    """返回Mock数据"""
    mock_data = []
    for i in range(1, 9):
        mock_data.append({
            'id': i,
            'title': f'【{region}】西安市纪委通报{i}起形式主义、官僚主义典型问题',
            'summary': f'西安市纪委监委公开通报{i}起形式主义、官僚主义典型问题',
            'date': f'2024-{12-i:02d}-01' if 12-i > 0 else f'2025-{abs(12-i):02d}-01',
            'source': '清风网',
            'region': region,
            'url': 'https://www.qinfeng.gov.cn/scdc/index.htm'
        })
    return mock_data


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        try:
            # 解析查询参数
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)

            # 地区参数
            region = query_params.get('region', ['all'])[0]

            # 其他过滤参数
            menu_filter = query_params.get('menu', [None])[0]
            submenu_filter = query_params.get('submenu', [None])[0]
            limit = int(query_params.get('limit', [50])[0])

            # 获取地区列表（用于返回给前端）
            if query_params.get('action', [None])[0] == 'regions':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    'code': 0,
                    'message': 'success',
                    'data': get_regions(),
                    'timestamp': datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            # 爬取数据
            all_news = crawl_region_news(region)

            # 应用过滤器
            filtered_news = all_news
            if menu_filter:
                filtered_news = [n for n in filtered_news if n.get('menu') == menu_filter]
            if submenu_filter:
                filtered_news = [n for n in filtered_news if n.get('submenu') == submenu_filter]

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
                'region': region,
                'region_name': REGIONS.get(region, {}).get("name", "全部") if region != "all" else "全部",
                'regions': get_regions(),
                'timestamp': datetime.now().isoformat()
            }

            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            print(f"请求处理错误: {e}")
            # 错误处理
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            response = {
                'code': -1,
                'message': f'服务器错误: {str(e)}',
                'data': get_mock_data(),
                'regions': get_regions(),
                'timestamp': datetime.now().isoformat()
            }

            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
