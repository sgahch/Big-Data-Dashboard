# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet, TagCategoryViewSet, TagViewSet,
    NewsViewSet, CrawlLogViewSet, CrawlTaskViewSet, AuditLogViewSet,
    StatsView, ForceCrawlView, SupervisionItemViewSet, NewsCorrectionView
)

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'tags/categories', TagCategoryViewSet, basename='tag-category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'crawl-logs', CrawlLogViewSet, basename='crawl-log')
router.register(r'crawl-tasks', CrawlTaskViewSet, basename='crawl-task')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'supervision-items', SupervisionItemViewSet, basename='supervision-item')

urlpatterns = [
    path('', include(router.urls)),
    # 保留stats相关的短路径 (兼容旧API)
    path('stats/', StatsView.as_view(), name='stats'),
    path('stats/all', StatsView.as_view(), name='stats-all'),
    path('news/force-crawl/', ForceCrawlView.as_view(), name='force-crawl'),
    path('news/<int:pk>/correct/', NewsCorrectionView.as_view(), name='news-correction'),
]
