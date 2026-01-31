# -*- coding: utf-8 -*-
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.news'
    verbose_name = '新闻管理'

    def ready(self):
        # Import signals to register them
        from . import signals  # noqa: F401
