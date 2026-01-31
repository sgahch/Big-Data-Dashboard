# -*- coding: utf-8 -*-
"""
爬虫配置模型
"""
from django.db import models
from django.contrib.auth.models import User


class CrawlConfig(models.Model):
    """爬虫任务配置"""
    TRIGGER_TYPE_CHOICES = [
        ('interval', '间隔执行'),
        ('cron', '定时执行'),
    ]

    ENABLE_CHOICES = [
        (True, '启用'),
        (False, '禁用'),
    ]

    name = models.CharField('任务名称', max_length=100)
    description = models.TextField('任务描述', blank=True)

    # 任务配置
    trigger_type = models.CharField('触发类型', max_length=20, choices=TRIGGER_TYPE_CHOICES, default='interval')
    interval_hours = models.IntegerField('间隔小时数', default=4, help_text='间隔执行时有效')
    cron_hour = models.IntegerField('小时', default=8, help_text='定时执行时有效（0-23）')
    cron_minute = models.IntegerField('分钟', default=0, help_text='定时执行时有效（0-59）')

    # 启用控制
    is_enabled = models.BooleanField('是否启用', default=True)
    max_instances = models.IntegerField('最大并发数', default=1, help_text='同时运行的最大任务数')

    # 执行范围
    crawl_all_regions = models.BooleanField('爬取所有地区', default=True)
    region_codes = models.TextField('指定地区', blank=True, help_text='爬取所有地区时忽略此选项，多个地区用逗号分隔，如：xian,baoji')

    # 创建信息
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'crawl_config'
        ordering = ['-created_at']
        verbose_name = '爬虫任务配置'
        verbose_name_plural = '爬虫任务配置管理'

    def __str__(self):
        return f'{self.name} ({self.get_trigger_type_display()})'

    def get_schedule_str(self):
        """获取调度描述"""
        if self.trigger_type == 'interval':
            return f'每 {self.interval_hours} 小时执行一次'
        else:
            return f'每天 {self.cron_hour:02d}:{self.cron_minute:02d} 执行'

    def get_regions_list(self):
        """获取地区列表"""
        if self.crawl_all_regions:
            return ['all']
        return [r.strip() for r in self.region_codes.split(',') if r.strip()]


class CrawlScheduleLog(models.Model):
    """调度执行日志"""
    config = models.ForeignKey(CrawlConfig, on_delete=models.SET_NULL, null=True, verbose_name='任务配置')
    trigger_time = models.DateTimeField('触发时间', auto_now_add=True)
    status = models.CharField('状态', max_length=20, choices=[
        ('running', '运行中'),
        ('success', '成功'),
        ('failed', '失败'),
    ], default='running')
    total_crawled = models.IntegerField('爬取总数', default=0)
    new_count = models.IntegerField('新增数量', default=0)
    error_message = models.TextField('错误信息', blank=True)
    duration = models.FloatField('耗时（秒）', default=0)

    class Meta:
        db_table = 'crawl_schedule_log'
        ordering = ['-trigger_time']
        verbose_name = '调度执行日志'
        verbose_name_plural = '调度执行日志管理'

    def __str__(self):
        return f'{self.config.name if self.config else "未知"} - {self.trigger_time}'
