# -*- coding: utf-8 -*-
"""
爬虫配置API
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

from .models import CrawlConfig, CrawlScheduleLog

logger = logging.getLogger(__name__)


class CrawlConfigViewSet(viewsets.ModelViewSet):
    """爬虫配置API"""
    queryset = CrawlConfig.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        # 只返回启用的配置
        is_enabled = self.request.query_params.get('enabled')
        if is_enabled is not None:
            qs = qs.filter(is_enabled=is_enabled.lower() == 'true')
        return qs

    def list(self, request, *args, **kwargs):
        configs = self.get_queryset()
        data = []
        for config in configs:
            data.append({
                'id': config.id,
                'name': config.name,
                'description': config.description,
                'trigger_type': config.trigger_type,
                'interval_hours': config.interval_hours,
                'cron_hour': config.cron_hour,
                'cron_minute': config.cron_minute,
                'is_enabled': config.is_enabled,
                'max_instances': config.max_instances,
                'crawl_all_regions': config.crawl_all_regions,
                'region_codes': config.region_codes,
                'schedule_str': config.get_schedule_str(),
                'created_at': config.created_at.isoformat() if config.created_at else None,
                'updated_at': config.updated_at.isoformat() if config.updated_at else None,
            })
        return Response({'code': 0, 'data': data})

    def create(self, request, **kwargs):
        """创建配置"""
        data = request.data

        try:
            config = CrawlConfig.objects.create(
                name=data.get('name'),
                description=data.get('description', ''),
                trigger_type=data.get('trigger_type', 'interval'),
                interval_hours=int(data.get('interval_hours', 4)),
                cron_hour=int(data.get('cron_hour', 8)),
                cron_minute=int(data.get('cron_minute', 0)),
                is_enabled=data.get('is_enabled', True),
                max_instances=int(data.get('max_instances', 1)),
                crawl_all_regions=data.get('crawl_all_regions', True),
                region_codes=data.get('region_codes', ''),
            )

            # 重新加载调度器
            from .scheduler import reload_scheduler
            reload_scheduler()

            return Response({
                'code': 0,
                'message': '配置创建成功',
                'data': {'id': config.id}
            })
        except Exception as e:
            logger.exception('创建爬虫配置失败')
            return Response({
                'code': -1,
                'message': f'创建失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """更新配置"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data

        try:
            if 'name' in data:
                instance.name = data['name']
            if 'description' in data:
                instance.description = data['description']
            if 'trigger_type' in data:
                instance.trigger_type = data['trigger_type']
            if 'interval_hours' in data:
                instance.interval_hours = int(data['interval_hours'])
            if 'cron_hour' in data:
                instance.cron_hour = int(data['cron_hour'])
            if 'cron_minute' in data:
                instance.cron_minute = int(data['cron_minute'])
            if 'is_enabled' in data:
                instance.is_enabled = data['is_enabled']
            if 'max_instances' in data:
                instance.max_instances = int(data['max_instances'])
            if 'crawl_all_regions' in data:
                instance.crawl_all_regions = data['crawl_all_regions']
            if 'region_codes' in data:
                instance.region_codes = data['region_codes']

            instance.save()

            # 重新加载调度器
            from .scheduler import reload_scheduler
            reload_scheduler()

            return Response({
                'code': 0,
                'message': '配置更新成功'
            })
        except Exception as e:
            logger.exception('更新爬虫配置失败')
            return Response({
                'code': -1,
                'message': f'更新失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """删除配置"""
        instance = self.get_object()
        try:
            instance.delete()

            # 重新加载调度器
            from .scheduler import reload_scheduler
            reload_scheduler()

            return Response({
                'code': 0,
                'message': '配置删除成功'
            })
        except Exception as e:
            logger.exception('删除爬虫配置失败')
            return Response({
                'code': -1,
                'message': f'删除失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """切换启用状态"""
        config = self.get_object()
        config.is_enabled = not config.is_enabled
        config.save()

        from .scheduler import reload_scheduler
        reload_scheduler()

        return Response({
            'code': 0,
            'message': f'已{"启用" if config.is_enabled else "禁用"}任务',
            'is_enabled': config.is_enabled
        })


class CrawlScheduleLogViewSet(viewsets.ReadOnlyModelViewSet):
    """调度日志API"""
    queryset = CrawlScheduleLog.objects.all()

    def list(self, request, *args, **kwargs):
        logs = self.get_queryset()

        # 按配置筛选
        config_id = request.query_params.get('config')
        if config_id:
            logs = logs.filter(config_id=config_id)

        # 按状态筛选
        log_status = request.query_params.get('status')
        if log_status:
            logs = logs.filter(status=log_status)

        # 日期范围
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            logs = logs.filter(trigger_time__date__gte=start_date)
        if end_date:
            logs = logs.filter(trigger_time__date__lte=end_date)

        data = []
        for log in logs[:100]:
            data.append({
                'id': log.id,
                'config_name': log.config.name if log.config else '未知',
                'trigger_time': log.trigger_time.isoformat() if log.trigger_time else None,
                'status': log.status,
                'total_crawled': log.total_crawled,
                'new_count': log.new_count,
                'duration': log.duration,
                'error_message': log.error_message,
            })

        return Response({'code': 0, 'data': data})


class SchedulerControlView(APIView):
    """调度器控制API"""

    def get(self, request):
        """获取调度器状态"""
        from .scheduler import get_scheduler

        scheduler = get_scheduler()
        if scheduler is None:
            return Response({
                'code': 0,
                'data': {
                    'initialized': False,
                    'running': False,
                    'jobs': []
                }
            })

        jobs = []
        for job in scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger),
            })

        return Response({
            'code': 0,
            'data': {
                'initialized': True,
                'running': scheduler.running,
                'jobs': jobs
            }
        })

    def post(self, request):
        """控制调度器"""
        action = request.data.get('action')

        from .scheduler import get_scheduler, stop_scheduler, reload_scheduler

        scheduler = get_scheduler()

        if action == 'reload':
            """重新加载所有配置"""
            reload_scheduler()
            return Response({
                'code': 0,
                'message': '调度器已重新加载'
            })

        elif action == 'stop':
            """停止调度器"""
            stop_scheduler()
            return Response({
                'code': 0,
                'message': '调度器已停止'
            })

        elif action == 'start':
            """启动调度器"""
            if scheduler and scheduler.running:
                return Response({
                    'code': -1,
                    'message': '调度器已在运行'
                }, status=status.HTTP_400_BAD_REQUEST)
            reload_scheduler()
            return Response({
                'code': 0,
                'message': '调度器已启动'
            })

        return Response({
            'code': -1,
            'message': '无效操作'
        }, status=status.HTTP_400_BAD_REQUEST)
