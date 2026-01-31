# -*- coding: utf-8 -*-
"""
爬虫任务管理视图
"""
import logging
import threading
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# 任务状态存储（内存中，生产环境建议用Redis）
_task_status = {
    'running': False,
    'current_region': None,
    'start_time': None,
    'results': None,
}


class CrawlTaskStatusView(APIView):
    """爬虫任务状态查询"""

    def get(self, request):
        """获取当前爬虫任务状态"""
        return Response({
            'code': 0,
            'data': {
                'is_running': _task_status['running'],
                'current_region': _task_status.get('current_region'),
                'start_time': _task_status.get('start_time'),
                'results': _task_status.get('results'),
            }
        })


class CrawlTaskTriggerView(APIView):
    """手动触发爬虫任务"""

    def post(self, request):
        """触发爬虫任务"""
        global _task_status

        if _task_status['running']:
            return Response({
                'code': -1,
                'message': '已有爬虫任务正在运行，请稍后再试'
            }, status=status.HTTP_400_BAD_REQUEST)

        region_code = request.data.get('region')  # 可选，指定地区

        # 启动后台任务
        def run_crawl():
            global _task_status
            _task_status['running'] = True
            _task_status['start_time'] = datetime.now().isoformat()
            _task_status['current_region'] = None
            _task_status['results'] = None

            try:
                if region_code:
                    _task_status['current_region'] = region_code
                    result = crawl_single_region(region_code)
                else:
                    result = crawl_all_regions()

                _task_status['results'] = result
                logger.info(f"爬虫任务完成: {result}")
            except Exception as e:
                logger.exception('爬虫任务失败')
                _task_status['results'] = {'error': str(e)}
            finally:
                _task_status['running'] = False
                _task_status['current_region'] = None

        thread = threading.Thread(target=run_crawl)
        thread.daemon = True
        thread.start()

        return Response({
            'code': 0,
            'message': '爬虫任务已启动',
            'data': {
                'is_running': True,
                'start_time': _task_status['start_time']
            }
        })


class CrawlTaskStopView(APIView):
    """停止爬虫任务"""

    def post(self, request):
        """停止当前爬虫任务"""
        global _task_status

        if not _task_status['running']:
            return Response({
                'code': -1,
                'message': '没有正在运行的爬虫任务'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 注意：由于是线程执行，无法直接停止，这里只是标记
        _task_status['running'] = False
        _task_status['results'] = {'stopped': True, 'message': '任务已停止'}

        return Response({
            'code': 0,
            'message': '爬虫任务已停止'
        })


class CrawlSchedulerView(APIView):
    """调度器管理"""

    def get(self, request):
        """获取调度器状态"""
        from .scheduler import get_scheduler

        scheduler = get_scheduler()
        if scheduler is None:
            return Response({
                'code': 0,
                'data': {
                    'initialized': False,
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
        """调度器操作"""
        action = request.data.get('action')
        from .scheduler import get_scheduler, stop_scheduler, init_scheduler

        scheduler = get_scheduler()

        if action == 'stop':
            stop_scheduler()
            return Response({
                'code': 0,
                'message': '调度器已停止'
            })

        elif action == 'start':
            if scheduler and scheduler.running:
                return Response({
                    'code': -1,
                    'message': '调度器已在运行'
                }, status=status.HTTP_400_BAD_REQUEST)
            init_scheduler()
            return Response({
                'code': 0,
                'message': '调度器已启动'
            })

        elif action == 'pause':
            if scheduler:
                scheduler.pause()
                return Response({
                    'code': 0,
                    'message': '调度器已暂停'
                })

        elif action == 'resume':
            if scheduler:
                scheduler.resume()
                return Response({
                    'code': 0,
                    'message': '调度器已恢复'
                })

        return Response({
            'code': -1,
            'message': '无效操作'
        }, status=status.HTTP_400_BAD_REQUEST)
