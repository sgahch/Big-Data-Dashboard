# -*- coding: utf-8 -*-
from django.urls import path
from .views import (
    ViolationsStatsView, CasesStatsView, RegionsStatsView,
    TagsStatsView, DashboardStatsView, WeeklyStatsView, ArticlesStatsView,
    ReportGenerateView, SystemMonitorView
)

urlpatterns = [
    # 同时支持带斜杠和不带斜杠的URL
    path('stats/violations', ViolationsStatsView.as_view(), name='stats-violations'),
    path('stats/violations/', ViolationsStatsView.as_view(), name='stats-violations-slash'),
    path('stats/cases', CasesStatsView.as_view(), name='stats-cases'),
    path('stats/cases/', CasesStatsView.as_view(), name='stats-cases-slash'),
    path('stats/regions', RegionsStatsView.as_view(), name='stats-regions'),
    path('stats/regions/', RegionsStatsView.as_view(), name='stats-regions-slash'),
    path('stats/tags', TagsStatsView.as_view(), name='stats-tags'),
    path('stats/tags/', TagsStatsView.as_view(), name='stats-tags-slash'),
    path('stats/dashboard', DashboardStatsView.as_view(), name='stats-dashboard'),
    path('stats/dashboard/', DashboardStatsView.as_view(), name='stats-dashboard-slash'),
    path('stats/weekly', WeeklyStatsView.as_view(), name='stats-weekly'),
    path('stats/weekly/', WeeklyStatsView.as_view(), name='stats-weekly-slash'),
    path('stats/articles', ArticlesStatsView.as_view(), name='stats-articles'),
    path('stats/articles/', ArticlesStatsView.as_view(), name='stats-articles-slash'),
    path('stats/report', ReportGenerateView.as_view(), name='stats-report'),
    path('stats/report/', ReportGenerateView.as_view(), name='stats-report-slash'),
    path('stats/monitor', SystemMonitorView.as_view(), name='stats-monitor'),
    path('stats/monitor/', SystemMonitorView.as_view(), name='stats-monitor-slash'),
]
