# 廉智通项目部署指南

## 项目概述

本项目是一个全栈 Web 应用，包含：
- 前端：Vue.js 3 + Vite + TypeScript + Ant Design Vue
- 后端：Django + Django REST Framework
- 数据库：SQLite（开发环境），支持 MySQL（生产环境）

## 部署前准备

### 服务器环境要求
- 操作系统：Linux（推荐 Ubuntu 20.04+ 或 CentOS 8+）
- Python 3.13
- Node.js 18+ / pnpm
- 数据库（MySQL 8.0+ 推荐）
- Nginx

## 前端部署

### 1. 构建前端项目

在项目根目录执行：

```bash
# 安装依赖
pnpm install

# 构建生产版本
pnpm build
```

构建完成后，会在 `dist/` 目录生成静态文件。

### 2. 部署静态文件

将 `dist` 目录下的所有文件上传到服务器的静态文件目录（如 `/var/www/lianzhitong-frontend/`）。

### 3. Nginx 配置

创建 Nginx 配置文件：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为你的域名
    
    # 前端静态文件
    location / {
        root /var/www/lianzhitong-frontend;
        try_files $uri $uri/ /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 代理 API 请求到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 代理媒体文件请求
    location /media/ {
        proxy_pass http://127.0.0.1:8000/media/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 代理管理后台请求
    location /admin/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查
    location /health/ {
        proxy_pass http://127.0.0.1:8000/health/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

重启 Nginx：
```bash
sudo nginx -t  # 检查配置
sudo systemctl reload nginx  # 重新加载配置
```

## 后端部署

### 1. 服务器环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 3.13 和相关工具
sudo apt install python3.13 python3.13-venv python3.13-dev build-essential -y

# 安装数据库（如果使用 MySQL）
sudo apt install mysql-server -y
```

### 2. 项目部署

在服务器上创建项目目录：

```bash
mkdir -p /opt/lianzhitong
cd /opt/lianzhitong
```

上传或克隆项目代码到此目录。

### 3. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境
python3.13 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装生产依赖
pip install -r backend/requirements.txt

# 安装 Gunicorn（生产环境 WSGI 服务器）
pip install gunicorn
```

### 4. 配置生产环境设置

修改 `backend/lianzhitong/settings.py`：

```python
import os

# 生产环境配置
DEBUG = False

# 设置为你的域名或服务器 IP
ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip']

# 生产环境密钥（从环境变量读取）
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-production-secret-key')

# 生产环境数据库配置（示例使用 MySQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'lianzhitong'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your-password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = '/opt/lianzhitong/staticfiles/'

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = '/opt/lianzhitong/media/'
```

### 5. 数据库设置

创建数据库（如果使用 MySQL）：

```sql
CREATE DATABASE lianzhitong CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lianzhitong_user'@'localhost' IDENTIFIED BY 'your-secure-password';
GRANT ALL PRIVILEGES ON lianzhitong.* TO 'lianzhitong_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. 运行数据库迁移

```bash
# 激活虚拟环境
source venv/bin/activate

# 进入后端目录
cd /opt/lianzhitong/backend

# 运行迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

### 7. 启动后端服务

使用 Gunicorn 启动 Django 应用：

```bash
# 激活虚拟环境
source venv/bin/activate

# 进入后端目录
cd /opt/lianzhitong/backend

# 启动服务
gunicorn lianzhitong.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120 --max-requests 1000 --max-requests-jitter 100
```

### 8. 使用 systemd 管理服务

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/lianzhitong-backend.service
```

内容如下：

```ini
[Unit]
Description=LianZhiTong Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/lianzhitong/backend
Environment=PATH=/opt/lianzhitong/venv/bin
EnvironmentFile=/opt/lianzhitong/.env
ExecStart=/opt/lianzhitong/venv/bin/gunicorn lianzhitong.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120 --max-requests 1000 --max-requests-jitter 100
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

创建环境变量文件：

```bash
sudo nano /opt/lianzhitong/.env
```

```bash
DJANGO_SECRET_KEY=your-production-secret-key
DB_NAME=lianzhitong
DB_USER=lianzhitong_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306
```

设置权限和启动服务：

```bash
sudo chown -R www-data:www-data /opt/lianzhitong
sudo systemctl daemon-reload
sudo systemctl enable lianzhitong-backend
sudo systemctl start lianzhitong-backend
sudo systemctl status lianzhitong-backend
```

## 环境变量配置

创建 `.env` 文件来管理敏感信息：

```bash
# 后端环境变量示例
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=mysql://user:password@localhost:3306/database_name
DB_NAME=lianzhitong
DB_USER=lianzhitong_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=3306
```

## SSL 证书配置（推荐）

使用 Let's Encrypt 获取免费 SSL 证书：

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## 监控与日志

### 日志配置

后端日志会记录在 Gunicorn 输出中，可以重定向到文件：

```bash
gunicorn lianzhitong.wsgi:application --bind 0.0.0.0:8000 --workers 4 --error-logfile /var/log/lianzhitong/error.log --access-logfile /var/log/lianzhitong/access.log
```

### 系统监控

可使用 `htop`、`pm2` 或其他监控工具来监控应用状态。

## 常见问题

### 1. 权限问题
确保应用目录有正确的权限：
```bash
sudo chown -R www-data:www-data /opt/lianzhitong
```

### 2. 静态文件无法访问
确认运行了 `collectstatic` 命令并正确配置了 Nginx。

### 3. 数据库连接失败
检查数据库服务是否运行，以及配置文件中的连接参数是否正确。

### 4. 端口冲突
确保 8000 端口未被其他服务占用。

## 备份策略

### 数据库备份
```bash
# MySQL 备份
mysqldump -u root -p lianzhitong > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 代码和配置备份
定期备份项目代码和配置文件。

## 更新部署

### 1. 停止服务
```bash
sudo systemctl stop lianzhitong-backend
```

### 2. 更新代码
```bash
cd /opt/lianzhitong
git pull origin main  # 如果使用 Git
```

### 3. 更新依赖
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 4. 运行迁移
```bash
cd backend
python manage.py migrate
```

### 5. 重新收集静态文件
```bash
python manage.py collectstatic --noinput
```

### 6. 重启服务
```bash
sudo systemctl start lianzhitong-backend
```