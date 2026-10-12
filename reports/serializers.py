from rest_framework import serializers
from .models import Report, ReportTransfer


class ReportSerializer(serializers.ModelSerializer):
    """举报序列化器"""
    acceptor_name = serializers.CharField(source='acceptor.username', read_only=True)
    handler_name = serializers.CharField(source='handler.username', read_only=True)
    report_no = serializers.CharField(read_only=True)  # 由后端自动生成

    class Meta:
        model = Report
        fields = ['id', 'report_no', 'report_type', 'report_level', 'reporter_name',
                  'reporter_phone', 'reporter_id_card', 'is_anonymous', 'accused_name',
                  'accused_unit', 'accused_position', 'title', 'content', 'attachment',
                  'status', 'acceptor', 'acceptor_name', 'accept_time', 'handler',
                  'handler_name', 'handle_time', 'result', 'created_at', 'updated_at']


class ReportTransferSerializer(serializers.ModelSerializer):
    """移送记录序列化器"""
    class Meta:
        model = ReportTransfer
        fields = ['id', 'report', 'from_unit', 'to_unit', 'transfer_reason',
                  'transfer_time', 'transfer_person', 'created_at']
