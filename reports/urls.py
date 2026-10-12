from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ReportTransferViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'report-transfers', ReportTransferViewSet, basename='report-transfer')

urlpatterns = [
    path('', include(router.urls)),
]
