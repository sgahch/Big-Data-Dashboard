from rest_framework import serializers
from .models import Case, CaseProgress, Evidence, Trial, Conclusion, AssistPartyTask, Regulation, Supervision, EducationMaterial, EducationActivity


class CaseSerializer(serializers.ModelSerializer):
    """案件序列化器"""
    leader_name = serializers.CharField(source='leader.username', read_only=True)
    case_no = serializers.CharField(read_only=True)
    # 前端兼容字段
    case_source = serializers.CharField(source='report_source', read_only=True)
    main_content = serializers.CharField(source='summary', read_only=True)
    handling_opinion = serializers.CharField(source='illegal_content', read_only=True)
    title = serializers.CharField(source='case_name', read_only=True)
    # case_type 用于前端案件类型
    case_type = serializers.CharField(source='case_category', read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'case_no', 'case_name', 'title', 'case_type', 'case_category', 'stage', 'status', 'case_level',
                  'suspect_name', 'suspect_unit', 'suspect_position', 'suspect_id_card',
                  'report_source', 'case_source', 'report_id', 'summary', 'main_content',
                  'illegal_content', 'handling_opinion',
                  'involved_amount', 'recovered_amount', 'leader', 'leader_name',
                  'filing_date', 'filing_approval', 'investigation_start_date',
                  'investigation_end_date', 'trial_start_date', 'trial_end_date',
                  'trial_opinion', 'conclusion_date', 'punishment_type',
                  'punishment_content', 'conclusion_report', 'created_at', 'updated_at']


class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    """案件创建/更新序列化器"""
    # 前端字段映射到后端字段
    title = serializers.CharField(source='case_name', required=False, allow_blank=True)
    case_type = serializers.CharField(source='case_category', required=False, allow_blank=True)
    case_source = serializers.CharField(source='report_source', required=False, allow_blank=True)
    main_content = serializers.CharField(source='summary', required=False, allow_blank=True)
    handling_opinion = serializers.CharField(source='illegal_content', required=False, allow_blank=True)

    class Meta:
        model = Case
        fields = ['id', 'case_name', 'title', 'case_type', 'case_category', 'stage', 'status', 'case_level',
                  'suspect_name', 'suspect_unit', 'suspect_position', 'suspect_id_card',
                  'report_source', 'case_source', 'report_id', 'summary', 'main_content',
                  'illegal_content', 'handling_opinion',
                  'involved_amount', 'recovered_amount', 'leader',
                  'filing_date', 'filing_approval', 'investigation_start_date',
                  'investigation_end_date', 'trial_start_date', 'trial_end_date',
                  'trial_opinion', 'conclusion_date', 'punishment_type',
                  'punishment_content', 'conclusion_report']


class CaseProgressSerializer(serializers.ModelSerializer):
    """案件进度序列化器"""
    class Meta:
        model = CaseProgress
        fields = ['id', 'case', 'progress_type', 'progress_date', 'progress_content', 'handler', 'created_at']


class EvidenceSerializer(serializers.ModelSerializer):
    """证据序列化器"""
    class Meta:
        model = Evidence
        fields = ['id', 'case', 'evidence_type', 'name', 'description', 'file',
                  'page_count', 'submitter', 'created_at']


class TrialSerializer(serializers.ModelSerializer):
    """案件审理序列化器"""
    case_name = serializers.CharField(source='case.case_name', read_only=True)
    case_no = serializers.CharField(source='case.case_no', read_only=True)
    suspect_name = serializers.CharField(source='case.suspect_name', read_only=True)
    days_left = serializers.SerializerMethodField()
    accept_no = serializers.CharField(read_only=True)  # 由后端自动生成

    class Meta:
        model = Trial
        fields = ['id', 'accept_no', 'case', 'case_name', 'case_no', 'suspect_name',
                  'department', 'accept_date', 'deadline', 'judge', 'assistants',
                  'status', 'trial_opinion', 'result', 'days_left', 'created_at', 'updated_at']

    def get_days_left(self, obj):
        return obj.days_left


class TrialCreateSerializer(serializers.ModelSerializer):
    """案件审理创建序列化器"""
    accept_date = serializers.DateField(required=False)

    class Meta:
        model = Trial
        fields = ['case', 'department', 'accept_date', 'deadline', 'judge', 'assistants', 'trial_opinion']

    def validate_accept_date(self, value):
        """确保日期格式正确"""
        if value is None:
            # 如果没有提供，使用今天
            return value
        return value

    def create(self, validated_data):
        """创建审理记录"""
        # 如果没有提供 accept_date，使用今天
        if not validated_data.get('accept_date'):
            from datetime import date
            validated_data['accept_date'] = date.today()
        return super().create(validated_data)


