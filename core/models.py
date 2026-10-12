from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AssistParty(models.Model):
    """协助党委工作"""
    STATUS_CHOICES = [
        ('pending', '待开展'),
        ('active', '进行中'),
        ('completed', '已完成'),
    ]

    title = models.CharField('工作标题', max_length=200)
    content = models.TextField('工作内容')
    assist_type = models.CharField('协助类型', max_length=100)
    party_organization = models.CharField('党委组织', max_length=200)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='处理人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '协助党委'
        verbose_name_plural = '协助党委'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class DisciplineEducation(models.Model):
    """纪律教育"""
    TYPE_CHOICES = [
        ('notice', '通报'),
        ('study', '学习材料'),
        ('video', '视频资料'),
        ('case', '案例警示'),
        ('exam', '知识测试'),
    ]

    title = models.CharField('标题', max_length=200)
    edu_type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES, default='study')
    content = models.TextField('内容')
    attachment = models.FileField('附件', upload_to='education/', blank=True)
    target_dept = models.CharField('目标部门', max_length=200, blank=True)
    is_published = models.BooleanField('是否发布', default=False)
    publish_time = models.DateTimeField('发布时间', null=True, blank=True)
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='发布人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '纪律教育'
        verbose_name_plural = '纪律教育'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Supervision(models.Model):
    """监督检查"""
    STATUS_CHOICES = [
        ('planned', '计划中'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('reported', '已报告'),
    ]

    TYPE_CHOICES = [
        ('routine', '常规检查'),
        ('special', '专项检查'),
        ('random', '随机抽查'),
    ]

    title = models.CharField('标题', max_length=200)
    supervision_type = models.CharField('检查类型', max_length=20, choices=TYPE_CHOICES, default='routine')
    content = models.TextField('检查内容')
    target_objects = models.CharField('检查对象', max_length=500, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='planned')
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_supervisions', verbose_name='负责人')
    members = models.ManyToManyField(User, related_name='supervision_tasks', verbose_name='参与人员')
    result = models.TextField('检查结果', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '监督检查'
        verbose_name_plural = '监督检查'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Clue(models.Model):
    """线索处置"""
    STATUS_CHOICES = [
        ('pending', '待处置'),
        ('reviewed', '已审阅'),
        ('assigned', '已分办'),
        ('investigating', '调查中'),
        ('closed', '已了结'),
        ('filed', '已暂存'),
    ]

    SOURCE_CHOICES = [
        ('report', '举报线索'),
        ('audit', '审计线索'),
        ('discover', '发现线索'),
        ('transfer', '移送线索'),
        ('other', '其他'),
    ]

    clue_no = models.CharField('线索编号', max_length=50, unique=True)
    source = models.CharField('线索来源', max_length=20, choices=SOURCE_CHOICES, default='report')
    title = models.CharField('线索标题', max_length=200)
    content = models.TextField('线索内容')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    discoverer = models.CharField('发现人', max_length=100, blank=True)
    discover_time = models.DateField('发现时间', null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_clues', verbose_name='审阅人')
    review_time = models.DateTimeField('审阅时间', null=True, blank=True)
    review_opinion = models.TextField('审阅意见', blank=True)
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_clues', verbose_name='承办人')
    handle_time = models.DateTimeField('处置时间', null=True, blank=True)
    handle_result = models.TextField('处置结果', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '线索处置'
        verbose_name_plural = '线索处置'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.clue_no} - {self.title}'


class Regulation(models.Model):
    """法规库"""
    CATEGORY_CHOICES = [
        ('law', '法律'),
        ('regulation', '法规'),
        ('rule', '规章'),
        ('policy', '政策'),
        ('interpretation', '解释'),
    ]

    title = models.CharField('标题', max_length=200)
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES, default='law')
    document_no = models.CharField('文号', max_length=100, blank=True)
    issuing_authority = models.CharField('发文机关', max_length=200, blank=True)
    content = models.TextField('内容')
    attachment = models.FileField('附件', upload_to='regulations/', blank=True)
    effective_date = models.DateField('生效日期', null=True, blank=True)
    expiry_date = models.DateField('失效日期', null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)
    view_count = models.IntegerField('浏览次数', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '法规库'
        verbose_name_plural = '法规库'
        ordering = ['-effective_date']

    def __str__(self):
        return self.title
