from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    """消息模型"""
    TYPE_CHOICES = [
        ('task', '任务通知'),
        ('system', '系统通知'),
        ('remind', '提醒通知'),
    ]

    PRIORITY_CHOICES = [
        ('low', '一般'),
        ('medium', '重要'),
        ('high', '紧急'),
    ]

    title = models.CharField('消息标题', max_length=200)
    content = models.TextField('消息内容')
    msg_type = models.CharField('消息类型', max_length=20, choices=TYPE_CHOICES, default='system')
    priority = models.CharField('优先级', max_length=20, choices=PRIORITY_CHOICES, default='low')

    # 发送者信息
    sender = models.CharField('发送人', max_length=100, default='系统')
    sender_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages', verbose_name='发送用户')

    # 接收者信息
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收用户')
    is_read = models.BooleanField('是否已读', default=False)
    read_time = models.DateTimeField('阅读时间', null=True, blank=True)

    # 关联业务
    related_type = models.CharField('关联类型', max_length=50, blank=True)
    related_id = models.CharField('关联ID', max_length=50, blank=True)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} -> {self.receiver.username}'


class MessageTemplate(models.Model):
    """消息模板"""
    name = models.CharField('模板名称', max_length=100)
    msg_type = models.CharField('消息类型', max_length=20, choices=Message.TYPE_CHOICES)
    title_template = models.CharField('标题模板', max_length=200)
    content_template = models.TextField('内容模板')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '消息模板'
        verbose_name_plural = '消息模板'

    def __str__(self):
        return self.name
