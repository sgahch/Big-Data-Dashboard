# 智慧监督管理系统 - Bug分析报告

## 生成时间
2026-01-28

---

## 一、高优先级Bug（需要立即修复）

### 1.1 服务响应异常（502错误）🔴
**状态**: 待确认
**描述**: API服务返回502 Bad Gateway错误
**可能原因**:
- Django应用崩溃
- 数据库连接失败
- 内存不足
- APScheduler与Django冲突

**排查步骤**:
```bash
# 1. 检查Django进程
ps aux | grep python

# 2. 查看Django日志
python manage.py shell 2>&1

# 3. 检查数据库连接
python manage.py dbshell
```

**临时解决方案**:
```bash
# 重启Django服务
pkill -f "manage.py runserver"
python manage.py runserver 0.0.0.0:8000
```

---

## 二、中优先级Bug

### 2.1 News.save() 标签同步逻辑缺陷
**文件**: `apps/news/models.py` 第106-111行
```python
def save(self, *args, **kwargs):
    if self.pk:
        tags = self.tags.all()
        self.tag_names = ','.join([t.name for t in tags])
    super().save(*args, **kwargs)
```
**问题**:
- 新创建的新闻不会生成 tag_names
- M2M关系在save()后才生效

**修复方案**: 使用 Django signals

### 2.2 SQL注入风险
**文件**: `apps/news/views.py` 第84行
```python
limit = int(request.query_params.get('limit', 20))
```
**问题**: 未验证参数合法性

**修复方案**:
```python
try:
    limit = min(int(request.query_params.get('limit', 20)), 100)
except ValueError:
    limit = 20
```

### 2.3 XSS跨站脚本风险
**文件**: `index.html` 多处使用 innerHTML
**位置**: 第1494-1501行, 第1593-1605行, 第1842-1866行

**修复方案**:
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### 2.4 API Key暴露风险
**文件**: `index.html` 第915-916行
```javascript
const COZE_API_KEY = "cztei_ljQufsTRwIc73ibCixxHrYXzCgEgKJuNCFElA1OXP5s5GAp6llFKkAsfg82fRgFYU";
```

**修复方案**: 将API调用迁移到后端代理

### 2.5 调试模式安全隐患
**文件**: `supervision/settings.py` 第9行
```python
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')
```

**修复方案**: 默认关闭调试模式

### 2.6 跨域配置过于宽松
**文件**: `supervision/settings.py` 第100行
```python
CORS_ALLOW_ALL_ORIGINS = True
```

**修复方案**:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

### 2.7 认证权限配置过于宽松
**文件**: `supervision/settings.py` 第93-94行
```python
'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
```

**修复方案**: 根据实际需求调整权限

---

## 三、低优先级Bug

### 3.1 重复初始化问题
**文件**: `index.html` 第1002-1008行 vs 第1945-1962行

### 3.2 定时器未清理
**文件**: `index.html` 第1094行, 第1958-1961行

### 3.3 ECharts图表未销毁
**文件**: `index.html` 第1099行, 第1213行

### 3.4 聊天记录无限增长
**文件**: `index.html` 第1698-1716行

### 3.5 线程安全问题
**文件**: `apps/crawler/views.py` 第15-20行

### 3.6 爬虫无重试机制
**文件**: `apps/crawler/crawler.py` 第48行

---

## 四、性能问题

### 4.1 统计方法N+1查询
**文件**: `apps/news/views.py` 第178-190行

**修复方案**: 使用数据库聚合查询

### 4.2 requests连接未复用
**文件**: `apps/crawler/crawler.py` 第48行

**修复方案**: 使用requests.Session()

---

## 五、安全建议

| 问题 | 风险等级 | 建议 |
|------|----------|------|
| DEBUG模式开启 | 高 | 默认关闭 |
| CORS过于宽松 | 高 | 限制域名 |
| API Key暴露 | 高 | 后端代理 |
| 权限配置过松 | 高 | 启用认证 |
| XSS风险 | 中 | 输入转义 |
| SQL注入风险 | 中 | 参数验证 |
| 内存泄漏 | 低 | 清理定时器 |

---

## 六、测试脚本

### 6.1 API测试
```bash
python test_api.py
```

### 6.2 爬虫测试
```bash
python test_crawler.py
```

### 6.3 手动测试
```bash
# 测试连接
curl http://localhost:8000/api/news/

# 测试统计
curl http://localhost:8000/api/stats/dashboard/

# 测试爬虫状态
curl http://localhost:8000/api/crawl/status/
```

---

## 七、修复优先级

| 优先级 | Bug编号 | 问题描述 | 预计修复时间 |
|--------|---------|----------|--------------|
| P0 | 1.1 | 服务响应异常 | 立即 |
| P1 | 2.5 | 调试模式安全 | 5分钟 |
| P1 | 2.6 | 跨域配置 | 5分钟 |
| P1 | 2.3 | XSS风险 | 30分钟 |
| P2 | 2.1 | save()逻辑 | 1小时 |
| P2 | 2.2 | SQL注入 | 30分钟 |
| P2 | 2.4 | API Key | 2小时 |
| P3 | 3.1-3.6 | 其他问题 | 4小时 |

---

## 八、相关文件

- `test_api.py` - API测试脚本
- `test_crawler.py` - 爬虫测试脚本
- `docs/开发阶段记录.md` - 开发记录

---

*报告生成时间: 2026-01-28*
