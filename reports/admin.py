from django.contrib import admin
from .models import Report, ReportTransfer


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_no', 'title', 'report_type', 'report_level', 'accused_name', 'status', 'acceptor', 'created_at']
    list_filter = ['report_type', 'report_level', 'status']
    search_fields = ['report_no', 'title', 'accused_name', 'reporter_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['acceptor', 'handler']


@admin.register(ReportTransfer)
class ReportTransferAdmin(admin.ModelAdmin):
    list_display = ['report', 'from_unit', 'to_unit', 'transfer_person', 'transfer_time']
    list_filter = ['from_unit', 'to_unit']
    search_fields = ['report__report_no', 'transfer_person']
    ordering = ['-transfer_time']
