from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """自定义用户管理器"""
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名必须提供')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    """自定义用户模型"""
    ROLE_CHOICES = [
        ('admin', '系统管理员'),
        ('leader', '领导'),
        ('investigator', '办案人员'),
        ('clerk', '一般工作人员'),
    ]

    DEPT_CHOICES = [
        ('discipline', '纪检监察室'),
        ('supervision', '监督执纪室'),
        ('office', '办公室'),
    ]

    real_name = models.CharField('真实姓名', max_length=50, blank=True)
    phone = models.CharField('手机号码', max_length=11, blank=True)
    department = models.CharField('所属部门', max_length=50, choices=DEPT_CHOICES, default='discipline')
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='clerk')
    title = models.CharField('职务', max_length=50, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门模型"""
    name = models.CharField('部门名称', max_length=100)
    code = models.CharField('部门代码', max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级部门')
    leader = models.CharField('部门负责人', max_length=50, blank=True)
    phone = models.CharField('联系电话', max_length=20, blank=True)
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['sort']

    def __str__(self):
        return self.name
