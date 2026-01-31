# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class SupervisionItem(models.Model):
    """监督事项清单（按年月管理）"""
    YEAR_CHOICES = [(str(y), str(y)) for y in range(2020, 2031)]
    MONTH_CHOICES = [(str(m), f'{m}月') for m in range(1, 13)]

    name = models.CharField('事项名称', max_length=100)
    year = models.CharField('年份', max_length=4, choices=YEAR_CHOICES, default='2026')
    month = models.CharField('月份', max_length=2, choices=MONTH_CHOICES, default='1')
    category = models.ForeignKey('TagCategory', on_delete=models.CASCADE, verbose_name='监督分类')

    # 关键词配置
    core_keywords = models.TextField('核心关键词', blank=True, help_text='核心关键词，用逗号分隔')
    synonyms = models.TextField('近义词', blank=True, help_text='近义词，用逗号分隔')
    context_words = models.TextField('上下文行动词', blank=True, help_text='上下文行动词，用逗号分隔')

    # 描述
    description = models.TextField('事项描述', blank=True)
    standard = models.TextField('判定标准', blank=True)

    # 状态
    is_active = models.BooleanField('是否启用', default=True)
    sort = models.IntegerField('排序', default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'supervision_item'
        ordering = ['year', 'month', 'sort']
        verbose_name = '监督事项清单'
        verbose_name_plural = '监督事项清单管理'
        unique_together = ['name', 'year', 'month']

    def __str__(self):
        return f'{self.year}年{self.month}月 - {self.name}'

    def get_core_keywords_list(self):
        return [k.strip() for k in self.core_keywords.split(',') if k.strip()]

    def get_synonyms_list(self):
        return [k.strip() for k in self.synonyms.split(',') if k.strip()]

    def get_context_words_list(self):
        return [k.strip() for k in self.context_words.split(',') if k.strip()]


class Region(models.Model):
    """地区"""
    code = models.CharField('地区代码', max_length=20, unique=True)
    name = models.CharField('地区名称', max_length=50)
    domain = models.CharField('域名', max_length=100)
    path = models.CharField('路径', max_length=100, default='scdc.htm')
    is_active = models.BooleanField('是否启用', default=True)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'region'
        ordering = ['sort']
        verbose_name = '地区'
        verbose_name_plural = '地区管理'

    def __str__(self):
        return self.name


class TagCategory(models.Model):
    """标签分类"""
    name = models.CharField('分类名称', max_length=50)
    description = models.CharField('描述', max_length=200, blank=True)
    color = models.CharField('颜色', max_length=20, default='#00D2FF')
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'tag_category'
        ordering = ['sort']
        verbose_name = '标签分类'
        verbose_name_plural = '标签分类管理'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签"""
    name = models.CharField('标签名称', max_length=50)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, verbose_name='分类')
    keywords = models.TextField('关键词（逗号分隔）', blank=True, help_text='用于自动匹配的关键词')
    description = models.CharField('描述', max_length=200, blank=True)
    color = models.CharField('颜色', max_length=20, default='#00D2FF')
    is_auto = models.BooleanField('自动匹配', default=True)
    is_active = models.BooleanField('是否启用', default=True)
    sort = models.IntegerField('排序', default=0)

    class Meta:
        db_table = 'tag'
        ordering = ['category', 'sort']
        verbose_name = '标签'
        verbose_name_plural = '标签管理'

    def __str__(self):
        return f'{self.category.name}-{self.name}'

    def get_keywords_list(self):
        return [k.strip() for k in self.keywords.split(',') if k.strip()]


class News(models.Model):
    """新闻"""
    title = models.CharField('标题', max_length=500)
    summary = models.TextField('摘要', blank=True)
    content = models.TextField('内容', blank=True)
    date = models.DateField('发布日期', null=True, blank=True)
    url = models.URLField('原文链接', max_length=500, unique=True)
    source = models.CharField('来源', max_length=100, default='清风网')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='地区')
    region_name = models.CharField('地区名称', max_length=50, blank=True)
    menu = models.CharField('菜单分类', max_length=100, blank=True)
    submenu = models.CharField('子菜单', max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    tag_names = models.CharField('标签名称', max_length=500, blank=True)
    crawl_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    status = models.CharField('状态', max_length=20, default='published', choices=[
        ('draft', '草稿'),
        ('published', '已发布'),
        ('archived', '已归档'),
    ])
    view_count = models.IntegerField('浏览次数', default=0)

    # 手动修正分类相关字段
    manual_tags = models.ManyToManyField(Tag, verbose_name='手动修正标签', related_name='manual_news', blank=True)
    manual_tag_names = models.CharField('手动标签名称', max_length=500, blank=True)
    is_manual_corrected = models.BooleanField('已手动修正', default=False)
    correction_reason = models.TextField('修正原因', blank=True)
    corrected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='修正人', related_name='corrected_news')
    corrected_at = models.DateTimeField('修正时间', null=True, blank=True)

    class Meta:
        db_table = 'news'
        ordering = ['-date', '-crawl_time']
        verbose_name = '新闻'
        verbose_name_plural = '新闻管理'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['region']),
            models.Index(fields=['url']),
        ]

    def __str__(self):
        return self.title[:50]

    def get_tag_names_list(self):
        return [t.strip() for t in self.tag_names.split(',') if t.strip()]

    def save(self, *args, **kwargs):
        # 保存标签名称
        if self.pk:
            tags = self.tags.all()
            self.tag_names = ','.join([t.name for t in tags])
        super().save(*args, **kwargs)


class CrawlLog(models.Model):
    """爬取日志"""
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name='地区')
    region_name = models.CharField('地区名称', max_length=50, blank=True)
    total_crawled = models.IntegerField('爬取总数', default=0)
    new_count = models.IntegerField('新增数量', default=0)
    status = models.CharField('状态', max_length=20, choices=[
        ('success', '成功'),
        ('error', '失败'),
        ('empty', '无新数据'),
    ])
    error_message = models.TextField('错误信息', blank=True)
    crawl_time = models.DateTimeField('爬取时间', auto_now_add=True)
    duration = models.FloatField('耗时（秒）', default=0)

    class Meta:
        db_table = 'crawl_log'
        ordering = ['-crawl_time']
        verbose_name = '爬取日志'
        verbose_name_plural = '爬取日志管理'

    def __str__(self):
        return f'{self.region_name} - {self.crawl_time}'


class CrawlTask(models.Model):
    """爬虫任务"""
    TASK_TYPE_CHOICES = [
        ('all', '全量爬取'),
        ('single', '单地区爬取'),
        ('manual', '手动触发'),
    ]

    STATUS_CHOICES = [
        ('pending', '等待中'),
        ('running', '运行中'),
        ('success', '成功'),
        ('failed', '失败'),
        ('stopped', '已停止'),
    ]

    task_type = models.CharField('任务类型', max_length=20, choices=TASK_TYPE_CHOICES, default='manual')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='地区')
    region_code = models.CharField('地区代码', max_length=20, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_crawled = models.IntegerField('爬取总数', default=0)
    new_count = models.IntegerField('新增数量', default=0)
    error_message = models.TextField('错误信息', blank=True)
    started_at = models.DateTimeField('开始时间', null=True, blank=True)
    finished_at = models.DateTimeField('完成时间', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'crawl_task'
        ordering = ['-created_at']
        verbose_name = '爬虫任务'
        verbose_name_plural = '爬虫任务管理'

    def __str__(self):
        return f'{self.get_task_type_display()} - {self.get_status_display()} - {self.created_at}'


class AuditLog(models.Model):
    """审计日志"""
    ACTION_CHOICES = [
        ('create', '新增'),
        ('update', '修改'),
        ('delete', '删除'),
        ('crawl', '爬取'),
        ('export', '导出'),
        ('login', '登录'),
    ]

    action = models.CharField('操作类型', max_length=20, choices=ACTION_CHOICES)
    content_type = models.CharField('内容类型', max_length=50)
    object_id = models.IntegerField('对象ID', null=True, blank=True)
    object_repr = models.CharField('对象描述', max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='操作用户')
    user_ip = models.GenericIPAddressField('用户IP', null=True, blank=True)
    detail = models.TextField('详细信息', blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        db_table = 'audit_log'
        ordering = ['-created_at']
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志管理'

    def __str__(self):
        return f'{self.user} - {self.action} - {self.content_type} - {self.created_at}'
