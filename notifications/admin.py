from django.contrib import admin
from .models import Message, MessageTemplate


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'msg_type', 'priority', 'sender', 'receiver', 'is_read', 'created_at']
    list_filter = ['msg_type', 'priority', 'is_read']
    search_fields = ['title', 'content', 'sender', 'receiver__username']
    ordering = ['-created_at']
    raw_id_fields = ['receiver', 'sender_user']


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'msg_type', 'is_active', 'created_at']
    list_filter = ['msg_type', 'is_active']
    search_fields = ['name', 'title_template']
