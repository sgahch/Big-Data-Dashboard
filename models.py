# -*- coding: utf-8 -*-
"""
数据库模型 - SQLite
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import os

DB_FILE = 'crawler.db'


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_connection()
    cursor = conn.cursor()

    # 新闻表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT,
            date TEXT,
            url TEXT UNIQUE,
            source TEXT,
            region TEXT,
            menu TEXT,
            submenu TEXT,
            region_code TEXT,
            tags TEXT,
            crawl_time TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 标签表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            keywords TEXT,
            description TEXT,
            color TEXT DEFAULT '#00D2FF'
        )
    ''')

    # 爬取日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_code TEXT,
            region_name TEXT,
            total_crawled INTEGER,
            new_count INTEGER,
            status TEXT,
            error_message TEXT,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 初始化默认标签
    init_default_tags(cursor)

    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成: {DB_FILE}")


def init_default_tags(cursor):
    """初始化默认标签"""
    default_tags = [
        # 违规事项分布标签
        ('违反八项规定', '违规类型', '公款吃喝|礼品礼金|违规发放|公车私用|公款旅游', '违反中央八项规定精神', '#FF6B9D'),
        ('形式主义官僚主义', '违规类型', '形式主义|官僚主义|不作为|慢作为|乱作为|推诿扯皮', '形式主义和官僚主义问题', '#FFA502'),
        ('贪污受贿', '违规类型', '贪污|受贿|挪用公款|侵占挪用', '贪污贿赂类违纪违法', '#F8B500'),
        ('滥用职权', '违规类型', '滥用职权|玩忽职守|徇私枉法', '滥用职权类违纪违法', '#00D2FF'),
        ('失职渎职', '违规类型', '失职|渎职|监管不力|履职不力', '失职渎职类违纪违法', '#9933FF'),
        ('违规插手工程', '违规类型', '工程|招标|采购|土地|建设', '违规插手工程建设和矿产开发', '#3EECAC'),
        ('扶贫领域', '违规类型', '扶贫|脱贫|惠农|低保|困难群众', '扶贫领域违纪违法', '#17B978'),
        ('教育医疗', '违规类型', '教育|学校|医疗|医保|医院|招生', '教育医疗领域违纪违法', '#0080FF'),
        ('生态环保', '违规类型', '生态|环保|污染|环境|督察', '生态环保领域违纪违法', '#00C4B4'),

        # 案件查处统计标签
        ('省管干部', '干部级别', '省管|副省级|正厅级|副厅级', '省管干部违纪违法', '#FF6B9D'),
        ('市管干部', '干部级别', '市管|正处级|副处级', '市管干部违纪违法', '#00D2FF'),
        ('县管干部', '干部级别', '县管|正科级|副科级', '县管干部违纪违法', '#9933FF'),
        ('基层干部', '干部级别', '科员|办事员|村干部|社区干部', '基层干部违纪违法', '#3EECAC'),

        ('执纪审查', '案件状态', '接受纪律审查|接受监察调查|审查调查', '正在接受审查调查', '#FFA502'),
        ('党纪处分', '案件状态', '开除党籍|严重警告|警告|留党察看', '受到党纪处分', '#FF6B9D'),
        ('政务处分', '案件状态', '开除公职|政务撤职|政务降级|政务警告', '受到政务处分', '#00D2FF'),
        ('双开', '案件状态', '开除党籍.*开除公职|双开', '被双开', '#FF4444'),
    ]

    for name, category, keywords, description, color in default_tags:
        try:
            cursor.execute(
                'INSERT OR IGNORE INTO tags (name, category, keywords, description, color) VALUES (?, ?, ?, ?, ?)',
                (name, category, keywords, description, color)
            )
        except:
            pass


# ========== 新闻操作 ==========

def insert_news(news_list: List[Dict], region_code: str) -> int:
    """插入新闻，返回新增数量"""
    conn = get_connection()
    cursor = conn.cursor()

    new_count = 0
    for news in news_list:
        try:
            # 检查是否已存在
            cursor.execute('SELECT id FROM news WHERE url = ?', (news['url'],))
            if cursor.fetchone():
                continue

            # 自动打标签
            tags = auto_tagging(news['title'] + ' ' + (news.get('summary', '') or ''))
            tags_str = ','.join(tags)

            cursor.execute('''
                INSERT INTO news (title, summary, date, url, source, region, menu, submenu, region_code, tags, crawl_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                news['title'], news['summary'], news['date'], news['url'],
                news.get('source', ''), news.get('region', ''),
                news.get('menu', ''), news.get('submenu', ''),
                region_code, tags_str, news.get('crawl_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            ))
            new_count += 1
        except Exception as e:
            print(f"插入失败: {e}")
            continue

    conn.commit()
    conn.close()
    return new_count


def get_news(limit: int = 100, region: str = None, tag: str = None, news_id: int = None) -> List[Dict]:
    """获取新闻列表"""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM news WHERE 1=1'
    params = []

    if news_id:
        query += ' AND id = ?'
        params.append(news_id)

    if region and region != 'all':
        query += ' AND region_code = ?'
        params.append(region)

    if tag:
        query += ' AND tags LIKE ?'
        params.append(f'%{tag}%')

    if not news_id:  # 只有非详情查询才需要limit和排序
        query += ' ORDER BY date DESC, crawl_time DESC LIMIT ?'
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_news_by_date(start_date: str, end_date: str = None) -> List[Dict]:
    """按日期范围获取新闻"""
    conn = get_connection()
    cursor = conn.cursor()

    if end_date:
        cursor.execute(
            'SELECT * FROM news WHERE date BETWEEN ? AND ? ORDER BY date DESC',
            (start_date, end_date)
        )
    else:
        cursor.execute(
            'SELECT * FROM news WHERE date >= ? ORDER BY date DESC',
            (start_date,)
        )

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ========== 标签操作 ==========

def auto_tagging(text: str) -> List[str]:
    """根据文本内容自动打标签"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, keywords FROM tags')
    tags = cursor.fetchall()
    conn.close()

    matched = []
    for tag in tags:
        keywords = tag['keywords'].split('|')
        for keyword in keywords:
            if keyword and keyword in text:
                matched.append(tag['name'])
                break

    return list(set(matched))  # 去重


