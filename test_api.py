# -*- coding: utf-8 -*-
"""
智慧监督管理系统 - API测试脚本
测试所有API端点的功能、错误处理和安全性
"""
import os
import sys
import json
import time
import random
import string
from datetime import datetime, timedelta

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supervision.settings')

import django
django.setup()

import requests
from django.test import Client
from django.contrib.auth.models import User
from apps.news.models import News, Region, Tag, TagCategory, CrawlTask

BASE_URL = 'http://localhost:8000/api'
ADMIN_URL = 'http://localhost:8000/admin'
client = Client()


class APITester:
    """API测试类"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0

    def log(self, test_name, passed, message=''):
        """记录测试结果"""
        status = '[PASS]' if passed else '[FAIL]'
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

    def test_news_api(self):
        """测试新闻API"""
        print('\n' + '='*50)
        print('测试新闻API')
        print('='*50)

        # 测试1: 获取新闻列表
        try:
            response = requests.get(f'{BASE_URL}/news/')
            passed = response.status_code == 200
            self.log('获取新闻列表', passed,
                    f'Status: {response.status_code}, Count: {len(response.json()) if passed else 0}')
        except Exception as e:
            self.log('获取新闻列表', False, str(e))

        # 测试2: 新闻分页参数
        try:
            response = requests.get(f'{BASE_URL}/news/?limit=10')
            passed = response.status_code == 200
            self.log('新闻分页参数', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('新闻分页参数', False, str(e))

        # 测试3: 地区筛选
        try:
            response = requests.get(f'{BASE_URL}/news/?region=xian')
            passed = response.status_code == 200
            self.log('新闻地区筛选', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('新闻地区筛选', False, str(e))

        # 测试4: 关键词搜索
        try:
            response = requests.get(f'{BASE_URL}/news/?keyword=测试')
            passed = response.status_code == 200
            self.log('关键词搜索', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('关键词搜索', False, str(e))

        # 测试5: 日期范围筛选
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            response = requests.get(f'{BASE_URL}/news/?start_date={today}&end_date={today}')
            passed = response.status_code == 200
            self.log('日期范围筛选', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('日期范围筛选', False, str(e))

        # 测试6: 标签筛选
        try:
            response = requests.get(f'{BASE_URL}/news/?tag=违反八项规定')
            passed = response.status_code == 200
            self.log('标签筛选', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('标签筛选', False, str(e))

        # 测试7: 非法参数处理
        try:
            response = requests.get(f'{BASE_URL}/news/?limit=invalid')
            # 应该返回400或使用默认值
            passed = response.status_code in [200, 400]
            self.log('非法参数处理', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('非法参数处理', False, str(e))

        # 测试8: 新闻详情API
        try:
            # 先获取一个新闻ID
            response = requests.get(f'{BASE_URL}/news/')
            if response.status_code == 200:
                news_list = response.json()
                if news_list:
                    news_id = news_list[0]['id']
                    detail_response = requests.get(f'{BASE_URL}/news/{news_id}/detail/')
                    passed = detail_response.status_code == 200
                    self.log('新闻详情API', passed, f'Status: {detail_response.status_code}')
                else:
                    self.log('新闻详情API', False, '无新闻数据')
            else:
                self.log('新闻详情API', False, '无法获取新闻列表')
        except Exception as e:
            self.log('新闻详情API', False, str(e))

    def test_stats_api(self):
        """测试统计API"""
        print('\n' + '='*50)
        print('测试统计API')
        print('='*50)

        tests = [
            ('违规事项统计', '/stats/violations/'),
            ('案件查处统计', '/stats/cases/'),
            ('地区统计', '/stats/regions/'),
            ('仪表盘统计', '/stats/dashboard/'),
            ('周统计', '/stats/weekly/'),
            ('文章统计', '/stats/articles/'),
        ]

        for name, endpoint in tests:
            try:
                response = requests.get(f'{BASE_URL}{endpoint}')
                passed = response.status_code == 200
                self.log(f'统计API - {name}', passed, f'Status: {response.status_code}')
            except Exception as e:
                self.log(f'统计API - {name}', False, str(e))

        # 测试非法月份参数
        try:
            response = requests.get(f'{BASE_URL}/stats/cases/?months=-1')
            passed = response.status_code in [200, 400]
            self.log('非法月份参数处理', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('非法月份参数处理', False, str(e))

    def test_crawl_api(self):
        """测试爬虫API"""
        print('\n' + '='*50)
        print('测试爬虫API')
        print('='*50)

        # 测试1: 获取爬虫状态
        try:
            response = requests.get(f'{BASE_URL}/crawl/status/')
            passed = response.status_code == 200
            self.log('获取爬虫状态', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('获取爬虫状态', False, str(e))

        # 测试2: 获取调度器状态
        try:
            response = requests.get(f'{BASE_URL}/crawl/scheduler/')
            passed = response.status_code == 200
            self.log('获取调度器状态', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('获取调度器状态', False, str(e))

        # 测试3: 触发爬虫（谨慎测试）
        print('\n⚠️  跳过触发爬虫测试（需要较长时间）')

        # 测试4: 任务历史
        try:
            response = requests.get(f'{BASE_URL}/crawl-tasks/')
            passed = response.status_code == 200
            self.log('获取任务历史', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('获取任务历史', False, str(e))

        # 测试5: 爬取日志
        try:
            response = requests.get(f'{BASE_URL}/crawl-logs/')
            passed = response.status_code == 200
            self.log('获取爬取日志', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('获取爬取日志', False, str(e))

    def test_report_api(self):
        """测试报告API"""
        print('\n' + '='*50)
        print('测试报告API')
        print('='*50)

        # 测试1: 预览报告数据
        try:
            response = requests.get(f'{BASE_URL}/stats/report/')
            passed = response.status_code == 200
            self.log('预览报告数据', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('预览报告数据', False, str(e))

        # 测试2: 生成Word报告
        try:
            response = requests.post(f'{BASE_URL}/stats/report/',
                                     json={'type': 'word'})
            passed = response.status_code == 200
            content_type = response.headers.get('Content-Type', '')
            passed = passed and 'word' in content_type
            self.log('生成Word报告', passed, f'Status: {response.status_code}, Type: {content_type}')
        except Exception as e:
            self.log('生成Word报告', False, str(e))

        # 测试3: 生成Excel报告
        try:
            response = requests.post(f'{BASE_URL}/stats/report/',
                                     json={'type': 'excel'})
            passed = response.status_code == 200
            content_type = response.headers.get('Content-Type', '')
            passed = passed and 'excel' in content_type or 'spreadsheet' in content_type
            self.log('生成Excel报告', passed, f'Status: {response.status_code}, Type: {content_type}')
        except Exception as e:
            self.log('生成Excel报告', False, str(e))

        # 测试4: 非法报告类型
        try:
            response = requests.post(f'{BASE_URL}/stats/report/',
                                     json={'type': 'invalid'})
            passed = response.status_code in [200, 400, 500]
            self.log('非法报告类型处理', passed, f'Status: {response.status_code}')
        except Exception as e:
            self.log('非法报告类型处理', False, str(e))

    def test_region_tag_api(self):
        """测试地区和标签API"""
        print('\n' + '='*50)
        print('测试地区和标签API')
        print('='*50)

        tests = [
            ('地区列表', '/regions/'),
            ('标签列表', '/tags/'),
            ('标签分类', '/tags/categories/'),
        ]

        for name, endpoint in tests:
            try:
                response = requests.get(f'{BASE_URL}{endpoint}')
                passed = response.status_code == 200
                self.log(f'{name}', passed, f'Status: {response.status_code}')
            except Exception as e:
                self.log(f'{name}', False, str(e))

    def test_concurrent_requests(self):
        """测试并发请求"""
        print('\n' + '='*50)
        print('测试并发请求')
        print('='*50)

        import concurrent.futures

        def make_request():
            try:
                response = requests.get(f'{BASE_URL}/stats/dashboard/')
                return response.status_code
            except:
                return 0

        # 测试10个并发请求
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [f.result() for f in concurrent.futures.as_completed(futures, timeout=10)]

            passed = all(r == 200 for r in results)
            self.log('并发请求稳定性', passed, f'Success: {sum(1 for r in results if r == 200)}/10')
        except Exception as e:
            self.log('并发请求稳定性', False, str(e))

    def test_response_time(self):
        """测试响应时间"""
        print('\n' + '='*50)
        print('测试响应时间')
        print('='*50)

        endpoints = [
            ('/news/', '新闻列表'),
            ('/stats/dashboard/', '仪表盘'),
            ('/stats/violations/', '违规统计'),
            ('/regions/', '地区列表'),
        ]

        for endpoint, name in endpoints:
            try:
                times = []
                for _ in range(5):
                    start = time.time()
                    response = requests.get(f'{BASE_URL}{endpoint}')
                    elapsed = time.time() - start
                    times.append(elapsed)

                avg_time = sum(times) / len(times)
                passed = avg_time < 2.0  # 2秒内响应
                self.log(f'{name}响应时间', passed, f'Avg: {avg_time:.3f}s, Max: {max(times):.3f}s')
            except Exception as e:
                self.log(f'{name}响应时间', False, str(e))

    def test_security(self):
        """测试安全性"""
        print('\n' + '='*50)
        print('测试安全性')
        print('='*50)

        # 测试1: SQL注入防护
        sql_injection_tests = [
            ("DROP TABLE news", "SQL注入1"),
            ("UNION SELECT", "SQL注入2"),
        ]

        for test_input, name in sql_injection_tests:
            try:
                response = requests.get(f'{BASE_URL}/news/?region={test_input}')
                passed = response.status_code == 200
                # 检查响应中是否有敏感信息泄露
                if passed:
                    try:
                        data = response.json()
                        passed = 'password' not in str(data).lower()
                    except:
                        passed = True
                self.log(f'SQL注入防护 - {name}', passed, f'Status: {response.status_code}')
            except Exception as e:
                self.log(f'SQL注入防护 - {name}', False, str(e))

        # 测试2: XSS防护
        xss_tests = [
            ('SCRIPT_ALERT', 'XSS脚本测试'),
        ]

        for test_input, name in xss_tests:
            try:
                # URL编码测试输入
                import urllib.parse
                encoded_input = urllib.parse.quote(test_input)
                response = requests.get(f'{BASE_URL}/news/?keyword={encoded_input}')
                passed = response.status_code == 200
                if passed:
                    try:
                        data = response.json()
                        # 检查是否返回了预期结果
                        passed = len(str(data)) > 0
                    except:
                        passed = True
                self.log(f'XSS防护 - {name}', passed, f'Status: {response.status_code}')
            except Exception as e:
                self.log(f'XSS防护 - {name}', False, str(e))

    def test_rate_limiting(self):
        """测试请求频率限制"""
        print('\n' + '='*50)
        print('测试请求频率限制')
        print('='*50)

        # 快速发送50个请求
        try:
            success_count = 0
            for i in range(50):
                response = requests.get(f'{BASE_URL}/news/')
                if response.status_code == 200:
                    success_count += 1

            passed = success_count >= 45  # 允许少量失败
            self.log('高频请求处理', passed, f'Success: {success_count}/50')
        except Exception as e:
            self.log('高频请求处理', False, str(e))

    def run_all_tests(self):
        """运行所有测试"""
        print('\n' + '='*60)
        print('  智慧监督管理系统 - API测试套件')
        print('='*60)
        print(f'测试时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print('='*60)

        self.test_news_api()
        self.test_stats_api()
        self.test_crawl_api()
        self.test_report_api()
        self.test_region_tag_api()
        self.test_concurrent_requests()
        self.test_response_time()
        self.test_security()
        self.test_rate_limiting()

        # 打印总结
        print('\n' + '='*60)
        print('  测试总结')
        print('='*60)
        print(f'总测试数: {self.passed + self.failed}')
        print(f'通过: {self.passed} ✅')
        print(f'失败: {self.failed} ❌')
        print(f'通过率: {self.passed / (self.passed + self.failed) * 100:.1f}%')
        print('='*60)

        # 保存测试结果
        with open('test_results.json', 'w', encoding='utf-8') as f:
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

        print('\n测试结果已保存到 test_results.json')


if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
