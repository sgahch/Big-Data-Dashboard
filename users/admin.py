from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'real_name', 'department', 'role', 'phone', 'is_active']
    list_filter = ['department', 'role', 'is_active']
    search_fields = ['username', 'real_name', 'phone']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'phone', 'email')}),
        ('工作信息', {'fields': ('department', 'role', 'title')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('时间', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'department', 'role'),
        }),
    )

    def real_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    real_name.short_description = '姓名'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'leader', 'phone', 'sort', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['sort']
