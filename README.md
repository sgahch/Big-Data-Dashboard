# 智慧监督管理系统

基于 Django + MySQL 的纪检监察数据爬取与分析系统。

## 功能特性

- **自动爬虫**：定时爬取陕西各地市清风网新闻
- **智能打标签**：自动根据关键词识别违规类型
- **数据分析**：违规事项分布、案件查处统计
- **后台管理**：Django Admin 自带完整管理界面
- **REST API**：提供数据接口供前端调用

## 技术栈

- **后端**：Django 4.2 + Django REST Framework
- **数据库**：MySQL 8.0 + Redis（可选缓存）
- **爬虫**：Requests + BeautifulSoup + APScheduler
- **前端**：ECharts 可视化

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

确保 MySQL 已启动，并创建数据库：

```sql
CREATE DATABASE supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 初始化项目

```bash
# 创建数据库表
python manage.py makemigrations
python manage.py migrate

# 初始化基础数据
python manage.py shell -c "
from apps.crawler.tasks import init_regions, init_tags
init_regions()
init_tags()
"
```

### 4. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端页面 | http://localhost:8000/ |
| 后台管理 | http://localhost:8000/admin/ |
| API接口 | http://localhost:8000/api/ |

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/news/` | GET | 新闻列表 |
| `/api/stats/violations/` | GET | 违规事项分布 |
| `/api/stats/cases/` | GET | 案件查处统计 |
| `/api/stats/regions/` | GET | 地区统计 |
| `/api/news/force-crawl/` | POST | 手动触发爬取 |

## 后台管理

访问 http://localhost:8000/admin/ ，使用管理员账号登录后可管理：
- 新闻管理
- 标签管理
- 地区管理
- 爬取日志
- 用户管理

## 定时任务

- 每4小时自动爬取所有地区
- 每天8:00额外爬取

## 项目结构

```
├── supervision/      # Django项目配置
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── news/         # 新闻管理
│   ├── crawler/      # 爬虫模块
│   ├── stats/        # 统计分析
│   └── users/        # 用户管理
├── manage.py
└── requirements.txt
```
