"""
AI聊天URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('ai/chat', views.chat, name='ai_chat'),
    path('ai/health', views.health, name='ai_health'),
]

