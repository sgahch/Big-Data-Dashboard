# -*- coding: utf-8 -*-
"""
定时任务
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def crawl_single_region(region_code: str):
    """
    爬取单个地区（供手动调用）
    """
    from apps.crawler.crawler import crawl_region as do_crawl
    from apps.news.models import CrawlTask, Region

    region = Region.objects.filter(code=region_code).first()

    # 创建任务记录
    task = CrawlTask.objects.create(
        task_type='single',
        region=region,
        region_code=region_code,
        status='running',
        started_at=datetime.now()
    )

    try:
        result = do_crawl(region_code)

        task.status = 'success' if result.get('new', 0) > 0 else 'empty'
        task.total_crawled = result.get('total', 0)
        task.new_count = result.get('new', 0)
        task.finished_at = datetime.now()
        task.save()

        return {
            'task_id': task.id,
            'result': result
        }
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.finished_at = datetime.now()
        task.save()
        raise


def crawl_all_regions():
    """
    爬取所有地区（供定时任务调用）
    """
    from apps.crawler.crawler import crawl_all_regions as do_crawl
    from apps.news.models import CrawlTask

    # 创建任务记录
    task = CrawlTask.objects.create(
        task_type='all',
        status='running',
        started_at=datetime.now()
    )

    logger.info(f"{'='*60}")
    logger.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 开始定时爬取")
    logger.info(f"{'='*60}")

    try:
        result = do_crawl()

        task.status = 'success'
        task.total_crawled = result.get('total_crawled', 0)
        task.new_count = result.get('total_new', 0)
        task.finished_at = datetime.now()
        task.save()

        logger.info(f"爬取完成: 总计爬取 {result['total_crawled']} 条, 新增 {result['total_new']} 条")
        return result
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        task.finished_at = datetime.now()
        task.save()
        logger.exception('定时爬取失败')
        raise


def init_regions():
    """初始化地区数据"""
    from apps.news.models import Region
    from apps.crawler.crawler import REGIONS

    for code, config in REGIONS.items():
        Region.objects.update_or_create(
            code=code,
            defaults={
                'name': config['name'],
                'domain': config['domain'],
                'path': config['path'],
                'is_active': True,
            }
        )
    logger.info('地区数据初始化完成')


def init_tags():
    """初始化标签数据"""
    from apps.news.models import TagCategory, Tag

    # 违规类型
    violation_cat, _ = TagCategory.objects.get_or_create(
        name='违规类型',
        defaults={'color': '#FF6B9D'}
    )

    violations = [
        ('违反八项规定', '公款吃喝,礼品礼金,违规发放,公车私用,公款旅游'),
        ('形式主义官僚主义', '形式主义,官僚主义,不作为,慢作为,乱作为,推诿扯皮'),
        ('贪污受贿', '贪污,受贿,挪用公款,侵占挪用'),
        ('滥用职权', '滥用职权,玩忽职守,徇私枉法'),
        ('失职渎职', '失职,渎职,监管不力,履职不力'),
        ('违规插手工程', '工程,招标,采购,土地,建设'),
        ('扶贫领域', '扶贫,脱贫,惠农,低保,困难群众'),
        ('教育医疗', '教育,学校,医疗,医保,医院,招生'),
        ('生态环保', '生态,环保,污染,环境,督察'),
    ]

    for name, keywords in violations:
        Tag.objects.update_or_create(
            name=name,
            category=violation_cat,
            defaults={
                'keywords': keywords,
                'is_auto': True,
                'is_active': True,
            }
        )

    # 干部级别
    level_cat, _ = TagCategory.objects.get_or_create(
        name='干部级别',
        defaults={'color': '#00D2FF'}
    )

    levels = [
        ('省管干部', '省管,副省级,正厅级,副厅级'),
        ('市管干部', '市管,正处级,副处级'),
        ('县管干部', '县管,正科级,副科级'),
        ('基层干部', '科员,办事员,村干部,社区干部'),
    ]

    for name, keywords in levels:
        Tag.objects.update_or_create(
            name=name,
            category=level_cat,
            defaults={
                'keywords': keywords,
                'is_auto': True,
                'is_active': True,
            }
        )

    # 案件状态
    status_cat, _ = TagCategory.objects.get_or_create(
        name='案件状态',
        defaults={'color': '#9933FF'}
    )

    statuses = [
        ('执纪审查', '接受纪律审查,接受监察调查,审查调查'),
        ('党纪处分', '开除党籍,严重警告,警告,留党察看'),
        ('政务处分', '开除公职,政务撤职,政务降级,政务警告'),
        ('双开', '开除党籍开除公职,双开'),
    ]

    for name, keywords in statuses:
        Tag.objects.update_or_create(
            name=name,
            category=status_cat,
            defaults={
                'keywords': keywords,
                'is_auto': True,
                'is_active': True,
            }
        )

    logger.info('标签数据初始化完成')
