from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Case, CaseProgress, Evidence, Trial, Conclusion, AssistPartyTask, Regulation, Supervision, EducationMaterial, EducationActivity
from .serializers import CaseSerializer, CaseCreateUpdateSerializer, CaseProgressSerializer, EvidenceSerializer, TrialSerializer, TrialCreateSerializer, ConclusionSerializer, ConclusionCreateSerializer, AssistPartyTaskSerializer, AssistPartyTaskCreateUpdateSerializer, RegulationSerializer, RegulationCreateUpdateSerializer, SupervisionSerializer, SupervisionCreateUpdateSerializer, EducationMaterialSerializer, EducationMaterialCreateUpdateSerializer, EducationActivitySerializer, EducationActivityCreateUpdateSerializer


class CaseViewSet(viewsets.ModelViewSet):
    """案件视图集"""
    queryset = Case.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CaseCreateUpdateSerializer
        return CaseSerializer

    def get_queryset(self):
        queryset = Case.objects.all()
        stage = self.request.query_params.get('stage')
        status = self.request.query_params.get('status')
        case_level = self.request.query_params.get('case_level')
        if stage:
            queryset = queryset.filter(stage=stage)
        if status:
            queryset = queryset.filter(status=status)
        if case_level:
            queryset = queryset.filter(case_level=case_level)
        return queryset


class CaseProgressViewSet(viewsets.ModelViewSet):
    """案件进度视图集"""
    queryset = CaseProgress.objects.all()
    serializer_class = CaseProgressSerializer
    permission_classes = [IsAuthenticated]


class EvidenceViewSet(viewsets.ModelViewSet):
    """证据视图集"""
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Evidence.objects.all()
        case_id = self.request.query_params.get('case')
        if case_id:
            queryset = queryset.filter(case_id=case_id)
        return queryset


class TrialViewSet(viewsets.ModelViewSet):
    """案件审理视图集"""
    queryset = Trial.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TrialCreateSerializer
        return TrialSerializer

    def get_queryset(self):
        queryset = Trial.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ConclusionViewSet(viewsets.ModelViewSet):
    """结案报告视图集"""
    queryset = Conclusion.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return ConclusionCreateSerializer
        return ConclusionSerializer

    def get_queryset(self):
        queryset = Conclusion.objects.all()
        execution_status = self.request.query_params.get('execution_status')
        archived = self.request.query_params.get('archived')
        if execution_status:
            queryset = queryset.filter(execution_status=execution_status)
        if archived == 'true':
            queryset = queryset.filter(archived=True)
        elif archived == 'false':
            queryset = queryset.filter(archived=False)
        return queryset


class AssistPartyTaskViewSet(viewsets.ModelViewSet):
    """协助党委任务视图集"""
    queryset = AssistPartyTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AssistPartyTaskCreateUpdateSerializer
        return AssistPartyTaskSerializer

    def get_queryset(self):
        queryset = AssistPartyTask.objects.all()
        status = self.request.query_params.get('status')
        search = self.request.query_params.get('search')
        if status is not None:
            queryset = queryset.filter(status=int(status))
        if search:
            queryset = queryset.filter(task_name__icontains=search) | queryset.filter(owner__icontains=search)
        return queryset


class RegulationViewSet(viewsets.ModelViewSet):
    """法规库视图集"""
    queryset = Regulation.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RegulationCreateUpdateSerializer
        return RegulationSerializer

    def get_queryset(self):
        queryset = Regulation.objects.all()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        is_valid = self.request.query_params.get('is_valid')
        if search:
            queryset = queryset.filter(title__icontains=search)
        if category:
            queryset = queryset.filter(category=category)
        if is_valid is not None:
            queryset = queryset.filter(is_valid=is_valid.lower() == 'true')
        return queryset


class SupervisionViewSet(viewsets.ModelViewSet):
    """监督检查视图集"""
    queryset = Supervision.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SupervisionCreateUpdateSerializer
        return SupervisionSerializer

    def get_queryset(self):
        queryset = Supervision.objects.all()
        search = self.request.query_params.get('search')
        supervision_type = self.request.query_params.get('supervision_type')
        status = self.request.query_params.get('status')
        if search:
            queryset = queryset.filter(title__icontains=search)
        if supervision_type:
            queryset = queryset.filter(supervision_type=supervision_type)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class EducationMaterialViewSet(viewsets.ModelViewSet):
    """教育资料视图集"""
    queryset = EducationMaterial.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EducationMaterialCreateUpdateSerializer
        return EducationMaterialSerializer

    def get_queryset(self):
        queryset = EducationMaterial.objects.all()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        if search:
            queryset = queryset.filter(title__icontains=search)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class EducationActivityViewSet(viewsets.ModelViewSet):
    """教育活动视图集"""
    queryset = EducationActivity.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EducationActivityCreateUpdateSerializer
        return EducationActivitySerializer

    def get_queryset(self):
        queryset = EducationActivity.objects.all()
        search = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        if search:
            queryset = queryset.filter(title__icontains=search)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
