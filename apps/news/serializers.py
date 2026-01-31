# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Region, TagCategory, Tag, News, CrawlLog, CrawlTask, AuditLog, SupervisionItem


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'code', 'name', 'domain', 'is_active']


class TagCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = ['id', 'name', 'description', 'color']


class TagSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'category', 'category_name', 'keywords', 'description', 'color', 'is_auto']


class SupervisionItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    core_keywords_list = serializers.SerializerMethodField()
    synonyms_list = serializers.SerializerMethodField()
    context_words_list = serializers.SerializerMethodField()

    class Meta:
        model = SupervisionItem
        fields = [
            'id', 'name', 'year', 'month', 'category', 'category_name',
            'core_keywords', 'core_keywords_list', 'synonyms', 'synonyms_list',
            'context_words', 'context_words_list', 'description', 'standard',
            'is_active', 'sort', 'created_at', 'updated_at'
        ]

    def get_core_keywords_list(self, obj):
        return obj.get_core_keywords_list()

    def get_synonyms_list(self, obj):
        return obj.get_synonyms_list()

    def get_context_words_list(self, obj):
        return obj.get_context_words_list()


class NewsSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(read_only=True)
    tags_list = serializers.SerializerMethodField()
    manual_tags_list = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'summary', 'date', 'url', 'source',
            'region', 'region_name', 'menu', 'submenu',
            'tags', 'tags_list', 'crawl_time', 'status', 'view_count',
            'manual_tags', 'manual_tags_list', 'is_manual_corrected',
            'correction_reason', 'corrected_at'
        ]

    def get_tags_list(self, obj):
        return obj.get_tag_names_list()

    def get_manual_tags_list(self, obj):
        return [t.name for t in obj.manual_tags.all()]

    def to_internal_value(self, data):
        # 处理tags字段（支持标签ID列表或标签名列表）
        if 'tags' in data:
            if isinstance(data['tags'], list):
                # 如果是字符串形式的列表
                if isinstance(data['tags'][0], str):
                    tag_names = data['tags']
                    data = data.copy()
                    data['tags'] = []
                    for name in tag_names:
                        try:
                            tag = Tag.objects.get(name=name)
                            data['tags'].append(tag.id)
                        except Tag.DoesNotExist:
                            pass
        return super().to_internal_value(data)


class NewsListSerializer(serializers.ModelSerializer):
    """新闻列表简化序列化器"""
    region_name = serializers.CharField(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'date', 'region_name', 'tag_names', 'crawl_time']


class CrawlLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlLog
        fields = ['id', 'region', 'region_name', 'total_crawled', 'new_count', 'status', 'crawl_time', 'duration']


class CrawlTaskSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CrawlTask
        fields = [
            'id', 'task_type', 'task_type_display', 'region', 'region_name',
            'region_code', 'status', 'status_display', 'total_crawled',
            'new_count', 'error_message', 'started_at', 'finished_at',
            'created_by', 'created_at'
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'action_display', 'content_type', 'object_id',
            'object_repr', 'user', 'user_name', 'user_ip', 'detail', 'created_at'
        ]
