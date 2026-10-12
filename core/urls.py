from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AssistPartyViewSet, DisciplineEducationViewSet,
                    SupervisionViewSet, ClueViewSet, RegulationViewSet)

router = DefaultRouter()
router.register(r'assist-party', AssistPartyViewSet, basename='assist-party')
router.register(r'discipline-education', DisciplineEducationViewSet, basename='discipline-education')
router.register(r'supervision', SupervisionViewSet, basename='supervision')
router.register(r'clues', ClueViewSet, basename='clue')
router.register(r'regulations', RegulationViewSet, basename='regulation')

urlpatterns = [
    path('', include(router.urls)),
]