def get_all_tags() -> Dict[str, List[Dict]]:
    """获取所有标签，按分类分组"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tags ORDER BY category, name')
    rows = cursor.fetchall()
    conn.close()

    result = {}
    for row in rows:
        category = row['category']
        if category not in result:
            result[category] = []
        result[category].append(dict(row))

    return result


# ========== 统计操作 ==========

def get_violation_stats() -> List[Dict]:
    """获取违规事项分布统计"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT tags, COUNT(*) as count FROM news
        WHERE tags != '' AND tags IS NOT NULL
        GROUP BY tags
    ''')

    rows = cursor.fetchall()
    conn.close()

    # 统计每个标签的数量
    stats = {}
    for row in rows:
        tags = (row['tags'] or '').split(',')
        for tag in tags:
            tag = tag.strip()
            if tag:
                stats[tag] = stats.get(tag, 0) + row['count']

    # 按数量排序
    result = [{'name': k, 'value': v} for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)]
    return result


def get_case_stats(months: int = 12) -> Dict:
    """获取案件查处统计（按月）"""
    conn = get_connection()
    cursor = conn.cursor()

    # 获取最近月份的统计
    cursor.execute(f'''
        SELECT
            strftime('%Y-%m', date) as month,
            COUNT(*) as count
        FROM news
        WHERE date >= date('now', '-{months} months')
        GROUP BY month
        ORDER BY month DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    months_list = []
    values_list = []

    for row in rows:
        months_list.append(row['month'].replace('2025-', '') + '月')
        values_list.append(row['count'])

    return {
        'months': list(reversed(months_list)),
        'values': list(reversed(values_list))
    }


def get_region_stats() -> List[Dict]:
    """获取各地区新闻数量统计"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT region, region_code, COUNT(*) as count
        FROM news
        WHERE region IS NOT NULL AND region != ''
        GROUP BY region
        ORDER BY count DESC
    ''')

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ========== 日志操作 ==========

def log_crawl(region_code: str, region_name: str, total: int, new_count: int, status: str, error: str = None):
    """记录爬取日志"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO crawl_logs (region_code, region_name, total_crawled, new_count, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (region_code, region_name, total, new_count, status, error))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
