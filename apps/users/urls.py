# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, GroupViewSet, RoleViewSet, CurrentUserView, AIChatView,
    LoginView, LogoutView, ForgotPasswordView, ResetPasswordView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
    path('users/me', CurrentUserView.as_view(), name='current-user'),
    path('users/me/', CurrentUserView.as_view(), name='current-user-slash'),
    path('ai/chat', AIChatView.as_view(), name='ai-chat'),
    path('ai/chat/', AIChatView.as_view(), name='ai-chat-slash'),
    path('ai/health', AIChatView.as_view(), name='ai-health'),
    path('ai/health/', AIChatView.as_view(), name='ai-health-slash'),
    # 认证相关路由
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/login/', LoginView.as_view(), name='login-slash'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/logout/', LogoutView.as_view(), name='logout-slash'),
    path('auth/forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password-slash'),
    path('auth/reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset-password-slash'),
]
