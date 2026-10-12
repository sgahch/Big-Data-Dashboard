from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


class Case(models.Model):
    """案件模型 - 覆盖立案、调查、审理、结案全流程"""
    STAGE_CHOICES = [
        ('filing', '立案'),
        ('investigation', '调查'),
        ('trial', '审理'),
        ('conclusion', '结案'),
    ]

    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('suspended', '已暂停'),
    ]

    LEVEL_CHOICES = [
        ('minor', '轻微'),
        ('ordinary', '一般'),
        ('major', '严重'),
        ('serious', '特别严重'),
    ]

    # 案件类型 choices (对应前端的 case_type)
    CATEGORY_CHOICES = [
        ('discipline', '纪律审查'),
        ('supervision', '监督执纪'),
        ('case', '简易案件'),
    ]

    case_no = models.CharField('案件编号', max_length=50, unique=True)
    case_name = models.CharField('案件名称', max_length=200)
    case_category = models.CharField('案件类型', max_length=20, choices=CATEGORY_CHOICES, default='discipline')
    stage = models.CharField('案件阶段', max_length=20, choices=STAGE_CHOICES, default='filing')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    case_level = models.CharField('案件级别', max_length=20, choices=LEVEL_CHOICES, default='ordinary')

    # 涉案人员
    suspect_name = models.CharField('被调查人姓名', max_length=100)
    suspect_unit = models.CharField('被调查人单位', max_length=200, blank=True)
    suspect_position = models.CharField('被调查人职务', max_length=100, blank=True)
    suspect_id_card = models.CharField('身份证号', max_length=18, blank=True)

    # 案件信息
    report_source = models.CharField('线索来源', max_length=100, blank=True)
    report_id = models.CharField('来源举报ID', max_length=50, blank=True)
    summary = models.TextField('案件摘要', blank=True)
    illegal_content = models.TextField('违纪违法事实', blank=True)

    # 涉案金额
    involved_amount = models.DecimalField('涉案金额', max_digits=15, decimal_places=2, default=0)
    recovered_amount = models.DecimalField('追回金额', max_digits=15, decimal_places=2, default=0)

    # 人员信息
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_cases', verbose_name='主办人')
    investigators = models.ManyToManyField(User, related_name='investigated_cases', verbose_name='调查人员')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    # 立案信息
    filing_date = models.DateField('立案日期', null=True, blank=True)
    filing_approval = models.CharField('立案审批人', max_length=100, blank=True)

    # 调查信息
    investigation_start_date = models.DateField('调查开始日期', null=True, blank=True)
    investigation_end_date = models.DateField('调查结束日期', null=True, blank=True)

    # 审理信息
    trial_start_date = models.DateField('审理开始日期', null=True, blank=True)
    trial_end_date = models.DateField('审理结束日期', null=True, blank=True)
    trial_opinion = models.TextField('审理意见', blank=True)

    # 结案信息
    conclusion_date = models.DateField('结案日期', null=True, blank=True)
    punishment_type = models.CharField('处分类型', max_length=100, blank=True)
    punishment_content = models.TextField('处分内容', blank=True)
    conclusion_report = models.TextField('结案报告', blank=True)

    class Meta:
        verbose_name = '案件'
        verbose_name_plural = '案件'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.case_no} - {self.case_name}'

    def save(self, *args, **kwargs):
        if not self.case_no:
            import uuid
            from django.utils import timezone
            now = timezone.now()
            self.case_no = f'AJ{now.strftime("%Y%m%d")}{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)


