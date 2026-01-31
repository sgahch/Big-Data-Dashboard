# -*- coding: utf-8 -*-
import logging
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

# 权限定义
PERMISSIONS = {
    'admin': ['view', 'add', 'change', 'delete', 'export', 'crawl', 'admin'],
    'editor': ['view', 'add', 'change', 'export', 'crawl'],
    'viewer': ['view'],
}


class IsAdmin(permissions.BasePermission):
    """管理员权限检查"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff


class IsEditorOrReadOnly(permissions.BasePermission):
    """编辑者或只读权限"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.groups.filter(name='editor').exists()


class UserViewSet(viewsets.ModelViewSet):
    """用户API"""
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        # 非管理员只能看到自己
        if not self.request.user.is_staff:
            qs = qs.filter(id=self.request.user.id)

        # 筛选条件
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')

        group_id = self.request.query_params.get('group')
        if group_id:
            qs = qs.filter(groups__id=group_id)

        return qs.prefetch_related('groups')

    def list(self, request, *args, **kwargs):
        users = self.get_queryset().values(
            'id', 'username', 'email', 'date_joined', 'is_active', 'is_staff'
        )

        # 添加用户组信息
        result = []
        for user in users:
            user_obj = User.objects.get(id=user['id'])
            groups = list(user_obj.groups.values_list('name', flat=True))
            user_data = dict(user)
            user_data['groups'] = groups
            result.append(user_data)

        return Response({
            'code': 0,
            'data': result
        })

    def create(self, request, **kwargs):
        """创建用户"""
        if not request.user.is_staff:
            return Response({
                'code': -1,
                'message': '只有管理员可以创建用户'
            }, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        username = data.get('username')
        password = data.get('password', 'Admin123456')
        email = data.get('email', '')
        is_staff = data.get('is_staff', False)
        group_ids = data.get('groups', [])

        if User.objects.filter(username=username).exists():
            return Response({
                'code': -1,
                'message': '用户名已存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(
                username=username,
                password=make_password(password),
                email=email,
                is_staff=is_staff,
                is_active=True
            )

            if group_ids:
                user.groups.set(group_ids)

            logger.info(f'创建用户: {username}')

            return Response({
                'code': 0,
                'message': '用户创建成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff
                }
            })
        except Exception as e:
            logger.exception('创建用户失败')
            return Response({
                'code': -1,
                'message': f'创建用户失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """重置用户密码"""
        if not request.user.is_staff:
            return Response({
                'code': -1,
                'message': '只有管理员可以重置密码'
            }, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        new_password = request.data.get('password', 'Admin123456')

        if len(new_password) < 6:
            return Response({
                'code': -1,
                'message': '密码长度至少6位'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        logger.info(f'重置用户 {user.username} 的密码')

        return Response({
            'code': 0,
            'message': '密码重置成功'
        })

    @action(detail=True, methods=['post'])
    def set_groups(self, request, pk=None):
        """设置用户角色组"""
        if not request.user.is_staff:
            return Response({
                'code': -1,
                'message': '只有管理员可以设置用户组'
            }, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        group_ids = request.data.get('groups', [])

        user.groups.set(group_ids)
        user.save()

        return Response({
            'code': 0,
            'message': '用户组设置成功'
        })


class GroupViewSet(viewsets.ModelViewSet):
    """用户组API"""
    queryset = Group.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        groups = self.get_queryset().prefetch_related('permissions')

        result = []
        for group in groups:
            result.append({
                'id': group.id,
                'name': group.name,
                'permissions': list(group.permissions.values_list('codename', flat=True)),
                'user_count': group.user_set.count()
            })

        return Response({
            'code': 0,
            'data': result
        })

    def create(self, request, **kwargs):
        """创建用户组"""
        if not request.user.is_staff:
            return Response({
                'code': -1,
                'message': '只有管理员可以创建用户组'
            }, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        permissions = request.data.get('permissions', [])

        if Group.objects.filter(name=name).exists():
            return Response({
                'code': -1,
                'message': '用户组名称已存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.create(name=name)

            if permissions:
                from django.contrib.auth.models import Permission
                perms = Permission.objects.filter(codename__in=permissions)
                group.permissions.set(perms)

            logger.info(f'创建用户组: {name}')

            return Response({
                'code': 0,
                'message': '用户组创建成功',
                'data': {
                    'id': group.id,
                    'name': group.name
                }
            })
        except Exception as e:
            logger.exception('创建用户组失败')
            return Response({
                'code': -1,
                'message': f'创建用户组失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """角色配置API（只读）"""
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """列出所有预定义角色及其权限"""
        return Response({
            'code': 0,
            'data': [
                {
                    'code': 'admin',
                    'name': '管理员',
                    'description': '拥有所有权限',
                    'permissions': PERMISSIONS['admin']
                },
                {
                    'code': 'editor',
                    'name': '编辑者',
                    'description': '可查看、编辑、导出、触发爬取',
                    'permissions': PERMISSIONS['editor']
                },
                {
                    'code': 'viewer',
                    'name': '查看者',
                    'description': '仅可查看数据',
                    'permissions': PERMISSIONS['viewer']
                }
            ]
        })


class CurrentUserView(APIView):
    """当前用户信息"""

    def get(self, request):
        """获取当前用户信息"""
        if not request.user.is_authenticated:
            return Response({
                'code': -1,
                'message': '未登录'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        groups = list(user.groups.values_list('name', flat=True))

        # 确定用户角色
        if user.is_staff:
            role = 'admin'
        elif groups and 'editor' in groups:
            role = 'editor'
        elif groups:
            role = groups[0]
        else:
            role = 'viewer'

        return Response({
            'code': 0,
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff,
                'groups': groups,
                'role': role,
                'date_joined': user.date_joined.isoformat()
            }
        })
