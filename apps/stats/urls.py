# -*- coding: utf-8 -*-
from django.urls import path
from .views import (
    ViolationsStatsView, CasesStatsView, RegionsStatsView,
    TagsStatsView, DashboardStatsView, WeeklyStatsView, ArticlesStatsView,
    ReportGenerateView, SystemMonitorView
)

urlpatterns = [
    path('stats/violations/', ViolationsStatsView.as_view(), name='stats-violations'),
    path('stats/cases/', CasesStatsView.as_view(), name='stats-cases'),
    path('stats/regions/', RegionsStatsView.as_view(), name='stats-regions'),
    path('stats/tags/', TagsStatsView.as_view(), name='stats-tags'),
    path('stats/dashboard/', DashboardStatsView.as_view(), name='stats-dashboard'),
    path('stats/weekly/', WeeklyStatsView.as_view(), name='stats-weekly'),
    path('stats/articles/', ArticlesStatsView.as_view(), name='stats-articles'),
    path('stats/report/', ReportGenerateView.as_view(), name='stats-report'),
    path('stats/monitor/', SystemMonitorView.as_view(), name='stats-monitor'),
]
