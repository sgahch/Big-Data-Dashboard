from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Report(models.Model):
    """信访举报模型"""
    STATUS_CHOICES = [
        ('pending', '待受理'),
        ('accepted', '已受理'),
        ('investigating', '调查中'),
        ('closed', '已办结'),
        ('rejected', '不予受理'),
    ]

    TYPE_CHOICES = [
        ('letter', '来信'),
        ('visit', '来访'),
        ('call', '来电'),
        ('network', '网络举报'),
        ('other', '其他'),
    ]

    LEVEL_CHOICES = [
        ('normal', '一般'),
        ('important', '重要'),
        ('urgent', '紧急'),
    ]

    report_no = models.CharField('举报编号', max_length=50, unique=True)
    report_type = models.CharField('举报方式', max_length=20, choices=TYPE_CHOICES, default='letter')
    report_level = models.CharField('举报级别', max_length=20, choices=LEVEL_CHOICES, default='normal')

    # 举报人信息
    reporter_name = models.CharField('举报人姓名', max_length=100, blank=True)
    reporter_phone = models.CharField('举报人电话', max_length=20, blank=True)
    reporter_id_card = models.CharField('举报人身份证号', max_length=18, blank=True)
    is_anonymous = models.BooleanField('是否匿名', default=False)

    # 被举报人信息
    accused_name = models.CharField('被举报人姓名', max_length=100)
    accused_unit = models.CharField('被举报人单位', max_length=200, blank=True)
    accused_position = models.CharField('被举报人职务', max_length=100, blank=True)

    # 举报内容
    title = models.CharField('举报标题', max_length=200)
    content = models.TextField('举报内容')
    attachment = models.FileField('附件', upload_to='reports/', blank=True)

    # 处理信息
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    acceptor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_reports', verbose_name='受理人')
    accept_time = models.DateTimeField('受理时间', null=True, blank=True)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_reports', verbose_name='承办人')
    handle_time = models.DateTimeField('办理时间', null=True, blank=True)
    result = models.TextField('处理结果', blank=True)

    # 时间信息
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '信访举报'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.report_no} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.report_no:
            import uuid
            from django.utils import timezone
            # 使用当前时间而不是 created_at，因为 created_at 还没设置
            now = timezone.now()
            self.report_no = f'BX{now.strftime("%Y%m%d")}{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)


class ReportTransfer(models.Model):
    """举报件移送记录"""
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='transfers', verbose_name='举报件')
    from_unit = models.CharField('移送单位', max_length=100)
    to_unit = models.CharField('接收单位', max_length=100)
    transfer_reason = models.TextField('移送原因')
    transfer_time = models.DateTimeField('移送时间', auto_now_add=True)
    transfer_person = models.CharField('移送人', max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '移送记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.report.report_no} - {self.from_unit} -> {self.to_unit}'