class CaseProgress(models.Model):
    """案件进度记录"""
    CASE_TYPE_CHOICES = [
        ('filing', '立案'),
        ('investigation', '调查'),
        ('trial', '审理'),
        ('conclusion', '结案'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='progresses', verbose_name='案件')
    progress_type = models.CharField('进度类型', max_length=20, choices=CASE_TYPE_CHOICES)
    progress_date = models.DateField('进度日期')
    progress_content = models.TextField('进度内容')
    handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='处理人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '案件进度'
        verbose_name_plural = '案件进度'
        ordering = ['-progress_date']

    def __str__(self):
        return f'{self.case.case_no} - {self.progress_type}'


class Evidence(models.Model):
    """证据材料"""
    EVIDENCE_TYPE_CHOICES = [
        ('document', '书证'),
        ('material', '物证'),
        ('testimony', '证人证言'),
        ('statement', '当事人陈述'),
        ('appraisal', '鉴定意见'),
        ('audio_video', '视听资料'),
        ('electronic', '电子数据'),
        ('other', '其他'),
    ]

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidences', verbose_name='案件')
    evidence_type = models.CharField('证据类型', max_length=20, choices=EVIDENCE_TYPE_CHOICES, default='document')
    name = models.CharField('证据名称', max_length=200)
    description = models.TextField('证据描述', blank=True)
    file = models.FileField('证据文件', upload_to='evidence/', blank=True)
    page_count = models.IntegerField('页数', default=0)
    submitter = models.CharField('提交人', max_length=100, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '证据'
        verbose_name_plural = '证据'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.case.case_no} - {self.name}'


class Trial(models.Model):
    """案件审理记录"""
    STATUS_CHOICES = [
        ('pending', '待审理'),
        ('processing', '审理中'),
        ('completed', '已审结'),
    ]

    STATUS_REVERSE_CHOICES = [
        ('returned', '退回补证'),
        ('suspended', '暂停审理'),
    ]

    accept_no = models.CharField('受理编号', max_length=50, unique=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='trials', verbose_name='关联案件')
    department = models.CharField('移送部门', max_length=200, blank=True)
    accept_date = models.DateField('受理日期')
    deadline = models.IntegerField('审理期限(天)', default=30)
    judge = models.CharField('主办审理员', max_length=100)
    assistants = models.CharField('协办人员', max_length=500, blank=True)
    status = models.CharField('审理状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    trial_opinion = models.TextField('审理意见', blank=True)
    result = models.CharField('审理结果', max_length=200, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '案件审理'
        verbose_name_plural = '案件审理'
        ordering = ['-accept_date']

    def __str__(self):
        return f'{self.accept_no} - {self.case.case_name}'

    @property
    def days_left(self):
        """计算剩余天数"""
        from datetime import date
        if self.status == 'completed':
            return None
        end_date = self.accept_date + timedelta(days=self.deadline)
        remaining = (end_date - date.today()).days
        return remaining

    def save(self, *args, **kwargs):
        if not self.accept_no:
            import uuid
            from django.utils import timezone
            now = timezone.now()
            self.accept_no = f'SL{now.strftime("%Y%m%d")}{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)


class Conclusion(models.Model):
    """结案记录"""
    STATUS_CHOICES = [
        ('pending', '执行中'),
        ('completed', '已执行'),
    ]

    CONCLUSION_TYPE_CHOICES = [
        ('party_discipline', '党纪处分'),
        ('administrative', '政务处分'),
        ('judicial', '移送司法'),
        ('criticism', '批评教育'),
        ('concluded', '予以了结'),
    ]

    conclusion_no = models.CharField('结案编号', max_length=50, unique=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='conclusions', verbose_name='关联案件')
    conclusion_date = models.DateField('结案日期')
    conclusion_type = models.CharField('结案方式', max_length=50, choices=CONCLUSION_TYPE_CHOICES)
    decision = models.TextField('处分决定', blank=True)
    execution_status = models.CharField('执行状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    execute_date = models.DateField('执行日期', null=True, blank=True)
    summary = models.TextField('案件总结', blank=True)
    archived = models.BooleanField('是否归档', default=False)
    archived_date = models.DateField('归档日期', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '结案报告'
        verbose_name_plural = '结案报告'
        ordering = ['-conclusion_date']

    def __str__(self):
        return f'{self.conclusion_no} - {self.case.case_name}'

    def save(self, *args, **kwargs):
        if not self.conclusion_no:
            import uuid
            from django.utils import timezone
            now = timezone.now()
            self.conclusion_no = f'JA{now.strftime("%Y%m%d")}{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)


class AssistPartyTask(models.Model):
    """协助党委工作任务"""
    STATUS_CHOICES = [
        (0, '待开始'),
        (1, '进行中'),
        (2, '已完成'),
        (3, '已逾期'),
    ]

    task_no = models.CharField('任务编号', max_length=50, unique=True)
    task_name = models.CharField('任务名称', max_length=200)
    owner = models.CharField('负责人', max_length=100)
    deadline = models.DateField('截止日期', null=True, blank=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=0)
    progress = models.IntegerField('进度(%)', default=0)
    description = models.TextField('任务描述', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '协助党委任务'
        verbose_name_plural = '协助党委任务'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.task_no} - {self.task_name}'

    def save(self, *args, **kwargs):
        if not self.task_no:
            import uuid
            from django.utils import timezone
            now = timezone.now()
            self.task_no = f'RW{now.strftime("%Y%m%d")}{str(uuid.uuid4())[:8].upper()}'
        super().save(*args, **kwargs)


class Regulation(models.Model):
    """法规库"""
    CATEGORY_CHOICES = [
        ('law', '法律'),
        ('regulation', '法规'),
        ('rule', '规章'),
        ('policy', '规范性文件'),
        ('interpretation', '解释'),
    ]

    LEVEL_CHOICES = [
        ('national', '国家级'),
        ('provincial', '省级'),
        ('city', '市级'),
        ('district', '区县级'),
    ]

    title = models.CharField('法规标题', max_length=200)
    category = models.CharField('法规类型', max_length=20, choices=CATEGORY_CHOICES)
    document_no = models.CharField('法规文号', max_length=100, blank=True)
    issuing_authority = models.CharField('发布部门', max_length=200, blank=True)
    level = models.CharField('效力层级', max_length=20, choices=LEVEL_CHOICES, blank=True)
    content = models.TextField('法规内容', blank=True)
    attachment = models.FileField('附件', upload_to='regulations/', blank=True, null=True)
    publish_date = models.DateField('发布日期', null=True, blank=True)
    effective_date = models.DateField('施行日期', null=True, blank=True)
    expiry_date = models.DateField('失效日期', null=True, blank=True)
    is_valid = models.BooleanField('是否有效', default=True)
    view_count = models.IntegerField('浏览次数', default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '法规'
        verbose_name_plural = '法规库'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Supervision(models.Model):
    """监督检查"""
    TYPE_CHOICES = [
        ('routine', '例行检查'),
        ('special', '专项检查'),
        ('random', '随机抽查'),
    ]

    STATUS_CHOICES = [
        ('planned', '计划中'),
        ('active', '进行中'),
        ('completed', '已完成'),
        ('reported', '已报告'),
    ]

    title = models.CharField('检查标题', max_length=200)
    supervision_type = models.CharField('检查类型', max_length=20, choices=TYPE_CHOICES)
    content = models.TextField('检查内容', blank=True)
    target_objects = models.TextField('检查对象', blank=True)  # 多个对象用逗号分隔
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='planned')
    start_date = models.DateField('开始日期', null=True, blank=True)
    end_date = models.DateField('结束日期', null=True, blank=True)
    progress = models.IntegerField('进度(%)', default=0)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='负责人', related_name='supervision_leader')
    members = models.ManyToManyField(User, verbose_name='参与人员', related_name='supervision_members', blank=True)
    result = models.TextField('检查结果', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '监督检查'
        verbose_name_plural = '监督检查'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EducationMaterial(models.Model):
    """教育资料"""
    CATEGORY_CHOICES = [
        ('policy', '政策法规'),
        ('case', '典型案例'),
        ('notice', '通知公告'),
        ('study', '学习材料'),
    ]

    title = models.CharField('资料标题', max_length=200)
    category = models.CharField('资料类型', max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField('内容', blank=True)
    attachment = models.FileField('附件', upload_to='education/', blank=True, null=True)
    source = models.CharField('来源', max_length=200, blank=True)
    view_count = models.IntegerField('浏览次数', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '教育资料'
        verbose_name_plural = '教育资料'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EducationActivity(models.Model):
    """教育活动"""
    STATUS_CHOICES = [
        ('upcoming', '未开始'),
        ('ongoing', '进行中'),
        ('completed', '已结束'),
    ]

    title = models.CharField('活动标题', max_length=200)
    content = models.TextField('活动内容', blank=True)
    activity_type = models.CharField('活动类型', max_length=100, blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    location = models.CharField('活动地点', max_length=200, blank=True)
    participants = models.TextField('参与人员', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '教育活动'
        verbose_name_plural = '教育活动'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
