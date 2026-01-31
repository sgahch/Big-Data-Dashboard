from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crawler'
    verbose_name = '爬虫管理'

    def ready(self):
        # 导入调度器
        from apps.crawler.scheduler import init_scheduler
        init_scheduler()
