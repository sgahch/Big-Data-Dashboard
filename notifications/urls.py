from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageTemplateViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'message-templates', MessageTemplateViewSet, basename='message-template')

urlpatterns = [
    path('', include(router.urls)),
]
