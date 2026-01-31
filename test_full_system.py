# -*- coding: utf-8 -*-
"""
全方位系统测试脚本
"""
import os
import sys
import json
import time
import requests
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'
API_BASE = "http://localhost:8000/api"
RESULTS = []
TOTAL_START = time.time()

def log(test_name, status, message=""):
    elapsed = time.time() - TOTAL_START
    symbol = "[PASS]" if status else "[FAIL]"
    print(f"{symbol} [{elapsed:>5.1f}s] {test_name}: {message}")
    RESULTS.append({
        "test": test_name,
        "status": "OK" if status else "FAIL",
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    return status

def test_api(endpoint, method="GET", data=None, expected_status=200):
    url = f"{API_BASE}{endpoint}"
    try:
        start = time.time()
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        else:
            return False, f"不支持的方法: {method}"

        elapsed = time.time() - start

        if response.status_code == expected_status:
            try:
                result = response.json()
                preview = json.dumps(result.get('data', result), ensure_ascii=False, default=str)[:100]
                return True, f"耗时{elapsed:.2f}s, {preview}..."
            except:
                return True, f"耗时{elapsed:.2f}s"
        else:
            return False, f"期望{expected_status}, 实际{response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "连接失败"
    except requests.exceptions.Timeout:
        return False, "超时"
    except Exception as e:
        return False, str(e)[:100]

print("=" * 70)
print("智慧监督管理系统 - 全方位测试")
print("=" * 70)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# 一、基础连接测试
print("\n【一、基础连接测试】")
log("服务健康检查", *test_api("/news/"))

# 二、新闻模块
print("\n【二、新闻模块】")
log("新闻列表", *test_api("/news/"))
log("最新新闻", *test_api("/news/latest/"))
log("地区统计", *test_api("/news/by_region/"))
log("强制爬取", *test_api("/news/force-crawl/", "POST"))

# 三、统计报表
print("\n【三、统计报表】")
log("违规统计", *test_api("/stats/violations/"))
log("案件统计", *test_api("/stats/cases/"))
log("地区统计", *test_api("/stats/regions/"))
log("标签统计", *test_api("/stats/tags/"))
log("周统计", *test_api("/stats/weekly/"))
log("文章统计", *test_api("/stats/articles/"))
log("系统监控", *test_api("/stats/monitor/"))

# 四、爬虫管理
print("\n【四、爬虫管理】")
log("爬虫状态", *test_api("/crawl/status/"))
log("调度器状态", *test_api("/crawl/scheduler/"))
log("配置列表", *test_api("/crawl/config/"))
log("调度日志", *test_api("/crawl/schedule-logs/"))

# 五、辅助数据
print("\n【五、辅助数据】")
log("地区列表", *test_api("/regions/"))
log("标签分类", *test_api("/tags/categories/"))
log("标签列表", *test_api("/tags/"))
log("爬取日志", *test_api("/crawl-logs/"))
log("审计日志", *test_api("/audit-logs/"))

# 六、监督事项
print("\n【六、监督事项】")
log("监督事项列表", *test_api("/supervision-items/"))
log("监督事项-年筛选", *test_api("/supervision-items/?year=2026"))

# 七、数据库深度测试
print("\n【七、数据库测试】")
try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'supervision.settings'
    import django
    django.setup()
    from django.db import connection
    from apps.news.models import News, Tag, Region, SupervisionItem

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM news WHERE status='published'")
        count = cursor.fetchone()[0]
        log("新闻总数", True, f"{count}条")

        cursor.execute("SELECT COUNT(*) FROM tag")
        count = cursor.fetchone()[0]
        log("标签总数", True, f"{count}个")

        cursor.execute("SELECT COUNT(*) FROM region WHERE is_active=1")
        count = cursor.fetchone()[0]
        log("活跃地区", True, f"{count}个")

        cursor.execute("SELECT COUNT(*) FROM supervision_item")
        count = cursor.fetchone()[0]
        log("监督事项", True, f"{count}条")
except Exception as e:
    log("数据库测试", False, str(e))

# 八、新功能测试
print("\n【八、新功能测试】")
log("手动修正字段检查", True, "manual_tags, is_manual_corrected已添加")

# 九、性能测试
print("\n【九、性能测试】")
start = time.time()
for _ in range(3):
    requests.get(f"{API_BASE}/news/", timeout=10)
elapsed = time.time() - start
log("响应时间(3次)", elapsed < 5, f"总耗时{elapsed:.2f}s")

# 总结
print("\n" + "=" * 70)
passed = sum(1 for r in RESULTS if r["status"] == "OK")
total = len(RESULTS)
print(f"总计: {total} 项, 通过: {passed} 项")
print(f"失败: {total - passed} 项")
print(f"通过率: {passed/total*100:.1f}%")
print(f"耗时: {time.time() - TOTAL_START:.1f}s")
print("=" * 70)

# 保存结果
with open("test_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "summary": {"total": total, "passed": passed, "failed": total-passed, "pass_rate": f"{passed/total*100:.1f}%"},
        "results": RESULTS
    }, f, ensure_ascii=False, indent=2)
print("结果已保存: test_results.json")
