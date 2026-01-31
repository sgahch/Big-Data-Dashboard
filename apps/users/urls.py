# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, RoleViewSet, CurrentUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
]
