"""
URL configuration for lianzhitong project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import home, health

urlpatterns = [
    # 首页 - 重定向到后台管理
    path('', home, name='home'),

    # 健康检查
    path('health/', health, name='health'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Admin logout - 确保登出正常工作
    path('admin/logout/', LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),

    # REST Framework auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API routes
    path('api/', include('users.urls')),
    path('api/', include('reports.urls')),
    path('api/', include('cases.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
