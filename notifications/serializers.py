from rest_framework import serializers
from .models import Message, MessageTemplate


class MessageSerializer(serializers.ModelSerializer):
    """消息序列化器"""
    class Meta:
        model = Message
        fields = ['id', 'title', 'content', 'msg_type', 'priority', 'sender',
                  'receiver', 'is_read', 'read_time', 'related_type', 'related_id', 'created_at']


class MessageTemplateSerializer(serializers.ModelSerializer):
    """消息模板序列化器"""
    class Meta:
        model = MessageTemplate
        fields = ['id', 'name', 'msg_type', 'title_template', 'content_template', 'is_active', 'created_at']
