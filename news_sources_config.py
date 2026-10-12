#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多源新闻网站配置
包含清风网、中央纪委国家监委网站、陕西省纪委监委等多个新闻源
"""

# 新闻源配置
NEWS_SOURCES = {
    "清风网": {
        "name": "清风网",
        "base_url": "https://www.qinfeng.gov.cn",
        "enabled": True,
        "priority": 1,
        "regions": {
            "西安": "https://www.qinfeng.gov.cn/jdpg1/xa.htm",
            "宝鸡": "https://www.qinfeng.gov.cn/jdpg1/bj.htm",
            "咸阳": "https://www.qinfeng.gov.cn/jdpg1/xy.htm",
            "渭南": "https://www.qinfeng.gov.cn/jdpg1/wn.htm",
            "铜川": "https://www.qinfeng.gov.cn/jdpg1/tc.htm",
            "延安": "https://www.qinfeng.gov.cn/jdpg1/ya.htm",
            "榆林": "https://www.qinfeng.gov.cn/jdpg1/yl.htm",
            "汉中": "https://www.qinfeng.gov.cn/jdpg1/hz.htm",
            "安康": "https://www.qinfeng.gov.cn/jdpg1/ak.htm",
            "商洛": "https://www.qinfeng.gov.cn/jdpg1/sl.htm"
        }
    },
    
    "中央纪委国家监委网站": {
        "name": "中央纪委国家监委网站",
        "base_url": "https://www.ccdi.gov.cn",
        "enabled": True,
        "priority": 2,
        "urls": [
            "https://www.ccdi.gov.cn/scdc/",  # 审查调查
            "https://www.ccdi.gov.cn/toutiao/",  # 头条
            "https://www.ccdi.gov.cn/yaowenn/"  # 要闻
        ]
    },
    
    "陕西省纪委监委": {
        "name": "陕西省纪委监委",
        "base_url": "http://www.sxdi.gov.cn",
        "enabled": True,
        "priority": 3,
        "urls": [
            "http://www.sxdi.gov.cn/xwzx/sxyw/",  # 陕西要闻
            "http://www.sxdi.gov.cn/xwzx/scdc/"   # 审查调查
        ]
    },
    
    "人民网-反腐倡廉": {
        "name": "人民网-反腐倡廉",
        "base_url": "http://fanfu.people.com.cn",
        "enabled": True,
        "priority": 4,
        "urls": [
            "http://fanfu.people.com.cn/GB/394325/index.html"
        ]
    },
    
    "新华网-反腐": {
        "name": "新华网-反腐",
        "base_url": "http://www.xinhuanet.com",
        "enabled": True,
        "priority": 5,
        "urls": [
            "http://www.xinhuanet.com/politics/fan/"
        ]
    },
    
    "西安市纪委监委": {
        "name": "西安市纪委监委",
        "base_url": "http://www.xajw.gov.cn",
        "enabled": False,  # 暂时禁用，需要测试
        "priority": 6,
        "urls": [
            "http://www.xajw.gov.cn/xwzx/"
        ]
    }
}

# 获取启用的新闻源
def get_enabled_sources():
    """获取所有启用的新闻源"""
    return {k: v for k, v in NEWS_SOURCES.items() if v.get('enabled', False)}

# 获取新闻源列表（用于前端展示）
def get_source_list():
    """获取新闻源名称列表"""
    return [source['name'] for source in NEWS_SOURCES.values() if source.get('enabled', False)]

# 获取地区对应的新闻源
def get_region_sources(region_name):
    """获取指定地区的所有新闻源"""
    sources = []
    
    # 清风网地区链接
    if region_name in NEWS_SOURCES['清风网']['regions']:
        sources.append({
            'name': '清风网',
            'url': NEWS_SOURCES['清风网']['regions'][region_name]
        })
    
    # 其他全国性新闻源
    for source_key, source_config in NEWS_SOURCES.items():
        if source_config.get('enabled') and source_key != '清风网':
            sources.append({
                'name': source_config['name'],
                'url': source_config['base_url']
            })
    
    return sources

if __name__ == '__main__':
    print("启用的新闻源：")
    for name in get_source_list():
        print(f"  - {name}")
    
    print("\n西安市的新闻源：")
    for source in get_region_sources('西安'):
        print(f"  - {source['name']}: {source['url']}")

