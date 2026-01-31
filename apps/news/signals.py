# -*- coding: utf-8 -*-
"""
Django Signals for Audit Logging
"""
import logging
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

logger = logging.getLogger(__name__)


def log_action(action, content_type, object_id=None, object_repr=None, user=None, detail='', user_ip=None):
    """Helper function to create audit log entries"""
    from .models import AuditLog

    try:
        AuditLog.objects.create(
            action=action,
            content_type=content_type,
            object_id=object_id,
            object_repr=object_repr[:200] if object_repr else '',
            user=user,
            user_ip=user_ip,
            detail=detail
        )
    except Exception as e:
        logger.warning(f'Failed to create audit log: {e}')


@receiver(post_save, sender='news.News')
def news_saved(sender, instance, created, **kwargs):
    """Log news create/update"""
    action = 'create' if created else 'update'
    content_type = 'news'

    # Get user from request if available (simplified approach)
    user = getattr(instance, '_current_user', None)

    log_action(
        action=action,
        content_type=content_type,
        object_id=instance.id,
        object_repr=instance.title[:50],
        user=user,
        detail=f'标题: {instance.title[:100]}'
    )


@receiver(post_save, sender='news.Tag')
def tag_saved(sender, instance, created, **kwargs):
    """Log tag create/update"""
    action = 'create' if created else 'update'
    content_type = 'tag'

    user = getattr(instance, '_current_user', None)

    log_action(
        action=action,
        content_type=content_type,
        object_id=instance.id,
        object_repr=f'{instance.category.name}-{instance.name}',
        user=user,
        detail=f'关键词: {instance.keywords[:100]}' if instance.keywords else ''
    )


@receiver(post_save, sender='news.Region')
def region_saved(sender, instance, created, **kwargs):
    """Log region create/update"""
    action = 'create' if created else 'update'
    content_type = 'region'

    user = getattr(instance, '_current_user', None)

    log_action(
        action=action,
        content_type=content_type,
        object_id=instance.id,
        object_repr=instance.name,
        user=user,
        detail=f'域名: {instance.domain}'
    )


@receiver(post_save, sender='news.CrawlTask')
def crawl_task_saved(sender, instance, created, **kwargs):
    """Log crawl task status changes"""
    content_type = 'crawl_task'

    user = getattr(instance, '_current_user', None)

    if created:
        log_action(
            action='create',
            content_type=content_type,
            object_id=instance.id,
            object_repr=f'{instance.get_task_type_display()} - {instance.get_status_display()}',
            user=user,
            detail=f'任务类型: {instance.get_task_type_display()}, 地区: {instance.region.name if instance.region else "全部"}'
        )
    else:
        # Log status changes
        if instance.status in ['success', 'failed', 'stopped']:
            log_action(
                action='crawl',
                content_type=content_type,
                object_id=instance.id,
                object_repr=f'{instance.get_task_type_display()} - {instance.get_status_display()}',
                user=user,
                detail=f'状态: {instance.get_status_display()}, 爬取: {instance.total_crawled}条, 新增: {instance.new_count}条'
            )


# User login logging
def log_user_login(user, request):
    """Log user login"""
    from .models import AuditLog

    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')

        AuditLog.objects.create(
            action='login',
            content_type='user',
            object_id=user.id,
            object_repr=user.username,
            user=user,
            user_ip=user_ip,
            detail=f'用户 {user.username} 登录成功'
        )
    except Exception as e:
        logger.warning(f'Failed to log user login: {e}')
