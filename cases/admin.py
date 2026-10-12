from django.contrib import admin
from .models import Case, CaseProgress, Evidence


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_no', 'case_name', 'stage', 'status', 'case_level', 'suspect_name', 'leader', 'created_at']
    list_filter = ['stage', 'status', 'case_level']
    search_fields = ['case_no', 'case_name', 'suspect_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    raw_id_fields = ['leader']


@admin.register(CaseProgress)
class CaseProgressAdmin(admin.ModelAdmin):
    list_display = ['case', 'progress_type', 'progress_date', 'handler']
    list_filter = ['progress_type']
    search_fields = ['case__case_no', 'progress_content']
    ordering = ['-progress_date']


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ['case', 'evidence_type', 'name', 'submitter', 'created_at']
    list_filter = ['evidence_type']
    search_fields = ['case__case_no', 'name']
    ordering = ['-created_at']
