# -*- coding: utf-8 -*-
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import connection
from apps.news.models import News, Region, Tag, TagCategory

from .report import generate_report, get_report_data

logger = logging.getLogger(__name__)

# 缓存超时时间
CACHE_TIMEOUT = 300  # 5分钟


class ViolationsStatsView(APIView):
    """违规事项分布统计"""

    def get(self, request):
        cache_key = 'stats_violations'
        cached = cache.get(cache_key)
        if cached is not None:
            return Response({'code': 0, 'data': cached})

        news = News.objects.filter(status='published')
        stats = {}

        for n in news:
            tags = n.get_tag_names_list()
            for tag in tags:
                stats[tag] = stats.get(tag, 0) + 1

        result = [{'name': k, 'value': v} for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)]

        # 缓存结果
        cache.set(cache_key, result, CACHE_TIMEOUT)

        return Response({'code': 0, 'data': result})


class CasesStatsView(APIView):
    """案件查处统计"""

    def get(self, request):
        months = int(request.query_params.get('months', 12))
        cache_key = f'stats_cases_{months}'

        cached = cache.get(cache_key)
        if cached is not None:
            return Response({'code': 0, 'data': cached})

        # 使用Python处理日期分组，避免数据库时区问题
        news_list = News.objects.filter(status='published').values('crawl_time')
        month_counts = {}
        for item in news_list:
            if item['crawl_time']:
                # 将UTC时间转换为本地时间
                dt = item['crawl_time'].replace(tzinfo=None)  # 移除时区信息
                key = dt.strftime('%Y-%m')
                month_counts[key] = month_counts.get(key, 0) + 1

        # 按月份排序
        sorted_months = sorted(month_counts.items())

        months_list = [m[0] for m in sorted_months]
        values_list = [m[1] for m in sorted_months]

        result = {
            'months': months_list,
            'values': values_list
        }

        cache.set(cache_key, result, CACHE_TIMEOUT)

        return Response({
            'code': 0,
            'data': result
        })


class RegionsStatsView(APIView):
    """地区统计"""

    def get(self, request):
        cache_key = 'stats_regions'

        cached = cache.get(cache_key)
        if cached is not None:
            return Response({'code': 0, 'data': cached})

        stats = (News.objects
                 .filter(status='published')
                 .values('region__name', 'region__code')
                 .annotate(count=Count('id'))
                 .order_by('-count'))

        return Response({
            'code': 0,
            'data': list(stats)
        })


class TagsStatsView(APIView):
    """标签统计"""

    def get(self, request):
        category_id = request.query_params.get('category')

        news = News.objects.filter(status='published')
        stats = {}

        for n in news:
            tags = n.get_tag_names_list()
            for tag in tags:
                stats[tag] = stats.get(tag, 0) + 1

        result = [{'name': k, 'value': v} for k, v in sorted(stats.items(), key=lambda x: x[1], reverse=True)]
        return Response({'code': 0, 'data': result})


