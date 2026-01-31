# -*- coding: utf-8 -*-
"""
缓存模块
支持 Redis 和内存缓存
"""
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

# 缓存默认超时时间（秒）
DEFAULT_TIMEOUT = 300  # 5分钟
LONG_TIMEOUT = 1800    # 30分钟


def get_cache_key(prefix, **kwargs):
    """生成缓存键"""
    key_parts = [prefix]
    for k, v in sorted(kwargs.items()):
        key_parts.append(f'{k}_{v}')
    return '_'.join(key_parts)


class CacheManager:
    """缓存管理器"""

    @staticmethod
    def get(key, default=None):
        """获取缓存"""
        try:
            result = cache.get(key)
            if result is not None:
                return result
        except Exception as e:
            logger.warning(f' {e}')
       缓存获取失败: return default

    @staticmethod
    def set(key, value, timeout=DEFAULT_TIMEOUT):
        """设置缓存"""
        try:
            cache.set(key, value, timeout)
            return True
        except Exception as e:
            logger.warning(f'缓存设置失败: {e}')
            return False

    @staticmethod
    def delete(key):
        """删除缓存"""
        try:
            cache.delete(key)
            return True
        except Exception as e:
            logger.warning(f'缓存删除失败: {e}')
            return False

    @staticmethod
    def delete_pattern(pattern):
        """删除匹配模式的缓存"""
        try:
            # Redis 支持模式删除
            keys = cache.keys(pattern)
            if keys:
                cache.delete_many(keys)
            return True
        except Exception as e:
            logger.warning(f'缓存模式删除失败: {e}')
            return False

    @staticmethod
    def clear_stats_cache():
        """清除统计相关缓存"""
        return CacheManager.delete_pattern('stats_*')

    @staticmethod
    def clear_news_cache():
        """清除新闻相关缓存"""
        return CacheManager.delete_pattern('news_*')


def cached_property(timeout=DEFAULT_TIMEOUT):
    """装饰器：为方法结果添加缓存"""
    def decorator(func):
        def wrapper(self):
            # 从实例属性获取缓存
            cache_attr = f'_cache_{func.__name__}'
            if not hasattr(self, cache_attr):
                result = func(self)
                if result is not None:
                    setattr(self, cache_attr, result)
            return getattr(self, cache_attr)
        return wrapper
    return decorator


# 预定义的缓存键生成函数
def stats_dashboard_key():
    return 'stats_dashboard'

def stats_violations_key():
    return 'stats_violations'

def stats_cases_key(months=12):
    return f'stats_cases_{months}'

def stats_regions_key():
    return 'stats_regions'

def news_list_key(region='all', page=1):
    return f'news_list_{region}_{page}'

def news_detail_key(news_id):
    return f'news_detail_{news_id}'
