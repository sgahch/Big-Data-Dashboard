# 纪检监察大数据看板系统

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**基于 Django + ECharts 的纪检监察数据爬取、分析与可视化系统**

[功能特性](#功能特性) • [快速开始](#快速开始) • [API文档](#api接口文档) • [系统架构](#系统架构) • [演示环境](#演示环境)

</div>

---

## 📊 功能特性

### 🔍 数据采集与处理

| 功能 | 描述 |
|------|------|
| 智能爬虫系统 | 基于 Requests + BeautifulSoup 自动爬取陕西各地市清风网新闻数据 |
| 定时任务调度 | 使用 APScheduler 实现周期性数据采集，支持自定义爬取间隔 |
| 智能去重机制 | 基于标题和内容的相似度算法，自动过滤重复新闻 |
| 智能标签识别 | 使用关键词匹配算法自动识别违规类型并打标签 |
| 数据质量监控 | 实时监控爬取成功率和数据完整性 |

### 📈 数据分析与可视化

| 功能 | 描述 |
|------|------|
| 违规事项分布 | 柱状图展示各类违规行为占比，支持多维度筛选 |
| 案件查处趋势 | 折线图展示时间维度上的案件数量变化趋势 |
| 地区分布统计 | 饼图展示各地区案件分布情况，支持地图可视化 |
| 实时数据更新 | 仪表盘实时展示今日数据概览和关键指标 |
| 数据钻取分析 | 支持从宏观到微观的多层级数据分析 |
| 交互式图表 | 支持图表放大、筛选、导出等交互功能 |

### 🤖 AI 智能客服

| 功能 | 描述 |
|------|------|
| Coze AI 集成 | 基于大语言模型的智能问答系统 |
| 数据分析解读 | 智能解读可视化图表和统计结果 |
| 自然语言查询 | 支持用自然语言查询特定数据和统计信息 |
| 智能报告生成 | 根据用户需求自动生成分析报告 |

### 📑 报告导出

| 格式 | 描述 |
|------|------|
| Word 报告 | 生成规范化 Word 文档，包含图表和数据分析 |
| Excel 报告 | 导出多维度数据表格，支持数据透视分析 |
| PDF 报告 | 生成专业 PDF 格式报告，支持打印和分享 |

### 🔐 权限管理

| 功能 | 描述 |
|------|------|
| 多级权限控制 | 支持管理员、编辑、查看等不同权限级别 |
| 用户角色管理 | 可配置的用户角色和权限分配 |
| 操作审计日志 | 记录用户操作行为，确保数据安全 |

---

## 🛠️ 技术栈

<div align="left">

| 类别 | 技术栈 | 版本/框架 |
|------|--------|-----------|
| 后端框架 | Django | 4.2+ |
| Web 框架 | Django REST Framework | 3.14+ |
| 数据库 | MySQL | 8.0+ |
| 缓存系统 | Redis | 6.0+ (可选) |
| 爬虫技术 | Requests + BeautifulSoup + lxml | 最新 |
| 定时任务 | APScheduler | 3.10+ |
| 前端技术 | HTML5 + CSS3 + JavaScript | ES6+ |
| 数据可视化 | ECharts | 5.0+ |
| 图标库 | Font Awesome | 6.0+ |
| AI 集成 | Coze API | 最新 |
| 报告生成 | python-docx + openpyxl + xhtml2pdf | 最新 |
| 依赖管理 | pip | 23.0+ |

</div>

---

## 📁 项目结构

```
.
├── supervision/              # Django 项目配置
│   ├── __init__.py           # 项目初始化
│   ├── settings.py           # 项目配置文件
│   ├── urls.py               # 项目主路由
│   ├── wsgi.py               # WSGI 配置
│   └── asgi.py               # ASGI 配置
├── apps/                     # 业务应用模块
│   ├── __init__.py
│   ├── core/                 # 核心功能
│   │   └── cache.py          # 缓存配置
│   ├── crawler/              # 爬虫模块
│   │   ├── __init__.py
│   │   ├── admin.py          # 管理后台配置
│   │   ├── apps.py           # 应用配置
│   │   ├── config_views.py   # 配置视图
│   │   ├── crawler.py        # 爬虫核心逻辑
│   │   ├── models.py         # 爬虫相关模型
│   │   ├── scheduler.py      # 定时任务调度
│   │   ├── tasks.py          # 爬虫任务
│   │   ├── urls.py           # 爬虫路由
│   │   ├── views.py          # 爬虫视图
│   │   ├── management/       # 管理命令
│   │   └── migrations/       # 数据库迁移文件
│   ├── news/                 # 新闻管理模块
│   │   ├── admin.py          # 新闻管理后台
│   │   ├── apps.py           # 应用配置
│   │   ├── models.py         # 新闻相关模型
│   │   ├── serializers.py    # 序列化器
│   │   ├── signals.py        # 信号处理
│   │   ├── urls.py           # 新闻路由
│   │   └── views.py          # 新闻视图
│   ├── stats/                # 统计分析模块
│   │   ├── __init__.py
│   │   ├── apps.py           # 应用配置
│   │   ├── report.py         # 报告生成模块
│   │   ├── urls.py           # 统计路由
│   │   └── views.py          # 统计视图
│   └── users/                # 用户管理模块
│       ├── __init__.py
│       ├── apps.py           # 应用配置
│       ├── urls.py           # 用户路由
│       └── views.py          # 用户视图
├── api/                      # API 接口模块
│   └── news.py               # 新闻相关API
├── templates/                # HTML 模板
│   └── index.html            # 主页模板
├── static/                   # 静态文件
│   ├── css/                  # 样式文件
│   ├── js/                   # JavaScript 文件
│   ├── images/               # 图片文件
│   └── libs/                 # 第三方库
├── docs/                     # 文档目录
│   ├── 功能清单.md           # 功能说明文档
│   ├── 开发阶段记录.md       # 开发历程记录
│   └── 其他文档...
├── .env                      # 环境变量配置
├── .env.example              # 环境变量示例
├── .gitignore                # Git 忽略配置
├── requirements.txt          # Python 依赖
├── manage.py                 # Django 管理脚本
├── config.py                 # 配置文件
├── models.py                 # 项目模型
├── server.py                 # 服务器配置
├── scheduler.py              # 调度器
├── start.bat                 # Windows 启动脚本
├── start.sh                  # Linux/macOS 启动脚本
├── setup_and_crawl.py        # 初始化和爬取脚本
├── trigger_crawl.py          # 触发爬虫脚本
├── start_crawler.py          # 爬虫启动脚本
├── shaanxi_3d_map.html       # 3D 地图可视化
├── shaanxi_3d_map_optimized.html  # 优化版 3D 地图
├── index.html                # 主前端页面
├── README.md                 # 项目说明文档
└── supervision.sql           # 数据库脚本
```

---

## 🚀 快速开始

### 环境要求

- **操作系统**: Windows 7+, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python**: 3.11 或更高版本
- **数据库**: MySQL 8.0 或 PostgreSQL 12+
- **内存**: 至少 4GB RAM (推荐 8GB+)
- **存储**: 至少 20GB 可用空间 (用于数据存储和缓存)

### 1. 克隆项目

```bash
# 安装 Git (如尚未安装)
# Windows: https://git-scm.com/download/win
# Linux: sudo apt install git
# macOS: brew install git

# 克隆项目
git clone https://github.com/sgahch/Big-Data-Dashboard.git
cd Big-Data-Dashboard
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 如遇依赖安装问题，可尝试
pip install --no-cache-dir -r requirements.txt
```

### 4. 配置数据库

确保 MySQL 已启动，并创建数据库：

```sql
-- 连接 MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 为项目创建专用用户（推荐）
CREATE USER 'supervision_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON supervision.* TO 'supervision_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env` 并修改：

```env
# 数据库配置
DB_NAME=supervision
DB_USER=supervision_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=3306

# Coze AI 配置（可选）
COZE_API_TOKEN=your_coze_api_token
COZE_BOT_ID=your_coze_bot_id

# Django 配置
DJANGO_SECRET_KEY=your-very-secret-key-here
DJANGO_DEBUG=True  # 生产环境设为 False

# Redis 配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 时区配置
TIME_ZONE=Asia/Shanghai
USE_TZ=False

# 邮件配置（可选）
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True

# 爬虫配置
CRAWLER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
CRAWLER_DELAY=1  # 爬取延迟（秒）
MAX_CRAWLER_THREADS=5  # 最大爬虫线程数
```

### 6. 初始化项目

```bash
# 创建数据库表
python manage.py makemigrations
python manage.py migrate

# 初始化基础数据（地区、标签）
python manage.py shell -c "
from apps.crawler.tasks import init_regions, init_tags
init_regions()
init_tags()
print('基础数据初始化完成')
"

# 创建超级管理员
python manage.py createsuperuser

# 预加载初始数据（可选）
python setup_and_crawl.py
```

### 7. 启动服务

```bash
# 方式一：使用启动脚本（Windows）
start.bat

# 方式二：直接运行
python manage.py runserver 0.0.0.0:8000

# 方式三：后台运行（Linux/macOS）
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
```

---

## 📖 API 接口文档

### 新闻管理 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/news/` | GET | 新闻列表（支持分页、筛选） | page, size, region, tag, start_date, end_date | 分页新闻列表 |
| `/api/news/<id>/` | GET | 新闻详情 | - | 单篇新闻详情 |
| `/api/news/force-crawl/` | POST | 手动触发爬取 | - | 爬取结果 |
| `/api/news/search/` | GET | 搜索新闻 | q, page, size | 搜索结果 |
| `/api/news/tags/` | GET | 获取所有标签 | - | 标签列表 |
| `/api/news/regions/` | GET | 获取所有地区 | - | 地区列表 |

### 统计分析 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/stats/dashboard/` | GET | 仪表盘数据 | - | 综合统计信息 |
| `/api/stats/violations/` | GET | 违规事项分布 | start_date, end_date | 违规分布数据 |
| `/api/stats/cases/` | GET | 案件查处统计 | start_date, end_date | 案件统计数据 |
| `/api/stats/regions/` | GET | 地区统计 | start_date, end_date | 地区统计数据 |
| `/api/stats/tags/` | GET | 标签统计 | start_date, end_date | 标签统计数据 |
| `/api/stats/weekly/` | GET | 周统计 | start_date, end_date | 周统计数据 |
| `/api/stats/articles/` | GET | 文章管理统计 | start_date, end_date | 文章统计数据 |
| `/api/stats/export/` | GET | 导出统计数据 | format, start_date, end_date | 导出文件 |

### 报告导出 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/stats/report/` | GET | 预览报告数据 | - | 报告数据 |
| `/api/stats/report/` | POST | 生成并下载报告 | type, start_date, end_date | 报告文件 |
| `/api/stats/report/template/` | GET | 获取报告模板 | type | 模板信息 |

> **报告类型参数**：`type=word` / `type=excel` / `type=pdf`

### AI 客服 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/ai/chat/` | POST | AI 聊天对话 | message, history | AI 回复 |
| `/api/ai/health/` | GET | AI 服务健康检查 | - | 服务状态 |
| `/api/ai/analytics/` | POST | 数据分析查询 | query, data_scope | 分析结果 |

### 用户管理 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/users/` | GET | 用户列表 | page, size, role | 分页用户列表 |
| `/api/users/me/` | GET | 当前用户信息 | - | 用户信息 |
| `/api/users/profile/` | PUT | 更新用户资料 | profile_data | 更新结果 |
| `/api/users/groups/` | GET | 用户组列表 | - | 用户组列表 |
| `/api/users/roles/` | GET | 角色配置（只读） | - | 角色列表 |

### 爬虫管理 API

| 接口 | 方法 | 说明 | 参数 | 返回 |
|------|------|------|------|------|
| `/api/crawler/config/` | GET | 获取爬虫配置 | - | 爬虫配置信息 |
| `/api/crawler/config/` | PUT | 更新爬虫配置 | config | 更新结果 |
| `/api/crawler/status/` | GET | 爬虫运行状态 | - | 状态信息 |
| `/api/crawler/start/` | POST | 启动爬虫 | - | 启动结果 |
| `/api/crawler/stop/` | POST | 停止爬虫 | - | 停止结果 |

---

## ⏰ 定时任务

### 默认调度配置

| 任务 | 周期 | 描述 | 优先级 |
|------|------|------|--------|
| 周期爬取 | 每 4 小时 | 自动爬取所有地区清风网数据 | 高 |
| 每日汇总 | 每天 8:00 | 执行额外爬取任务和数据汇总 | 中 |
| 数据清理 | 每周日凌晨2点 | 清理过期缓存和临时数据 | 低 |
| 数据备份 | 每日 2:00 | 备份数据库到指定位置 | 高 |
| 报告生成 | 每周一 9:00 | 生成上周统计报告 | 中 |

### 后台管理配置

访问 `/admin/crawler/crawlconfig/` 可修改爬虫配置：
- 爬取间隔时间（最小1小时）
- 启用/禁用定时任务
- 各地区爬取开关
- 爬取时间窗口设置
- 爬取失败重试次数

### 任务监控

系统提供任务执行日志和监控：
- 任务执行历史记录
- 执行成功率统计
- 异常告警通知
- 任务执行时长分析

---

## 💻 前端功能详解

### 看板主页

```
├── 顶部统计卡片区域
│   ├── 总新闻数统计
│   ├── 今日新增数量
│   ├── 昨日新增数量
│   ├── 活跃地区排名
│   └── 实时数据更新时间
├── 违规事项分布图（柱状图 + 折线图组合）
│   ├── 主要违规类型统计
│   ├── 可交互筛选
│   └── 数据导出功能
├── 案件查处趋势图（时间序列图）
│   ├── 按月统计数据
│   ├── 支持时间范围选择
│   └── 趋势预测功能
├── 地区分布排行榜（横向柱状图）
│   ├── 各地区案件数量
│   ├── 热力地图展示
│   └── 地区详情钻取
├── 最新通报案例滚动列表
│   ├── 最新案件信息
│   ├── 点击查看详情
│   └── 搜索和筛选功能
├── 导航和工具栏
│   ├── 数据筛选器
│   ├── 导出功能
│   ├── AI 客服入口
│   └── 用户设置
└── 底部信息栏
    ├── 系统状态
    ├── 数据更新时间
    └── 版权信息
```

### 交互功能

| 功能类别 | 具体功能 | 操作说明 |
|----------|----------|----------|
| 数据筛选 | 日期范围选择 | 使用日期选择器筛选数据范围 |
| 数据筛选 | 地区筛选 | 下拉选择特定地区数据 |
| 数据筛选 | 标签筛选 | 多选框选择特定违规类型 |
| 图表交互 | 图表缩放 | 鼠标滚轮或触摸手势缩放 |
| 图表交互 | 数据点查看 | 悬停查看详细数据信息 |
| 图表交互 | 数据钻取 | 点击图表进入更详细视图 |
| 报告导出 | 格式选择 | Word/Excel/PDF 三种格式 |
| 报告导出 | 自定义范围 | 选择特定时间范围导出 |
| 用户交互 | 实时搜索 | 搜索框快速查找新闻 |
| 用户交互 | AI 客服 | 点击右下角 AI 客服图标 |

### 响应式设计

- **桌面端**：充分利用大屏幕空间，显示完整的四象限布局
- **平板端**：调整为两列布局，保持主要功能可用
- **手机端**：采用单列布局，简化交互，突出核心功能

---

## 📍 访问地址

| 服务类型 | 地址 | 说明 | 认证要求 |
|----------|------|------|----------|
| 前端页面 | http://localhost:8000/ | 主看板界面 | 无需认证 |
| 后台管理 | http://localhost:8000/admin/ | Django Admin | 需要管理员权限 |
| API 接口 | http://localhost:8000/api/ | REST API | 部分接口需要认证 |
| API 文档 | http://localhost:8000/api/schema/swagger-ui/ | Swagger UI | 仅开发模式 |
| 3D 地图 | http://localhost:8000/shaanxi_3d_map.html | 3D 可视化地图 | 无需认证 |
| 健康检查 | http://localhost:8000/health/ | 系统健康状态 | 无需认证 |

---

## 📰 数据来源

### 主要数据源

- **陕西省纪委监委网站** (qinfeng.gov.cn) - 官方权威数据源
- **各地市分站**:
  - 西安市: http://xasjjw.xa.gov.cn/
  - 渭南市: http://www.wnjw.gov.cn/
  - 延安市: http://www.yasjjw.gov.cn/
  - 榆林市: http://www.sxyljjjc.gov.cn/
  - 汉中市: http://www.hzzq.gov.cn/
  - 安康市: http://www.akjjjc.gov.cn/
  - 商洛市: http://www.sljjjc.gov.cn/

### 数据更新频率

- **实时爬取**: 每4小时自动更新一次
- **人工验证**: 每日人工验证数据准确性
- **数据验证**: 自动数据质量检查

---

## 🏷️ 违规类型标签

系统自动识别的违规类型及关键词：

| 标签 | 关键词 | 识别规则 |
|------|--------|----------|
| 违规收受财物 | 礼品、礼金、有价证券、消费卡、购物卡、红包 | 包含任一关键词且上下文相关 |
| 违规接受宴请 | 宴请、聚餐、吃饭、招待、接待 | 与职务行为相关的描述 |
| 违规公款消费 | 公款旅游、公款娱乐、公款购物、公款消费 | 公款+消费行为的组合 |
| 违规使用公车 | 公车、私车公用、车辆使用、公务用车 | 公车私用相关描述 |
| 违规发放福利 | 福利、补贴、奖金、津贴、补助 | 违规发放相关描述 |
| 违规操办婚丧 | 婚丧、喜庆、宴席、庆典 | 大操大办性质的描述 |
| 违规发放津贴 | 津贴、补贴、加班费、补助费 | 违规发放的津贴类型 |
| 违规占用公物 | 占用、挪用、借用、私用 | 公物私用相关行为 |
| 失职渎职 | 失职、渎职、不作为、乱作为 | 职责履行不当的描述 |
| 其他违规 | 其他违规行为、违反纪律 | 未分类的违规行为 |

### 标签扩展机制

系统支持动态添加新的违规类型标签：
- 通过后台管理界面添加
- 支持关键词权重设置
- 支持正则表达式匹配

---

## 🔧 配置与部署

### 环境配置

#### 开发环境配置

```bash
# 克隆项目
git clone https://github.com/sgahch/Big-Data-Dashboard.git
cd Big-Data-Dashboard

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt

# 配置开发环境变量
cp .env.example .env
# 编辑 .env 文件，设置开发环境配置
```

#### 生产环境配置

```bash
# 使用 Gunicorn 部署
pip install gunicorn

# 启动命令
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 supervision.wsgi:application

# 或使用 Nginx 反向代理
# 配置 Nginx 代理到 Gunicorn
```

### 性能优化

#### 数据库优化

- 启用数据库索引，特别在新闻表的标题、日期、地区字段
- 配置数据库连接池
- 定期清理过期数据

#### 缓存策略

- 配置 Redis 缓存热点数据
- 设置合理的缓存过期时间
- 实现缓存预热机制

#### 静态资源优化

- 启用静态资源压缩
- 配置 CDN 加速
- 实现资源预加载

### 安全配置

#### Django 安全设置

```python
# settings.py 安全配置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True  # 生产环境
SESSION_COOKIE_SECURE = True  # 生产环境
CSRF_COOKIE_SECURE = True  # 生产环境
```

#### 数据库安全

- 使用强密码策略
- 限制数据库用户权限
- 定期备份数据

#### API 安全

- 启用 API 速率限制
- 使用 API 密钥认证
- 实现请求日志记录

---

## 🧪 测试与验证

### 单元测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test apps.news
python manage.py test apps.crawler
python manage.py test apps.stats

# 运行覆盖率测试
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### 数据验证

- **数据完整性检查**: 验证爬取数据的完整性
- **去重算法验证**: 确保重复数据正确识别
- **标签准确性验证**: 验证自动标签的准确性
- **API 响应验证**: 验证 API 接口响应格式

### 性能测试

- **并发访问测试**: 模拟多用户同时访问
- **大数据量测试**: 测试大数据量下的性能表现
- **长时间运行测试**: 验证系统稳定性

---

## 🚀 部署指南

### Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "supervision.wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_USER=supervision_user
      - DB_PASSWORD=your_password
      - DB_NAME=supervision
    depends_on:
      - db
      - redis

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: supervision
      MYSQL_USER: supervision_user
      MYSQL_PASSWORD: your_password
      MYSQL_ROOT_PASSWORD: root_password
    volumes:
      - db_data:/var/lib/mysql

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

volumes:
  db_data:
```

### 云平台部署

#### 部署到 Heroku

```bash
# 安装 Heroku CLI
# 创建应用
heroku create your-app-name

# 设置环境变量
heroku config:set DJANGO_SETTINGS_MODULE=supervision.settings
heroku config:set SECRET_KEY=your-secret-key

# 部署
git push heroku main

# 运行迁移
heroku run python manage.py migrate
```

#### 部署到 Vercel (仅前端)

项目已包含 `vercel.json` 配置文件，支持前端静态部署。

---

## 🔍 系统架构

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    前端层 (Frontend)                        │
├─────────────────────────────────────────────────────────────┤
│  ECharts 可视化  │  HTML/CSS/JS  │  响应式设计  │  AI 客服  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    API 网关 (API Gateway)                   │
├─────────────────────────────────────────────────────────────┤
│  路由分发  │  认证授权  │  限流熔断  │  日志监控            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    应用服务层 (Application)                 │
├─────────────────────────────────────────────────────────────┤
│ Django Web服务 │ 爬虫调度服务 │ 统计分析服务 │ AI集成服务   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    数据存储层 (Data Storage)                │
├─────────────────────────────────────────────────────────────┤
│  MySQL数据库  │  Redis缓存  │  文件存储  │  搜索引擎      │
└─────────────────────────────────────────────────────────────┘
```

### 数据流向

1. **数据采集流程**:
   ```
   目标网站 → HTTP请求 → 数据解析 → 数据清洗 → 存储到数据库
   ```

2. **数据分析流程**:
   ```
   数据库 → 统计计算 → 结果缓存 → API响应 → 前端展示
   ```

3. **用户请求流程**:
   ```
   用户浏览器 → API网关 → 应用服务 → 数据查询 → 响应返回
   ```

### 技术选型理由

- **Django**: 强大的ORM支持、完善的管理后台、丰富的生态
- **ECharts**: 优秀的可视化效果、良好的性能、丰富的图表类型
- **MySQL**: 数据一致性、复杂查询支持、成熟稳定
- **APScheduler**: 轻量级、易集成、支持多种调度方式
- **Redis**: 高性能缓存、会话存储、消息队列支持

---

## 📚 开发指南

### 代码规范

#### Python 代码规范

- 遵循 PEP 8 代码风格
- 使用 type hints 标注函数参数和返回值
- 保持函数和类的职责单一
- 编写单元测试覆盖核心逻辑

#### 前端代码规范

- 使用 ESLint 进行 JavaScript 代码检查
- CSS 类名使用 BEM 命名规范
- 组件保持单一职责
- 使用语义化 HTML 标签

### 新功能开发流程

1. **需求分析**: 确定功能需求和实现方案
2. **数据库设计**: 设计相关数据模型
3. **API 开发**: 实现后端 API 接口
4. **前端开发**: 实现前端交互和展示
5. **测试验证**: 编写测试用例并验证
6. **文档更新**: 更新相关文档

### 贡献代码

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## ❓ 常见问题

<details>
<summary>1. 数据库时区错误导致时间显示异常</summary>

确保 `settings.py` 中设置 `USE_TZ = False` 或正确配置时区：

```python
# supervision/settings.py
USE_TZ = False
TIME_ZONE = 'Asia/Shanghai'
```

或者在数据库连接中设置时区：

```python
# settings.py
DATABASES = {
    'default': {
        # ... 其他配置
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'autocommit': True,
        },
    }
}
```
</details>

<details>
<summary>2. 爬虫无法启动或频繁失败</summary>

检查以下配置：
- 数据库连接是否正常
- `crawl_config` 表中的配置是否正确
- 网络连接是否稳定
- 目标网站是否修改了结构

```bash
# 检查爬虫配置
python manage.py shell
from apps.crawler.models import CrawlConfig
config = CrawlConfig.objects.first()
print(config)
```

检查爬虫日志：
```bash
# 查看爬虫执行日志
python manage.py shell
from apps.crawler.models import CrawlTask
tasks = CrawlTask.objects.all().order_by('-created_at')[:10]
for task in tasks:
    print(f"Task {task.id}: {task.status}, {task.created_at}")
```
</details>

<details>
<summary>3. AI 客服无响应或响应缓慢</summary>

检查 `.env` 中的 `COZE_API_TOKEN` 是否有效：

```bash
# 测试 AI 服务连接
curl -X POST http://localhost:8000/api/ai/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "测试"}'
```

确保网络连接正常，并检查 API 频率限制。
</details>

<details>
<summary>4. PDF 导出失败</summary>

确保已正确安装 `xhtml2pdf` 及其依赖：

```bash
# 安装依赖
pip install xhtml2pdf
pip install reportlab

# 如遇问题，尝试升级
pip install --upgrade xhtml2pdf reportlab
```

检查是否安装了中文字体支持：

```python
# 在 settings.py 中配置
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimHei', 'path/to/simhei.ttf'))
```
</details>

<details>
<summary>5. 系统响应缓慢</summary>

性能优化建议：
- 配置 Redis 缓存热点数据
- 优化数据库查询，添加必要索引
- 启用 Gzip 压缩
- 优化静态资源加载

检查数据库性能：
```sql
-- 检查慢查询
SHOW PROCESSLIST;
-- 添加索引
ALTER TABLE news_news ADD INDEX idx_created_at (created_at);
ALTER TABLE news_news ADD INDEX idx_region (region_id);
ALTER TABLE news_news ADD INDEX idx_tags (tag_ids);
```
</details>

<details>
<summary>6. 定时任务不执行</summary>

检查 APScheduler 服务是否正常运行：

```bash
# 查看定时任务状态
python manage.py shell
from apps.crawler.scheduler import scheduler
print(scheduler.get_jobs())
print(f"Scheduler state: {scheduler.state}")
```

确保在启动应用时启动了调度器。
</details>

---

## 📈 性能指标

### 系统性能

- **页面加载时间**: < 2秒 (在标准网络条件下)
- **API 响应时间**: < 500ms (95%分位)
- **数据库查询时间**: < 200ms (复杂查询 < 1秒)
- **并发用户支持**: > 1000个同时在线用户
- **数据处理能力**: > 10万条记录/小时

### 资源使用

- **内存占用**: < 512MB (空闲状态)
- **CPU 使用率**: < 30% (常规操作)
- **存储空间**: 根据数据量动态增长

---

## 🔄 更新日志

### v3.0 - 最新版本
- 重构爬虫架构，提升稳定性
- 新增3D地图可视化功能
- 优化AI客服响应速度
- 改进数据去重算法
- 增强系统安全性

### v2.5 - 功能增强版
- 新增报告导出功能
- 优化数据可视化图表
- 改进定时任务管理
- 增加数据验证机制

### v2.0 - 核心功能版
- 实现完整的数据爬取系统
- 构建数据统计分析模块
- 集成AI客服功能
- 实现用户权限管理

### v1.0 - 基础版
- 搭建Django项目框架
- 实现基础爬虫功能
- 构建简单数据展示

---

## 🤝 贡献指南

### 开发环境设置

1. **克隆项目**:
   ```bash
   git clone https://github.com/sgahch/Big-Data-Dashboard.git
   cd Big-Data-Dashboard
   ```

2. **配置虚拟环境**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   venv\Scripts\activate  # Windows
   ```

3. **安装依赖**:
   ```bash
   pip install -r requirements-dev.txt  # 开发依赖
   ```

### 代码提交规范

- **提交信息格式**: `type(scope): description`
  - `type`: feat, fix, docs, style, refactor, test, chore
  - `scope`: 模块范围，如 crawler, news, stats
  - `description`: 简洁的描述

- **示例**:
  - `feat(news): 添加新闻搜索功能`
  - `fix(crawler): 修复爬虫超时问题`
  - `docs(readme): 更新部署说明`

### 测试要求

- 新功能必须包含相应的单元测试
- 修改核心功能需更新相关测试
- 确保所有测试用例通过后再提交

---

## 📄 许可证

本项目采用 MIT 许可证开源，详情请参阅 [LICENSE](LICENSE) 文件。

MIT License

Copyright (c) 2024 纪检监察大数据看板系统

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📞 联系方式

- 项目维护者：[@Ynchen](https://github.com/Ynchen)
- 项目地址：[https://github.com/sgahch/Big-Data-Dashboard](https://github.com/sgahch/Big-Data-Dashboard)
- 问题反馈：[GitHub Issues](https://github.com/sgahch/Big-Data-Dashboard/issues)
- 邮箱联系：[sgahch@github.com](mailto:sgahch@github.com)

---

<div align="center">

**如果本项目对您有帮助，请给个 ⭐ Star 支持一下！**

**持续更新中，欢迎贡献代码和提出建议！**

</div>