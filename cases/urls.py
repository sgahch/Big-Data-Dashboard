from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, CaseProgressViewSet, EvidenceViewSet, TrialViewSet, ConclusionViewSet, AssistPartyTaskViewSet, RegulationViewSet, SupervisionViewSet, EducationMaterialViewSet, EducationActivityViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'case-progress', CaseProgressViewSet, basename='case-progress')
router.register(r'evidences', EvidenceViewSet, basename='evidence')
router.register(r'trials', TrialViewSet, basename='trial')
router.register(r'conclusions', ConclusionViewSet, basename='conclusion')
router.register(r'assist-party-tasks', AssistPartyTaskViewSet, basename='assist-party-task')
router.register(r'regulations', RegulationViewSet, basename='regulation')
router.register(r'supervision', SupervisionViewSet, basename='supervision')
router.register(r'education-materials', EducationMaterialViewSet, basename='education-material')
router.register(r'education-activities', EducationActivityViewSet, basename='education-activity')

urlpatterns = [
    path('', include(router.urls)),
]
