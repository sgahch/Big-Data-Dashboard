@echo off
chcp 65001 >nul
echo ========================================
echo 清风网爬虫服务启动脚本
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境，请先安装Python 3.7+
    pause
    exit /b 1
)
echo.

echo [2/3] 安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo 警告: 依赖安装可能失败，尝试继续运行...
)
echo.

echo [3/3] 启动爬虫服务...
echo 服务将运行在 http://localhost:5000
echo 按 Ctrl+C 可停止服务
echo.
python server.py

pause

