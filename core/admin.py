from django.contrib import admin
from .models import AssistParty, DisciplineEducation, Supervision, Clue, Regulation


@admin.register(AssistParty)
class AssistPartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'assist_type', 'party_organization', 'status', 'start_date', 'handler']
    list_filter = ['assist_type', 'status']
    search_fields = ['title', 'party_organization']
    ordering = ['-created_at']


@admin.register(DisciplineEducation)
class DisciplineEducationAdmin(admin.ModelAdmin):
    list_display = ['title', 'edu_type', 'target_dept', 'is_published', 'publish_time', 'publisher']
    list_filter = ['edu_type', 'is_published']
    search_fields = ['title', 'content']
    ordering = ['-created_at']


@admin.register(Supervision)
class SupervisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'supervision_type', 'status', 'start_date', 'end_date', 'leader']
    list_filter = ['supervision_type', 'status']
    search_fields = ['title', 'target_objects']
    ordering = ['-created_at']


@admin.register(Clue)
class ClueAdmin(admin.ModelAdmin):
    list_display = ['clue_no', 'title', 'source', 'status', 'discoverer', 'reviewer', 'created_at']
    list_filter = ['source', 'status']
    search_fields = ['clue_no', 'title', 'content']
    ordering = ['-created_at']
    raw_id_fields = ['reviewer', 'handler']


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'document_no', 'issuing_authority', 'effective_date', 'is_valid']
    list_filter = ['category', 'is_valid']
    search_fields = ['title', 'content']
    ordering = ['-effective_date']
