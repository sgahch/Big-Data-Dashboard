# -*- coding: utf-8 -*-
"""
定时调度器 - 支持数据库配置
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)

scheduler = None


def init_scheduler():
    """初始化调度器（从数据库读取配置）"""
    global scheduler

    if scheduler is not None:
        return scheduler

    try:
        scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

        # 从数据库加载配置
        from .models import CrawlConfig

        enabled_configs = CrawlConfig.objects.filter(is_enabled=True)

        if enabled_configs.count() == 0:
            # 没有配置时，使用默认配置
            logger.info('未找到爬虫配置，使用默认配置')
            add_default_jobs(scheduler)
        else:
            # 加载数据库中的配置
            for config in enabled_configs:
                add_job_from_config(scheduler, config)

        scheduler.start()

        # 记录状态
        jobs_count = len(scheduler.get_jobs())
        next_run = scheduler.get_job('config_1').next_run_time if scheduler.get_job('config_1') else None
        logger.info(f"调度器启动成功，已加载 {jobs_count} 个任务")

        if next_run:
            logger.info(f"下次爬取时间: {next_run}")

        return scheduler

    except Exception as e:
        logger.exception('调度器启动失败')
        return None


def add_default_jobs(scheduler):
    """添加默认任务（当数据库没有配置时）"""
    # 每4小时爬取一次
    scheduler.add_job(
        crawl_job,
        trigger=IntervalTrigger(hours=4),
        id='crawl_all_regions',
        name='爬取所有地区新闻（默认）',
        replace_existing=True,
        max_instances=1
    )

    # 每天早上8点爬取
    scheduler.add_job(
        crawl_job,
        trigger=CronTrigger(hour=8, minute=0),
        id='crawl_daily',
        name='每天早上8点爬取（默认）',
        replace_existing=True,
        max_instances=1
    )

    logger.info('已添加默认爬虫任务')


def add_job_from_config(scheduler, config):
    """根据配置添加任务"""
    try:
        if config.trigger_type == 'interval':
            trigger = IntervalTrigger(hours=config.interval_hours)
            job_id = f'config_{config.id}'
        else:
            trigger = CronTrigger(hour=config.cron_hour, minute=config.cron_minute)
            job_id = f'config_{config.id}'

        scheduler.add_job(
            crawl_job,
            trigger=trigger,
            id=job_id,
            name=config.name,
            replace_existing=True,
            max_instances=config.max_instances,
            kwargs={'config_id': config.id}  # 传递配置ID
        )

        logger.info(f"已添加任务: {config.name}")

    except Exception as e:
        logger.error(f"添加任务失败: {config.name}, {e}")


def crawl_job(config_id=None):
    """爬取任务"""
    from .tasks import crawl_all_regions, crawl_single_region
    from .models import CrawlConfig, CrawlScheduleLog

    logger.info(f"\n{'='*60}")
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始定时爬取")
    logger.info(f"{'='*60}")

    start_time = timezone.now()
    log = None

    try:
        # 获取配置
        regions_to_crawl = 'all'
        if config_id:
            try:
                config = CrawlConfig.objects.get(id=config_id)
                if not config.crawl_all_regions:
                    regions_to_crawl = config.get_regions_list()
                log = CrawlScheduleLog.objects.create(
                    config=config,
                    status='running'
                )
            except CrawlConfig.DoesNotExist:
                pass

        # 执行爬取
        if regions_to_crawl == 'all':
            result = crawl_all_regions()
        else:
            # 按指定地区爬取
            total_result = {'total_crawled': 0, 'total_new': 0}
            for region in regions_to_crawl:
                r = crawl_single_region(region)
                total_result['total_crawled'] += r.get('result', {}).get('total', 0)
                total_result['total_new'] += r.get('result', {}).get('new', 0)
            result = total_result

        # 更新日志
        if log:
            log.status = 'success'
            log.total_crawled = result.get('total_crawled', 0)
            log.new_count = result.get('total_new', 0)
            log.duration = (timezone.now() - start_time).total_seconds()
            log.save()

        logger.info(f"爬取完成: 总计爬取 {result.get('total_crawled', 0)} 条, 新增 {result.get('total_new', 0)} 条")
        return result

    except Exception as e:
        logger.exception('定时爬取失败')
        if log:
            log.status = 'failed'
            log.error_message = str(e)
            log.duration = (timezone.now() - start_time).total_seconds()
            log.save()
        raise


def get_scheduler():
    """获取调度器实例"""
    global scheduler
    return scheduler


def stop_scheduler():
    """停止调度器"""
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None
        logger.info('调度器已停止')


def reload_scheduler():
    """重新加载调度器（从数据库读取最新配置）"""
    global scheduler

    logger.info('重新加载调度器配置...')

    # 停止现有调度器
    if scheduler:
        scheduler.shutdown()
        scheduler = None

    # 重新初始化
    return init_scheduler()
