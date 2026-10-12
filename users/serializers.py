from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Department

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'real_name', 'email',
                  'phone', 'department', 'role', 'title', 'is_active', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserSimpleSerializer(serializers.ModelSerializer):
    """简化用户序列化器"""
    # 添加 real_name 用于显示
    real_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'department', 'role']


class DepartmentSerializer(serializers.ModelSerializer):
    """部门序列化器"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'parent', 'parent_name', 'leader', 'phone', 'sort', 'is_active']
