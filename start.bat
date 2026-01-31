@echo off
chcp 65001 >nul
echo ============================================
echo   智慧监督管理系统 - 启动脚本
echo ============================================

echo.
echo [1/5] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ Python 未安装，请先安装 Python 3.9+
    pause
    exit /b 1
)
echo   ✅ Python 环境正常

echo.
echo [2/5] 安装依赖...
pip install -r requirements.txt -q
echo   ✅ 依赖安装完成

echo.
echo [3/5] 初始化数据库...
echo   请确保MySQL已启动，并创建数据库：
echo   CREATE DATABASE supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo.
set /p confirm="是否执行数据库迁移? (y/n): "
if "%confirm%"=="y" (
    python manage.py makemigrations
    python manage.py migrate
    echo   ✅ 数据库迁移完成
)

echo.
echo [4/5] 初始化数据...
python manage.py shell -c "
from apps.crawler.tasks import init_regions, init_tags
init_regions()
init_tags()
print('✅ 地区和标签数据初始化完成')
" 2>nul

echo.
echo [5/5] 启动服务...
echo.
echo ============================================
echo   访问地址：
echo   - 前端页面: http://localhost:8000/
echo   - 后台管理: http://localhost:8000/admin/
echo   - API文档: http://localhost:8000/api/
echo ============================================
echo.
python manage.py runserver 0.0.0.0:8000
