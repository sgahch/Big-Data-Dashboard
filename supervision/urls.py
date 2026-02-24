"""
supervision URL Configuration
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.news.urls')),
    path('api/', include('apps.crawler.urls')),
    path('api/', include('apps.stats.urls')),
    path('api/', include('apps.users.urls')),
    # 前端页面
    re_path(r'^$', lambda request: serve(request, 'index.html', document_root=BASE_DIR)),
    re_path(r'^(?!api/)(?!admin/)(?!static/)(?P<path>.*)$',
            lambda request, path: serve(request, path, document_root=BASE_DIR) if os.path.exists(os.path.join(BASE_DIR, path)) else serve(request, 'index.html', document_root=BASE_DIR)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
