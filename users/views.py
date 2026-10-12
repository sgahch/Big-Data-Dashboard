from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Department
from .serializers import UserSerializer, UserSimpleSerializer, DepartmentSerializer

User = get_user_model()


class UserAuthViewSet(viewsets.GenericViewSet):
    """用户认证相关视图集"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='check-username')
    def check_username(self, request):
        """检查用户名是否已存在"""
        username = request.query_params.get('username', '')
        if not username:
            return Response({'available': True, 'message': '请输入用户名'})
        exists = User.objects.filter(username=username).exists()
        if exists:
            return Response({'available': False, 'message': '用户名已存在'})
        return Response({'available': True, 'message': '用户名可用'})

    @action(detail=False, methods=['get'], url_path='me')
    def get_current_user(self, request):
        """获取当前登录用户信息"""
        if not request.user.is_authenticated:
            return Response({'error': '未登录'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """用户注册视图集（无需认证）"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        real_name = request.data.get('real_name', '')
        phone = request.data.get('phone', '')

        if not username or not password:
            return Response(
                {'error': '用户名和密码不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': '用户名已存在'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            real_name=real_name,
            phone=phone,
            role='staff',  # 默认普通员工角色
            is_active=True
        )

        return Response(
            {
                'message': '注册成功',
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSimpleSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        department = self.request.query_params.get('department')
        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')

        if department:
            queryset = queryset.filter(department=department)
        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    """部门视图集"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Department.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active == 'true')
        return queryset
