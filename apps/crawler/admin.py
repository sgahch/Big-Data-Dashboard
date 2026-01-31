# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import CrawlConfig, CrawlScheduleLog


@admin.register(CrawlConfig)
class CrawlConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'trigger_type', 'get_schedule_str', 'is_enabled', 'crawl_all_regions', 'created_at', 'updated_at']
    list_filter = ['trigger_type', 'is_enabled', 'crawl_all_regions', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    fieldsets = [
        ('基本信息', {
            'fields': ['name', 'description', 'is_enabled']
        }),
        ('调度配置', {
            'fields': ['trigger_type', 'interval_hours', 'cron_hour', 'cron_minute', 'max_instances'],
            'description': '设置任务的执行频率'
        }),
        ('执行范围', {
            'fields': ['crawl_all_regions', 'region_codes'],
            'description': '设置需要爬取的地区'
        }),
        ('系统信息', {
            'fields': ['created_by', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

    def get_schedule_str(self, obj):
        return obj.get_schedule_str()
    get_schedule_str.short_description = '执行计划'

    def save_model(self, request, obj, form, change):
        if not change:  # 新创建
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        # 修改后自动重载调度器
        from .scheduler import reload_scheduler
        reload_scheduler()


@admin.register(CrawlScheduleLog)
class CrawlScheduleLogAdmin(admin.ModelAdmin):
    list_display = ['config', 'trigger_time', 'status', 'total_crawled', 'new_count', 'duration']
    list_filter = ['status', 'trigger_time']
    search_fields = ['config__name']
    date_hierarchy = 'trigger_time'
    readonly_fields = ['trigger_time', 'status', 'total_crawled', 'new_count', 'error_message', 'duration']
    ordering = ['-trigger_time']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
