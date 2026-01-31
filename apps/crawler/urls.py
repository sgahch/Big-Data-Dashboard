# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CrawlTaskStatusView,
    CrawlTaskTriggerView,
    CrawlTaskStopView,
    CrawlSchedulerView,
)
from .config_views import CrawlConfigViewSet, CrawlScheduleLogViewSet, SchedulerControlView

# 创建路由器
router = DefaultRouter()
router.register(r'crawl/config', CrawlConfigViewSet, basename='crawl-config')
router.register(r'crawl/schedule-logs', CrawlScheduleLogViewSet, basename='crawl-schedule-logs')

urlpatterns = [
    path('crawl/status/', CrawlTaskStatusView.as_view(), name='crawl-status'),
    path('crawl/trigger/', CrawlTaskTriggerView.as_view(), name='crawl-trigger'),
    path('crawl/stop/', CrawlTaskStopView.as_view(), name='crawl-stop'),
    path('crawl/scheduler/', CrawlSchedulerView.as_view(), name='crawl-scheduler'),
    path('crawl/control/', SchedulerControlView.as_view(), name='crawl-control'),
    path('', include(router.urls)),
]
