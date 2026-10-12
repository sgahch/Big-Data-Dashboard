from rest_framework import serializers
from .models import AssistParty, DisciplineEducation, Supervision, Clue, Regulation


class AssistPartySerializer(serializers.ModelSerializer):
    """协助党委序列化器"""
    class Meta:
        model = AssistParty
        fields = ['id', 'title', 'content', 'assist_type', 'party_organization',
                  'status', 'start_date', 'end_date', 'handler', 'created_at', 'updated_at']


class DisciplineEducationSerializer(serializers.ModelSerializer):
    """纪律教育序列化器"""
    class Meta:
        model = DisciplineEducation
        fields = ['id', 'title', 'edu_type', 'content', 'attachment', 'target_dept',
                  'is_published', 'publish_time', 'publisher', 'created_at', 'updated_at']


class SupervisionSerializer(serializers.ModelSerializer):
    """监督检查序列化器"""
    class Meta:
        model = Supervision
        fields = ['id', 'title', 'supervision_type', 'content', 'target_objects',
                  'status', 'start_date', 'end_date', 'leader', 'result',
                  'created_at', 'updated_at']


from rest_framework import serializers
from django.utils import timezone
from .models import Clue


class ClueSerializer(serializers.ModelSerializer):
    """线索处置序列化器"""
    # 添加 handler_name 字段用于前端显示
    handler_name = serializers.SerializerMethodField()
    # 添加 reviewer_name 字段
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = Clue
        fields = ['id', 'clue_no', 'source', 'title', 'content', 'status',
                  'discoverer', 'discover_time', 'reviewer', 'reviewer_name', 'review_time',
                  'review_opinion', 'handler', 'handler_name', 'handle_time', 'handle_result',
                  'created_at', 'updated_at']
        read_only_fields = ['clue_no', 'status', 'created_at', 'updated_at']

    def get_handler_name(self, obj):
        """获取承办人姓名"""
        if obj.handler:
            return obj.handler.get_full_name() or obj.handler.username
        return None

    def get_reviewer_name(self, obj):
        """获取审阅人姓名"""
        if obj.reviewer:
            return obj.reviewer.get_full_name() or obj.reviewer.username
        return None

    def create(self, validated_data):
        # 自动生成线索编号：XS + 年月日 + 4位序号
        date_str = timezone.now().strftime('%Y%m%d')
        last_clue = Clue.objects.filter(
            clue_no__startswith=f'XS{date_str}'
        ).order_by('-clue_no').first()

        if last_clue:
            last_seq = int(last_clue.clue_no[-4:])
            seq = str(last_seq + 1).zfill(4)
        else:
            seq = '0001'

        validated_data['clue_no'] = f'XS{date_str}{seq}'
        validated_data['status'] = 'pending'
        return super().create(validated_data)


class RegulationSerializer(serializers.ModelSerializer):
    """法规库序列化器"""
    class Meta:
        model = Regulation
        fields = ['id', 'title', 'category', 'document_no', 'issuing_authority',
                  'content', 'attachment', 'effective_date', 'expiry_date',
                  'is_valid', 'view_count', 'created_at', 'updated_at']
