# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.crawler.scheduler import crawl_job


class Command(BaseCommand):
    help = '手动触发爬取任务'

    def add_arguments(self, parser):
        parser.add_argument(
            '--region',
            type=str,
            help='指定地区代码，如 xian,baoji',
        )

    def handle(self, *args, **options):
        self.stdout.write('开始手动爬取...')

        result = crawl_job()

        if result:
            total = result.get('total_crawled', 0)
            new = result.get('total_new', 0)
            self.stdout.write(
                self.style.SUCCESS(f'爬取完成: 总计 {total} 条, 新增 {new} 条')
            )
        else:
            self.stdout.write(self.style.WARNING('爬取失败或无数据'))
