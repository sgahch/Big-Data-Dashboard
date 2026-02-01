# 纪检监察大数据看板系统

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**基于 Django + ECharts 的纪检监察数据爬取、分析与可视化系统**

[功能特性](#功能特性) • [快速开始](#快速开始) • [API文档](#api接口文档) • [演示环境](#演示环境)

</div>

---

## 📊 功能特性

### 🔍 数据采集

| 功能 | 描述 |
|------|------|
| 自动爬虫 | 定时爬取陕西各地市清风网新闻数据 |
| 智能去重 | 自动过滤重复新闻，避免数据冗余 |
| 智能打标签 | 自动根据关键词识别违规类型 |

### 📈 数据分析

| 功能 | 描述 |
|------|------|
| 违规事项分布 | 按违规类型统计，展示各类违规占比 |
| 案件查处趋势 | 按月份统计案件数量，分析变化趋势 |
| 地区分布统计 | 展示各地区新闻发布量排名 |
| 实时数据更新 | 仪表盘展示今日数据概览 |

### 🤖 AI 智能客服

| 功能 | 描述 |
|------|------|
| Coze AI 集成 | 基于大模型的智能问答系统 |
| 数据分析解读 | 可向 AI 咨询数据分析结果 |

### 📑 报告导出

| 格式 | 描述 |
|------|------|
| Word 报告 | 生成规范化 Word 文档报告 |
| Excel 报告 | 导出多 sheet 数据表格 |
| PDF 报告 | 生成专业 PDF 格式报告 |

---

## 🛠️ 技术栈

<div align="left">

| 分类 | 技术 |
|------|------|
| 后端框架 | Django 4.2 + Django REST Framework |
| 数据库 | MySQL 8.0 + Redis（可选缓存）|
| 爬虫技术 | Requests + BeautifulSoup + lxml + APScheduler |
| 前端技术 | HTML5 + ECharts 可视化 + Font Awesome 图标 |
| AI 集成 | Coze API |
| 报告生成 | python-docx + openpyxl + xhtml2pdf |

</div>

---

## 📁 项目结构

```
.
├── supervision/          # Django 项目配置
│   ├── settings.py       # 项目配置
│   ├── urls.py           # 路由配置
│   └── wsgi.py
├── apps/                 # 应用模块
│   ├── news/            # 新闻管理模块
│   │   ├── models.py    # News, Region, Tag 模型
│   │   ├── views.py     # 新闻 API 接口
│   │   ├── crawler.py   # 爬虫核心逻辑
│   │   └── urls.py
│   ├── crawler/         # 爬虫调度模块
│   │   ├── scheduler.py # APScheduler 定时任务
│   │   └── models.py    # 爬虫配置模型
│   ├── stats/           # 统计分析模块
│   │   ├── views.py     # 统计 API
│   │   └── report.py    # 报告生成器
│   └── users/           # 用户管理模块
│       ├── views.py     # 用户 API + AI 客服
│       └── urls.py
├── templates/           # HTML 模板
├── static/              # 静态文件
├── index.html           # 主前端页面
├── requirements.txt     # Python 依赖
├── manage.py            # Django 管理脚本
├── start.bat            # Windows 启动脚本
└── .env                 # 环境变量配置
```

---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- MySQL 8.0
- Windows / Linux / macOS

### 1. 克隆项目

```bash
git clone https://your-repo-url.git
cd 大数据看板
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
pip install -r requirements.txt
```

### 4. 配置数据库

确保 MySQL 已启动，并创建数据库：

```sql
CREATE DATABASE supervision CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 配置环境变量

复制 `.env.example` 为 `.env` 并修改：

```env
# 数据库配置
DB_NAME=supervision
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Coze AI 配置（可选）
COZE_API_TOKEN=your_api_token
COZE_BOT_ID=your_bot_id

# Django 配置
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
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
print('初始化完成')
"

# 创建超级管理员
python manage.py createsuperuser
```

### 7. 启动服务

```bash
# 方式一：使用启动脚本（Windows）
start.bat

# 方式二：直接运行
python manage.py runserver 0.0.0.0:8000
```

---

## 📖 API 接口文档

### 新闻管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/news/` | GET | 新闻列表（分页、筛选） |
| `/api/news/<id>/` | GET | 新闻详情 |
| `/api/news/force-crawl/` | POST | 手动触发爬取 |
| `/api/news/search/` | GET | 搜索新闻 |

### 统计分析

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stats/dashboard/` | GET | 仪表盘数据 |
| `/api/stats/violations/` | GET | 违规事项分布 |
| `/api/stats/cases/` | GET | 案件查处统计 |
| `/api/stats/regions/` | GET | 地区统计 |
| `/api/stats/tags/` | GET | 标签统计 |
| `/api/stats/weekly/` | GET | 周统计 |
| `/api/stats/articles/` | GET | 文章管理统计 |

### 报告导出

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stats/report/` | GET | 预览报告数据 |
| `/api/stats/report/` | POST | 生成并下载报告 |

> **报告类型参数**：`type=word` / `type=excel` / `type=pdf`

### AI 客服

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/chat/` | POST | AI 聊天对话 |
| `/api/ai/health/` | GET | AI 服务健康检查 |

### 用户管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/users/` | GET | 用户列表 |
| `/api/users/me/` | GET | 当前用户信息 |
| `/api/users/groups/` | GET | 用户组列表 |
| `/api/users/roles/` | GET | 角色配置（只读）|

---

## ⏰ 定时任务

### 默认调度

| 任务 | 周期 | 描述 |
|------|------|------|
| 周期爬取 | 每 4 小时 | 自动爬取所有地区 |
| 每日汇总 | 每天 8:00 | 执行额外爬取任务 |

### 后台管理配置

访问 `/admin/crawler/crawlconfig/` 可修改爬虫配置：
- 爬取间隔时间
- 启用/禁用定时任务
- 各地区爬取开关

---

## 💻 前端功能

### 看板主页

```
├── 顶部统计卡片
│   ├── 总新闻数
│   ├── 今日新增
│   ├── 昨日新增
│   └── 活跃地区
├── 违规事项分布图（柱状图 + 折线图）
├── 案件查处趋势图
├── 地区分布排行榜
└── 最新通报案例滚动列表
```

### 操作说明

| 功能 | 操作方式 |
|------|----------|
| 日期筛选 | 使用日期选择器筛选数据范围 |
| 报告导出 | 点击"导出报告"按钮选择格式 |
| AI 客服 | 点击右下角 AI 客服图标 |

---

## 📍 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端页面 | http://localhost:8000/ | 主看板界面 |
| 后台管理 | http://localhost:8000/admin/ | Django Admin |
| API 接口 | http://localhost:8000/api/ | REST API |

---

## 📰 数据来源

- **清风网** (qinfeng.gov.cn) - 陕西省纪委监委网站
- 各地市分站：西安、渭南、延安、榆林、汉中、安康、商洛等

---

## 🏷️ 违规类型标签

系统自动识别的违规类型：

| 标签 | 关键词 |
|------|--------|
| 违规收受财物 | 礼品、礼金、有价证券、消费卡 |
| 违规接受宴请 | 宴请、聚餐、吃饭 |
| 违规公款消费 | 公款旅游、公款娱乐、公款购物 |
| 违规使用公车 | 公车、私车公用、车辆使用 |
| 违规发放福利 | 福利、补贴、奖金 |
| 违规操办婚丧 | 婚丧、喜庆、宴席 |
| 违规发放津贴 | 津贴、补贴、加班费 |
| 违规占用公物 | 占用、挪用、借用 |
| 失职渎职 | 失职、渎职、不作为 |
| 其他违规 | 其他违规行为 |

---

## ❓ 常见问题

<details>
<summary>1. 数据库时区错误</summary>

确保 `settings.py` 中设置 `USE_TZ = False`

```python
# supervision/settings.py
USE_TZ = False
```
</details>

<details>
<summary>2. 爬虫无法启动</summary>

检查数据库连接和 `crawl_config` 表中的配置

```bash
# 检查配置
python manage.py shell
from apps.crawler.models import CrawlConfig
print(CrawlConfig.objects.first())
```
</details>

<details>
<summary>3. AI 客服无响应</summary>

检查 `.env` 中的 `COZE_API_TOKEN` 是否有效

```bash
# 测试 AI 服务
curl http://localhost:8000/api/ai/health/
```
</details>

<details>
<summary>4. PDF 导出失败</summary>

确保已安装 `xhtml2pdf`：

```bash
pip install xhtml2pdf
```
</details>

---

## 🤝 贡献指南

1. Fork 本项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证开源，详情请参阅 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

- 项目维护者：[@Ynchen](https://github.com/Ynchen)
- 问题反馈：[GitHub Issues](https://github.com/Ynchen/大数据看板/issues)

---

<div align="center">

**如果本项目对您有帮助，请给个 ⭐ Star 支持一下！**

</div>
