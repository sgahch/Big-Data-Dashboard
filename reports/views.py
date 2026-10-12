from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Report, ReportTransfer
from .serializers import ReportSerializer, ReportTransferSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """举报视图集"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Report.objects.all()
        status_param = self.request.query_params.get('status')
        report_type = self.request.query_params.get('report_type')
        report_level = self.request.query_params.get('report_level')
        if status_param:
            queryset = queryset.filter(status=status_param)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        if report_level:
            queryset = queryset.filter(report_level=report_level)
        return queryset

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """受理举报"""
        report = self.get_object()
        if report.status != 'pending':
            return Response(
                {'detail': '该举报已受理，不能重复受理'},
                status=status.HTTP_400_BAD_REQUEST
            )
        report.status = 'accepted'
        report.accept_time = timezone.now()
        report.acceptor = request.user
        report.save()
        serializer = self.get_serializer(report)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        """转办举报"""
        report = self.get_object()
        to_unit = request.data.get('to_unit')
        transfer_reason = request.data.get('transfer_reason')

        if not to_unit:
            return Response(
                {'detail': '请指定转入单位'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 创建移送记录
        ReportTransfer.objects.create(
            report=report,
            from_unit=report.accused_unit or '未知',
            to_unit=to_unit,
            transfer_reason=transfer_reason,
            transfer_person=request.user.username
        )

        report.status = 'transferred'
        report.save()
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class ReportTransferViewSet(viewsets.ModelViewSet):
    """移送记录视图集"""
    queryset = ReportTransfer.objects.all()
    serializer_class = ReportTransferSerializer
    permission_classes = [IsAuthenticated]
