from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import AssistParty, DisciplineEducation, Supervision, Clue, Regulation
from .serializers import (AssistPartySerializer, DisciplineEducationSerializer,
                          SupervisionSerializer, ClueSerializer, RegulationSerializer)


@api_view(['GET'])
def home(request):
    """首页 - 重定向到后台管理"""
    return redirect('/admin/')


@api_view(['GET'])
def health(request):
    """健康检查"""
    return Response({'status': 'ok', 'message': '廉智通 API 运行正常'})


class AssistPartyViewSet(viewsets.ModelViewSet):
    """协助党委视图集"""
    queryset = AssistParty.objects.all()
    serializer_class = AssistPartySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AssistParty.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class DisciplineEducationViewSet(viewsets.ModelViewSet):
    """纪律教育视图集"""
    queryset = DisciplineEducation.objects.all()
    serializer_class = DisciplineEducationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = DisciplineEducation.objects.all()
        edu_type = self.request.query_params.get('edu_type')
        is_published = self.request.query_params.get('is_published')
        if edu_type:
            queryset = queryset.filter(edu_type=edu_type)
        if is_published is not None:
            queryset = queryset.filter(is_published=is_published == 'true')
        return queryset


class SupervisionViewSet(viewsets.ModelViewSet):
    """监督检查视图集"""
    queryset = Supervision.objects.all()
    serializer_class = SupervisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Supervision.objects.all()
        status = self.request.query_params.get('status')
        supervision_type = self.request.query_params.get('supervision_type')
        if status:
            queryset = queryset.filter(status=status)
        if supervision_type:
            queryset = queryset.filter(supervision_type=supervision_type)
        return queryset


class ClueViewSet(viewsets.ModelViewSet):
    """线索处置视图集"""
    queryset = Clue.objects.all()
    serializer_class = ClueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Clue.objects.all()
        status = self.request.query_params.get('status')
        source = self.request.query_params.get('source')
        if status:
            queryset = queryset.filter(status=status)
        if source:
            queryset = queryset.filter(source=source)
        return queryset


class RegulationViewSet(viewsets.ModelViewSet):
    """法规库视图集"""
    queryset = Regulation.objects.all()
    serializer_class = RegulationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Regulation.objects.all()
        category = self.request.query_params.get('category')
        is_valid = self.request.query_params.get('is_valid')
        if category:
            queryset = queryset.filter(category=category)
        if is_valid is not None:
            queryset = queryset.filter(is_valid=is_valid == 'true')
        return queryset
