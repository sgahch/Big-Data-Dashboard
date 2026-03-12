# -*- coding: utf-8 -*-
"""
配置文件
"""

import os

# ========== 数据库配置 ==========
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '20060424007Hq265'),
    'database': os.getenv('DB_NAME', 'supervision'),
    'charset': 'utf8mb4',
    'pool_size': 10,
    'pool_recycle': 3600
}

# ========== Redis配置（可选，用于缓存） ==========
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'key_prefix': 'supervision:'
}

# ========== 爬虫配置 ==========
CRAWLER_CONFIG = {
    'request_timeout': 15,
    'retry_times': 3,
    'retry_delay': 2,
    'request_interval': 0.5,  # 请求间隔（秒）
    'max_workers': 5,  # 并发爬取线程数
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ========== 调度器配置 ==========
SCHEDULER_CONFIG = {
    'crawl_interval_hours': 4,  # 爬取间隔（小时）
    'crawl_daily_hour': 8,  # 每天定时爬取时间
    'timezone': 'Asia/Shanghai'
}

# ========== 标签配置 ==========
TAG_CATEGORIES = {
    '违规类型': {
        '违反八项规定': ['公款吃喝', '礼品礼金', '违规发放', '公车私用', '公款旅游'],
        '形式主义官僚主义': ['形式主义', '官僚主义', '不作为', '慢作为', '乱作为', '推诿扯皮'],
        '贪污受贿': ['贪污', '受贿', '挪用公款', '侵占挪用'],
        '滥用职权': ['滥用职权', '玩忽职守', '徇私枉法'],
        '失职渎职': ['失职', '渎职', '监管不力', '履职不力'],
        '违规插手工程': ['工程', '招标', '采购', '土地', '建设'],
        '扶贫领域': ['扶贫', '脱贫', '惠农', '低保', '困难群众'],
        '教育医疗': ['教育', '学校', '医疗', '医保', '医院', '招生'],
        '生态环保': ['生态', '环保', '污染', '环境', '督察']
    },
    '干部级别': {
        '省管干部': ['省管', '副省级', '正厅级', '副厅级'],
        '市管干部': ['市管', '正处级', '副处级'],
        '县管干部': ['县管', '正科级', '副科级'],
        '基层干部': ['科员', '办事员', '村干部', '社区干部']
    },
    '案件状态': {
        '执纪审查': ['接受纪律审查', '接受监察调查', '审查调查'],
        '党纪处分': ['开除党籍', '严重警告', '警告', '留党察看'],
        '政务处分': ['开除公职', '政务撤职', '政务降级', '政务警告'],
        '双开': ['开除党籍.*开除公职', '双开']
    }
}

# ========== 地区配置 ==========
REGIONS = {
    'xian': {'name': '西安市', 'domain': 'xian.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'baoji': {'name': '宝鸡市', 'domain': 'baoji.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'xianyang': {'name': '咸阳市', 'domain': 'xianyang.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'tongchuan': {'name': '铜川市', 'domain': 'tongchuan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'weinan': {'name': '渭南市', 'domain': 'weinan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yanan': {'name': '延安市', 'domain': 'yanan.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yulin': {'name': '榆林市', 'domain': 'yulin.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'hanzhong': {'name': '汉中市', 'domain': 'hanzhong.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'ankang': {'name': '安康市', 'domain': 'ankang.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'shangluo': {'name': '商洛市', 'domain': 'shangluo.qinfeng.gov.cn', 'path': 'scdc.htm'},
    'yangling': {'name': '杨凌示范区', 'domain': 'yangling.qinfeng.gov.cn', 'path': 'scdc.htm'}
}

# ========== Flask配置 ==========
FLASK_CONFIG = {
    'debug': os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
    'host': '0.0.0.0',
    'port': int(os.getenv('FLASK_PORT', 5000)),
    'secret_key': os.getenv('SECRET_KEY', 'your-secret-key')
}

# ========== 日志配置 ==========
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/app.log',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}
