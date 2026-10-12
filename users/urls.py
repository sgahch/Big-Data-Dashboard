from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DepartmentViewSet, RegisterViewSet, UserAuthViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'auth', UserAuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
