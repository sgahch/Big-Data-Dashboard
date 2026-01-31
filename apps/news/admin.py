# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html
from .models import Region, TagCategory, Tag, News, CrawlLog, CrawlTask, AuditLog
from import_export.admin import ImportExportModelAdmin


@admin.register(Region)
class RegionAdmin(ImportExportModelAdmin):
    list_display = ['code', 'name', 'domain', 'is_active', 'sort', 'news_count']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['sort']

    def news_count(self, obj):
        return obj.news_set.count()
    news_count.short_description = '新闻数量'


@admin.register(TagCategory)
class TagCategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'description', 'color', 'sort', 'tag_count']
    ordering = ['sort']

    def tag_count(self, obj):
        return obj.tag_set.count()
    tag_count.short_description = '标签数量'


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = ['name', 'category', 'keywords_preview', 'is_auto', 'is_active', 'sort', 'news_count']
    list_filter = ['category', 'is_auto', 'is_active']
    search_fields = ['name']
    ordering = ['category', 'sort']

    def keywords_preview(self, obj):
        return obj.keywords[:50] + '...' if len(obj.keywords) > 50 else obj.keywords
    keywords_preview.short_description = '关键词'

    def news_count(self, obj):
        return obj.news_set.count()
    news_count.short_description = '新闻数量'


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin):
    list_display = ['title_short', 'region_link', 'date', 'tag_names_display', 'status', 'crawl_time', 'view_count']
    list_filter = ['region', 'status', 'crawl_time', 'tags__category']
    search_fields = ['title', 'region_name', 'tag_names', 'summary']
    date_hierarchy = 'date'
    ordering = ['-date', '-crawl_time']
    filter_horizontal = ['tags']
    readonly_fields = ['crawl_time', 'tag_names', 'view_count']
    raw_id_fields = ['region']
    show_full_result_count = False

    def title_short(self, obj):
        return obj.title[:60] + '...' if len(obj.title) > 60 else obj.title
    title_short.short_description = '标题'

    def region_link(self, obj):
        if obj.region:
            return format_html('<a href="?region={}">{}</a>', obj.region.id, obj.region.name)
        return obj.region_name
    region_link.short_description = '地区'

    def tag_names_display(self, obj):
        tags = obj.get_tag_names_list()
        return ', '.join(tags[:5]) + ('...' if len(tags) > 5 else '')
    tag_names_display.short_description = '标签'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'region')

    # 手动标签修正操作
    actions = ['recalculate_tags', 'reindex_tags']

    def recalculate_tags(self, request, queryset):
        """重新计算标签"""
        count = 0
        for news in queryset:
            old_tags = set(news.get_tag_names_list())
            # 重新匹配标签
            from apps.crawler.crawler import auto_tagging
            new_tag_names = auto_tagging(news.title)
            tags = Tag.objects.filter(name__in=new_tag_names)
            news.tags.set(tags)
            news.tag_names = ','.join(new_tag_names)
            news.save()
            count += 1
        self.message_user(request, f'已重新计算 {count} 条新闻的标签')
    recalculate_tags.short_description = '重新计算标签'

    def reindex_tags(self, request, queryset):
        """更新标签索引"""
        count = 0
        for news in queryset:
            tags = news.tags.all()
            news.tag_names = ','.join([t.name for t in tags])
            news.save()
            count += 1
        self.message_user(request, f'已更新 {count} 条新闻的标签索引')
    reindex_tags.short_description = '更新标签索引'


@admin.register(CrawlLog)
class CrawlLogAdmin(ImportExportModelAdmin):
    list_display = ['region', 'region_name', 'total_crawled', 'new_count', 'status', 'crawl_time', 'duration']
    list_filter = ['status', 'crawl_time']
    search_fields = ['region_name']
    date_hierarchy = 'crawl_time'
    ordering = ['-crawl_time']
    readonly_fields = ['crawl_time']
    raw_id_fields = ['region']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CrawlTask)
class CrawlTaskAdmin(ImportExportModelAdmin):
    list_display = ['task_type', 'region', 'status', 'total_crawled', 'new_count', 'started_at', 'finished_at', 'created_by']
    list_filter = ['task_type', 'status', 'created_at']
    search_fields = ['region__name']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'started_at', 'finished_at']
    raw_id_fields = ['region', 'created_by']

    actions = ['retry_failed_tasks']

    def retry_failed_tasks(self, request, queryset):
        """重新执行失败的任务"""
        for task in queryset.filter(status='failed'):
            task.status = 'pending'
            task.save()
        self.message_user(request, f'已标记 {queryset.filter(status="failed").count()} 个失败任务等待重试')
    retry_failed_tasks.short_description = '重试失败任务'


@admin.register(AuditLog)
class AuditLogAdmin(ImportExportModelAdmin):
    list_display = ['action', 'content_type', 'object_repr', 'user', 'user_ip', 'created_at']
    list_filter = ['action', 'content_type', 'created_at']
    search_fields = ['object_repr', 'user__username']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    raw_id_fields = ['user']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
