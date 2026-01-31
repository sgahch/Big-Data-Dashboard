# -*- coding: utf-8 -*-
"""
智慧监督管理系统 - 爬虫测试脚本
测试爬虫功能、错误处理和稳定性
"""
import os
import sys
import time
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')

import django
django.setup()

from apps.crawler.crawler import crawl_region, crawl_all_regions, auto_tagging, REGIONS
from apps.crawler.scheduler import get_scheduler, init_scheduler
from apps.news.models import News, Region

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CrawlerTester:
    """爬虫测试类"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def log(self, test_name, passed, message=''):
        """记录测试结果"""
        status = 'PASS' if passed else 'FAIL'
        print(f'{status} | {test_name}: {message}')
        self.results.append({
            'name': test_name,
            'passed': passed,
            'message': message
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def test_auto_tagging(self):
        """测试自动标签功能"""
        print('\n' + '='*50)
        print('测试自动标签功能')
        print('='*50)

        test_cases = [
            ('西安市纪委监委通报3起违反中央八项规定精神问题', ['违反八项规定']),
            ('宝鸡市查处形式主义官僚主义典型案例', ['形式主义', '官僚主义']),
            ('咸阳市一名干部因贪污受贿被移送司法机关', ['贪污受贿']),
            ('渭南市通报失职渎职典型问题', ['失职渎职']),
            ('延安市纪委监委查处滥用职权案件', ['滥用职权']),
            ('榆林市一名干部被查，涉嫌严重违纪违法', ['违纪违法']),
            ('汉中市纪委监委通报违规收受礼品礼金问题', ['违规收受礼品礼金']),
            ('安康市查处群众身边腐败和作风问题', ['群众身边腐败', '作风问题']),
        ]

        for title, expected_tags in test_cases:
            try:
                result = auto_tagging(title)
                matched = all(tag in result for tag in expected_tags)
                self.log(f'标签测试: {title[:20]}...', matched,
                        f'Expected: {expected_tags}, Got: {result}')
            except Exception as e:
                self.log(f'标签测试: {title[:20]}...', False, str(e))

    def test_region_config(self):
        """测试地区配置"""
        print('\n' + '='*50)
        print('测试地区配置')
        print('='*50)

        # 检查所有地区配置
        for code, config in REGIONS.items():
            try:
                has_name = 'name' in config and config['name']
                has_domain = 'domain' in config and config['domain']
                has_path = 'path' in config and config['path']

                passed = has_name and has_domain and has_path
                self.log(f'地区配置 - {code}', passed,
                        f'name: {has_name}, domain: {has_domain}, path: {has_path}')
            except Exception as e:
                self.log(f'地区配置 - {code}', False, str(e))

        # 检查数据库中的地区
        try:
            db_regions = Region.objects.filter(is_active=True)
            db_region_codes = set(r.code for r in db_regions)
            config_codes = set(REGIONS.keys())

            missing = config_codes - db_region_codes
            extra = db_region_codes - config_codes

            self.log('数据库地区同步',
                    len(missing) == 0 and len(extra) == 0,
                    f'Missing: {missing}, Extra: {extra}')
        except Exception as e:
            self.log('数据库地区同步', False, str(e))

    def test_single_region_crawl(self):
        """测试单地区爬取"""
        print('\n' + '='*50)
        print('测试单地区爬取')
        print('='*50)

        test_regions = ['xian', 'baoji']

        for region_code in test_regions:
            try:
                start_time = time.time()
                result = crawl_region(region_code)
                elapsed = time.time() - start_time

                passed = 'total' in result and 'new' in result
                self.log(f'爬取 {region_code}', passed,
                        f'Total: {result.get("total", 0)}, New: {result.get("new", 0)}, Time: {elapsed:.2f}s')
            except Exception as e:
                self.log(f'爬取 {region_code}', False, str(e))

    def test_crawler_error_handling(self):
        """测试爬虫错误处理"""
        print('\n' + '='*50)
        print('测试爬虫错误处理')
        print('='*50)

        # 测试无效地区代码
        try:
            result = crawl_region('invalid_region_xxx')
            # 应该返回空结果或抛出异常
            passed = 'total' in result or 'error' in result
            self.log('无效地区代码处理', passed, f'Result: {result}')
        except Exception as e:
            self.log('无效地区代码处理', True, f'抛出异常: {type(e).__name__}')

        # 测试网络超时处理
        try:
            from apps.crawler.crawler import HEADERS
            import requests

            # 使用无效域名测试超时
            response = requests.get(
                'http://invalid-domain-that-does-not-exist.xyz',
                headers=HEADERS,
                timeout=3
            )
            self.log('网络超时处理', False, '应该抛出异常')
        except requests.exceptions.Timeout:
            self.log('网络超时处理', True, '正确处理超时')
        except requests.exceptions.RequestException:
            self.log('网络超时处理', True, '正确处理网络错误')
        except Exception as e:
            self.log('网络超时处理', False, f'未预期的异常: {e}')

    def test_scheduler(self):
        """测试调度器"""
        print('\n' + '='*50)
        print('测试调度器')
        print('='*50)

        # 测试获取调度器状态
        try:
            scheduler = get_scheduler()
            if scheduler is None:
                # 初始化调度器
                scheduler = init_scheduler()

            has_jobs = scheduler.get_jobs() is not None
            self.log('调度器初始化', scheduler is not None,
                    f'Jobs count: {len(scheduler.get_jobs()) if has_jobs else 0}')
        except Exception as e:
            self.log('调度器初始化', False, str(e))

        # 测试调度器状态
        try:
            scheduler = get_scheduler()
            is_running = scheduler.running if scheduler else False
            self.log('调度器运行状态', True, f'Running: {is_running}')
        except Exception as e:
            self.log('调度器运行状态', False, str(e))

    def test_database_operations(self):
        """测试数据库操作"""
        print('\n' + '='*50)
        print('测试数据库操作')
        print('='*50)

        # 测试新闻计数
        try:
            total_news = News.objects.filter(status='published').count()
            today_news = News.objects.filter(
                status='published',
                crawl_time__date=datetime.now().date()
            ).count()

            self.log('新闻数据统计', True,
                    f'Total: {total_news}, Today: {today_news}')
        except Exception as e:
            self.log('新闻数据统计', False, str(e))

        # 测试标签统计
        try:
            from apps.news.models import Tag
            total_tags = Tag.objects.filter(is_active=True).count()
            self.log('标签数据统计', True, f'Total: {total_tags}')
        except Exception as e:
            self.log('标签数据统计', False, str(e))

        # 测试新闻去重
        try:
            # 检查是否有重复的URL
            from django.db.models import Count

            duplicates = News.objects.values('url').annotate(
                count=Count('id')
            ).filter(count__gt=1)

            has_duplicates = len(list(duplicates)) > 0
            self.log('新闻URL去重', not has_duplicates,
                    f'Duplicates: {duplicates.count() if has_duplicates else 0}')
        except Exception as e:
            self.log('新闻URL去重', False, str(e))

    def test_performance(self):
        """测试性能"""
        print('\n' + '='*50)
        print('测试性能')
        print('='*50)

        # 测试标签匹配性能
        try:
            test_titles = [
                '西安市纪委监委通报违反中央八项规定精神典型问题',
                '宝鸡市查处形式主义官僚主义问题',
                '咸阳市一名干部因贪污受贿被查',
                '渭南市通报失职渎职典型案例',
                '延安市纪委监委查处滥用职权案件',
            ]

            start_time = time.time()
            for _ in range(100):
                for title in test_titles:
                    auto_tagging(title)
            elapsed = time.time() - start_time

            passed = elapsed < 5.0  # 500次标签匹配应在5秒内完成
            self.log('标签匹配性能', passed, f'500次匹配耗时: {elapsed:.3f}s')
        except Exception as e:
            self.log('标签匹配性能', False, str(e))

        # 测试数据库查询性能
        try:
            start_time = time.time()
            for _ in range(10):
                list(News.objects.filter(status='published')[:100])
            elapsed = time.time() - start_time

            passed = elapsed < 2.0
            self.log('数据库查询性能', passed, f'10次查询耗时: {elapsed:.3f}s')
        except Exception as e:
            self.log('数据库查询性能', False, str(e))

    def test_concurrent_crawling(self):
        """测试并发爬取（危险，谨慎使用）"""
        print('\n' + '='*50)
        print('测试并发爬取')
        print('='*50)

        print('\n⚠️  跳过并发爬取测试（可能导致目标网站封禁）')

    def run_all_tests(self):
        """运行所有测试"""
        print('\n' + '='*60)
        print('  智慧监督管理系统 - 爬虫测试套件')
        print('='*60)
        print(f'测试时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('='*60)

        self.test_auto_tagging()
        self.test_region_config()
        self.test_single_region_crawl()
        self.test_crawler_error_handling()
        self.test_scheduler()
        self.test_database_operations()
        self.test_performance()
        self.test_concurrent_crawling()

        # 打印总结
        print('\n' + '='*60)
        print('  测试总结')
        print('='*60)
        print(f'总测试数: {self.passed + self.failed}')
        print(f'通过: {self.passed}')
        print(f'失败: {self.failed}')
        print(f'通过率: {self.passed / (self.passed + self.failed) * 100:.1f}%')
        print('='*60)

        # 保存测试结果
        import json
        with open('test_crawler_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'test_time': datetime.now().isoformat(),
                'summary': {
                    'total': self.passed + self.failed,
                    'passed': self.passed,
                    'failed': self.failed,
                    'pass_rate': f'{self.passed / (self.passed + self.failed) * 100:.1f}%'
                },
                'results': self.results
            }, f, ensure_ascii=False, indent=2)

        print('\n测试结果已保存到 test_crawler_results.json')


if __name__ == '__main__':
    tester = CrawlerTester()
    tester.run_all_tests()