class ConclusionSerializer(serializers.ModelSerializer):
    """结案报告序列化器"""
    case_name = serializers.CharField(source='case.case_name', read_only=True)
    suspect_name = serializers.CharField(source='case.suspect_name', read_only=True)
    execution_text = serializers.SerializerMethodField()
    conclusion_no = serializers.CharField(read_only=True)  # 由后端自动生成

    class Meta:
        model = Conclusion
        fields = ['id', 'conclusion_no', 'case', 'case_name', 'suspect_name',
                  'conclusion_date', 'conclusion_type', 'decision', 'execution_status',
                  'execution_text', 'execute_date', 'summary', 'archived', 'archived_date',
                  'created_at', 'updated_at']

    def get_execution_text(self, obj):
        """获取执行状态文本"""
        return '已执行' if obj.execution_status == 'completed' else '执行中'


class ConclusionCreateSerializer(serializers.ModelSerializer):
    """结案报告创建序列化器"""
    class Meta:
        model = Conclusion
        fields = ['case', 'conclusion_date', 'conclusion_type', 'decision',
                  'execution_status', 'execute_date', 'summary']


class AssistPartyTaskSerializer(serializers.ModelSerializer):
    """协助党委任务序列化器"""
    task_no = serializers.CharField(read_only=True)
    status_text = serializers.SerializerMethodField()

    class Meta:
        model = AssistPartyTask
        fields = ['id', 'task_no', 'task_name', 'owner', 'deadline', 'status',
                  'status_text', 'progress', 'description', 'created_by', 'created_at', 'updated_at']

    def get_status_text(self, obj):
        """获取状态文本"""
        status_map = {0: '待开始', 1: '进行中', 2: '已完成', 3: '已逾期'}
        return status_map.get(obj.status, '未知')


class AssistPartyTaskCreateUpdateSerializer(serializers.ModelSerializer):
    """协助党委任务创建/更新序列化器"""
    class Meta:
        model = AssistPartyTask
        fields = ['id', 'task_name', 'owner', 'deadline', 'status', 'progress', 'description']


class RegulationSerializer(serializers.ModelSerializer):
    """法规序列化器"""
    category_name = serializers.CharField(source='get_category_display', read_only=True)
    level_name = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Regulation
        fields = ['id', 'title', 'category', 'category_name', 'document_no', 'issuing_authority',
                  'level', 'level_name', 'content', 'attachment', 'publish_date', 'effective_date',
                  'expiry_date', 'is_valid', 'view_count', 'created_at', 'updated_at']


class RegulationCreateUpdateSerializer(serializers.ModelSerializer):
    """法规创建/更新序列化器"""
    class Meta:
        model = Regulation
        fields = ['id', 'title', 'category', 'document_no', 'issuing_authority', 'level',
                  'content', 'attachment', 'publish_date', 'effective_date', 'expiry_date', 'is_valid']


class SupervisionSerializer(serializers.ModelSerializer):
    """监督检查序列化器"""
    type_name = serializers.CharField(source='get_supervision_type_display', read_only=True)
    status_name = serializers.CharField(source='get_status_display', read_only=True)
    leader_name = serializers.CharField(source='leader.username', read_only=True)
    member_names = serializers.SerializerMethodField()

    class Meta:
        model = Supervision
        fields = ['id', 'title', 'supervision_type', 'type_name', 'content', 'target_objects',
                  'status', 'status_name', 'start_date', 'end_date', 'progress',
                  'leader', 'leader_name', 'members', 'member_names', 'result',
                  'created_at', 'updated_at']

    def get_member_names(self, obj):
        return [user.username for user in obj.members.all()]


class SupervisionCreateUpdateSerializer(serializers.ModelSerializer):
    """监督检查创建/更新序列化器"""
    member_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)

    class Meta:
        model = Supervision
        fields = ['id', 'title', 'supervision_type', 'content', 'target_objects',
                  'status', 'start_date', 'end_date', 'progress', 'leader', 'member_ids', 'result']

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        from django.contrib.auth import get_user_model
        User = get_user_model()
        members = User.objects.filter(id__in=member_ids)
        supervision = Supervision.objects.create(**validated_data)
        supervision.members.set(members)
        return supervision

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if member_ids is not None:
            members = User.objects.filter(id__in=member_ids)
            instance.members.set(members)
        return super().update(instance, validated_data)


class EducationMaterialSerializer(serializers.ModelSerializer):
    """教育资料序列化器"""
    category_name = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = EducationMaterial
        fields = ['id', 'title', 'category', 'category_name', 'content', 'attachment',
                  'source', 'view_count', 'is_published', 'published_at', 'created_at', 'updated_at']


class EducationMaterialCreateUpdateSerializer(serializers.ModelSerializer):
    """教育资料创建/更新序列化器"""
    class Meta:
        model = EducationMaterial
        fields = ['id', 'title', 'category', 'content', 'attachment', 'source',
                  'is_published', 'published_at']


class EducationActivitySerializer(serializers.ModelSerializer):
    """教育活动序列化器"""
    status_name = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EducationActivity
        fields = ['id', 'title', 'content', 'activity_type', 'start_time', 'end_time',
                  'location', 'participants', 'status', 'status_name', 'created_at', 'updated_at']


class EducationActivityCreateUpdateSerializer(serializers.ModelSerializer):
    """教育活动创建/更新序列化器"""
    class Meta:
        model = EducationActivity
        fields = ['id', 'title', 'content', 'activity_type', 'start_time', 'end_time',
                  'location', 'participants', 'status']