class DashboardStatsView(APIView):
    """仪表盘概览统计"""

    def get(self, request):
        from apps.news.models import CrawlLog, CrawlTask

        today = timezone.now().date()

        # 总新闻数
        total_news = News.objects.filter(status='published').count()

        # 今日新增
        today_news = News.objects.filter(crawl_time__date=today).count()

        # 昨日新增
        yesterday_news = News.objects.filter(
            crawl_time__date=today - timedelta(days=1)
        ).count()

        # 活跃地区数
        active_regions = News.objects.filter(
            crawl_time__date=today
        ).values('region').distinct().count()

        # 今日爬取日志
        today_logs = CrawlLog.objects.filter(crawl_time__date=today)
        total_crawled = today_logs.aggregate(total=Count('total_crawled'))['total'] or 0
        total_new = today_logs.aggregate(total=Count('new_count'))['total'] or 0

        # 标签统计（前10）
        tags_stats = {}
        news = News.objects.filter(status='published')
        for n in news:
            tags = n.get_tag_names_list()
            for tag in tags:
                tags_stats[tag] = tags_stats.get(tag, 0) + 1

        top_tags = sorted(tags_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        top_tags = [{'name': k, 'value': v} for k, v in top_tags]

        # 今日任务统计
        today_tasks = CrawlTask.objects.filter(created_at__date=today)
        tasks_running = today_tasks.filter(status='running').count()
        tasks_success = today_tasks.filter(status='success').count()
        tasks_failed = today_tasks.filter(status='failed').count()

        # 最近7天趋势
        week_ago = today - timedelta(days=7)
        week_stats = (News.objects
                      .filter(crawl_time__date__gte=week_ago)
                      .values('crawl_time__date')
                      .annotate(count=Count('id'))
                      .order_by('crawl_time__date'))

        week_data = []
        week_values = []
        for item in week_stats:
            week_data.append(item['crawl_time__date'].strftime('%m-%d'))
            week_values.append(item['count'])

        return Response({
            'code': 0,
            'data': {
                'total_news': total_news,
                'today_news': today_news,
                'yesterday_news': yesterday_news,
                'active_regions': active_regions,
                'today_crawled': total_crawled,
                'today_new': total_new,
                'top_tags': top_tags,
                'tasks': {
                    'running': tasks_running,
                    'success': tasks_success,
                    'failed': tasks_failed
                },
                'week_trend': {
                    'dates': week_data,
                    'values': week_values
                }
            }
        })


class WeeklyStatsView(APIView):
    """周统计"""

    def get(self, request):
        weeks = int(request.query_params.get('weeks', 4))

        # 使用Python处理日期分组，避免数据库时区问题
        news_list = News.objects.filter(status='published').values('crawl_time')
        week_counts = {}
        for item in news_list:
            if item['crawl_time']:
                dt = item['crawl_time'].replace(tzinfo=None)
                year, week_num = dt.isocalendar()[0], dt.isocalendar()[1]
                key = f"{year}年第{week_num}周"
                week_counts[key] = week_counts.get(key, 0) + 1

        # 按周排序
        sorted_weeks = sorted(week_counts.items())

        weeks_list = [w[0] for w in sorted_weeks]
        values_list = [w[1] for w in sorted_weeks]

        return Response({
            'code': 0,
            'data': {
                'weeks': weeks_list,
                'values': values_list
            }
        })


class ArticlesStatsView(APIView):
    """文章管理统计"""

    def get(self, request):
        # 按状态统计
        status_stats = News.objects.values('status').annotate(count=Count('id'))

        # 按来源统计
        source_stats = News.objects.values('source').annotate(count=Count('id')).order_by('-count')[:10]

        # 按月份统计 - 使用Python处理日期分组
        news_list = News.objects.filter(status='published').values('date')
        month_counts = {}
        for item in news_list:
            if item['date']:
                key = item['date'].strftime('%Y-%m')
                month_counts[key] = month_counts.get(key, 0) + 1

        # 按月份排序（降序）
        sorted_months = sorted(month_counts.items(), reverse=True)[:12]
        by_month = [{'month': m[0], 'count': m[1]} for m in sorted_months]

        # 按标签分类统计
        category_stats = []
        for cat in TagCategory.objects.all():
            count = News.objects.filter(tags__category=cat).distinct().count()
            category_stats.append({
                'name': cat.name,
                'count': count
            })

        return Response({
            'code': 0,
            'data': {
                'by_status': list(status_stats),
                'by_source': list(source_stats),
                'by_month': by_month,
                'by_category': category_stats
            }
        })


class ReportGenerateView(APIView):
    """报告生成API"""

    def get(self, request):
        """预览报告数据"""
        report_type = request.query_params.get('type', 'word')

        try:
            data = get_report_data()
            return Response({
                'code': 0,
                'data': data,
                'message': f'{report_type.upper()}报告数据准备完成'
            })
        except Exception as e:
            logger.exception('获取报告数据失败')
            return Response({
                'code': -1,
                'message': f'获取报告数据失败: {str(e)}'
            }, status=500)

    def post(self, request):
        """生成并下载报告"""
        report_type = request.data.get('type', 'word')

        try:
            # 获取报告数据
            data = get_report_data()

            # 生成报告
            output = generate_report(
                report_type=report_type,
                data=data,
                title='纪检监察数据分析报告',
                subtitle=f'生成时间: {timezone.now().strftime("%Y-%m-%d %H:%M")}'
            )

            # 设置响应头
            if report_type == 'word':
                filename = f'纪检监察报告_{timezone.now().strftime("%Y%m%d")}.docx'
                content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            else:
                filename = f'纪检监察报告_{timezone.now().strftime("%Y%m%d")}.xlsx'
                content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

            response = HttpResponse(
                output.getvalue(),
                content_type=content_type
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except Exception as e:
            logger.exception('生成报告失败')
            return Response({
                'code': -1,
                'message': f'生成报告失败: {str(e)}'
            }, status=500)


class SystemMonitorView(APIView):
    """系统监控API"""

    def get(self, request):
        """获取系统监控信息"""
        import psutil
        import os
        from apps.news.models import News, CrawlLog, CrawlTask
        from apps.crawler.models import CrawlConfig, CrawlScheduleLog

        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)

        # 内存使用率
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = round(memory.used / (1024 * 1024 * 1024), 2)
        memory_total = round(memory.total / (1024 * 1024 * 1024), 2)

        # 磁盘使用率
        disk = psutil.disk_usage('/')
        disk_percent = round(disk.percent, 1)
        disk_used = round(disk.used / (1024 * 1024 * 1024), 2)
        disk_total = round(disk.total / (1024 * 1024 * 1024), 2)

        # 数据库连接数
        from django.db import connections
        db_connections = len(connections.all())

        # 数据统计
        today = timezone.now().date()
        total_news = News.objects.filter(status='published').count()
        today_news = News.objects.filter(crawl_time__date=today).count()

        # 爬虫状态
        from apps.crawler.scheduler import get_scheduler
        scheduler = get_scheduler()
        scheduler_status = 'running' if scheduler and scheduler.running else 'stopped'
        scheduler_jobs = len(scheduler.get_jobs()) if scheduler else 0

        # 今日爬取统计
        today_logs = CrawlLog.objects.filter(crawl_time__date=today)
        crawl_stats = today_logs.aggregate(
            total=Count('total_crawled'),
            new=Count('new_count')
        )

        # API健康检查
        api_healthy = True
        api_latency = 0
        try:
            import time
            start = time.time()
            News.objects.all()[:1]
            api_latency = round((time.time() - start) * 1000, 2)
        except Exception:
            api_healthy = False

        return Response({
            'code': 0,
            'data': {
                'timestamp': timezone.now().isoformat(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'memory_used_gb': memory_used,
                    'memory_total_gb': memory_total,
                    'disk_percent': disk_percent,
                    'disk_used_gb': disk_used,
                    'disk_total_gb': disk_total,
                    'db_connections': db_connections,
                },
                'data': {
                    'total_news': total_news,
                    'today_news': today_news,
                    'total_regions': News.objects.values('region').distinct().count(),
                },
                'crawler': {
                    'status': scheduler_status,
                    'jobs_count': scheduler_jobs,
                    'today_crawled': crawl_stats['total'] or 0,
                    'today_new': crawl_stats['new'] or 0,
                },
                'api': {
                    'healthy': api_healthy,
                    'latency_ms': api_latency,
                }
            }
        })
