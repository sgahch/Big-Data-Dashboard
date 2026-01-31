# -*- coding: utf-8 -*-
"""
Django Admin Customization
"""
from django.contrib import admin
from django.contrib.auth.models import User, Group

# 移除默认的 User 和 Group（我们会自定义）
admin.site.unregister(User)
admin.site.unregister(Group)

# 自定义 Admin Site
admin.site.site_header = '智慧监督管理系统'
admin.site.site_title = '监督管理系统'
admin.site.index_title = '管理后台'

# 导入我们的模型进行注册
from apps.news.models import Region, TagCategory, Tag, News, CrawlLog, SupervisionItem


# 监督事项清单Admin
@admin.register(SupervisionItem)
class SupervisionItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'month', 'category', 'is_active', 'created_at']
    list_filter = ['year', 'month', 'category', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by']


# 注册新闻相关模型
admin.site.register(Region)
admin.site.register(TagCategory)
admin.site.register(Tag)
admin.site.register(News)
admin.site.register(CrawlLog)
