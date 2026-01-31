#!/bin/bash

echo "============================================"
echo "  智慧监督管理系统 - 启动脚本"
echo "============================================"

# 检查Python
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装"
    exit 1
fi

echo "✅ Python 环境正常"

# 安装依赖
echo ""
echo "安装依赖..."
pip install -r requirements.txt -q

# 创建数据库
echo ""
echo "创建数据库..."
read -p "是否创建数据库? (y/n): " confirm
if [ "$confirm" = "y" ]; then
    read -p "请输入MySQL root密码: " -s mysql_pass
    echo ""
    mysql -u root -p$mysql_pass -e "CREATE DATABASE IF NOT EXISTS supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

    # 执行迁移
    echo "执行数据库迁移..."
    python manage.py makemigrations
    python manage.py migrate
    echo "✅ 数据库迁移完成"
fi

# 初始化数据
echo ""
echo "初始化基础数据..."
python manage.py shell -c "
from apps.crawler.tasks import init_regions, init_tags
init_regions()
init_tags()
print('✅ 初始化完成')
"

# 启动服务
echo ""
echo "============================================"
echo "  启动服务..."
echo "============================================"
echo "  访问地址："
echo "  - 前端页面: http://localhost:8000/"
echo "  - 后台管理: http://localhost:8000/admin/"
echo "============================================"

python manage.py runserver 0.0.0.0:8000
