# Supervision Project Settings
import os
from pathlib import Path
import sys
import socket

# --- 关键修复：确保 Django 识别 PyMySQL 为 MySQL 驱动 ---
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# ========== 自动环境检测 ==========
def detect_environment():
    """自动检测运行环境"""
    # 方法1: 检查环境变量
    if os.getenv('ENV') == 'production':
        return 'production'

    # 方法2: 检查主机名（云服务器通常有特定主机名）
    hostname = socket.gethostname().lower()
    if any(keyword in hostname for keyword in ['server', 'cloud', 'aliyun', 'tencent', 'huawei', 'prod']):
        return 'production'

    # 方法3: 检查是否存在生产环境标识文件
    if os.path.exists('/etc/production') or os.path.exists(BASE_DIR / '.production'):
        return 'production'

    # 方法4: 检查IP地址（本地开发通常是127.0.0.1或192.168.x.x）
    try:
        hostname_ip = socket.gethostbyname(socket.gethostname())
        # 如果不是本地IP，可能是生产环境
        if not (hostname_ip.startswith('127.') or hostname_ip.startswith('192.168.') or hostname_ip.startswith('10.')):
            return 'production'
    except:
        pass

    return 'development'

# 检测环境
ENV = detect_environment()
print(f"🌍 Django环境检测: {ENV}")

# 加载对应的 .env 文件
from dotenv import load_dotenv

# 根据环境选择配置文件
if ENV == 'production':
    env_file = '.env.production'
else:
    env_file = '.env.development'

# 优先查找根目录的配置文件
env_path = os.path.join(BASE_DIR, env_file)

# 如果没有找到，尝试 config 目录
if not os.path.exists(env_path):
    env_path = os.path.join(BASE_DIR, 'config', '.env.prod' if ENV == 'production' else '.env.dev')

# 如果还没找到，尝试加载默认的 .env
if not os.path.exists(env_path):
    env_path = os.path.join(BASE_DIR, 'config', '.env')
    if not os.path.exists(env_path):
        env_path = os.path.join(BASE_DIR, '.env')

if os.path.exists(env_path):
    print(f"📄 加载配置文件: {env_path}")
    load_dotenv(env_path)
else:
    print(f"⚠️  未找到配置文件，使用默认配置")

# 从环境变量获取最终的ENV值（可能被.env文件覆盖）
ENV = os.environ.get('ENV', ENV)
IS_PROD = ENV == 'production'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-supervision-project-key')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True' if not IS_PROD else 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

# 确保 apps 目录在路径中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'import_export',
    'apps.news',
    'apps.crawler',
    'apps.users',
    'apps.stats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'supervision.middleware.SecurityHeadersMiddleware',  # 自定义安全头中间件
]

ROOT_URLCONF = 'supervision.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'supervision.wsgi.application'

# --- 数据库配置：都使用MySQL ---
print(f"📊 数据库: MySQL ({'生产' if IS_PROD else '开发'}环境)")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'supervision'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 500,  # 增加默认分页大小，支持显示更多新闻
}

CORS_ALLOW_ALL_ORIGINS = True
APPEND_SLASH = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'apps': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
    },
    'formatters': {
        'simple': {'format': '{levelname} {asctime} {message}', 'style': '{'},
    },
}

# 允许iframe嵌入（用于3D地图）
X_FRAME_OPTIONS = 'SAMEORIGIN'

# ========== 安全头配置 ==========
# 根据环境配置安全策略
if IS_PROD:
    # 生产环境：启用严格的安全策略（需要HTTPS）
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
    SECURE_SSL_REDIRECT = False  # 如果使用HTTPS，设置为True
    SESSION_COOKIE_SECURE = False  # 如果使用HTTPS，设置为True
    CSRF_COOKIE_SECURE = False  # 如果使用HTTPS，设置为True
else:
    # 开发环境：不启用COOP策略（避免警告）
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# 其他安全配置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True