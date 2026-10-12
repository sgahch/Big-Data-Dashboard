# 廉智通项目开发记录

## 项目概述
**廉智通** - 纪检监察工作管理平台
- 前端：Vue 3 + TypeScript + Ant Design Vue 4.x
- 后端：Django 4.2 + DRF (Python)
- 认证：JWT (Simple JWT)

---

## 第一阶段：API 服务层与页面数据对接
**时间**：2026-01-28

### 完成内容

#### 1. API 请求层 (`src/api/request.ts`)
- Axios 实例配置（baseURL、timeout、headers）
- JWT Token 管理（access_token、refresh_token）
- 请求拦截器（自动附加 Authorization）
- 响应拦截器（401 自动刷新 Token、错误提示）
- 路由守卫（未登录跳转登录页）

#### 2. API 服务模块
| 文件 | 功能 |
|------|------|
| `user.ts` | 用户登录、认证服务 |
| `report.ts` | 信访举报 CRUD、受理、转办 |
| `case.ts` | 案件管理、进度、证据管理 |
| `clue.ts` | 线索处置、分配、初核 |
| `supervision.ts` | 监督执纪服务 |
| `regulation.ts` | 政策法规服务 |
| `message.ts` | 消息通知服务 |

#### 3. 页面数据对接
| 页面 | 状态 | 说明 |
|------|------|------|
| 登录页 | ✅ | 对接 JWT 认证 |
| 信访举报 | ✅ | 真实 API 数据 |
| 线索处置 | ✅ | 真实 API 数据 |

### 修复的问题
- `src/api/case.ts` 导入语句中文乱码问题

### 运行状态
| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:5177/ |
| 后端 | http://localhost:8001/ |
| 演示账号 | admin / admin123 |

---

## 第二阶段：完善剩余页面数据对接
**时间**：2026-01-28（继续）

### 完成内容

#### 页面数据对接
| 页面 | 状态 | 说明 |
|------|------|------|
| 案件立案 | ✅ | 对接真实 API，分页、筛选、CRUD |
| 监督检查 | ✅ | 检查计划、任务列表、统计功能 |
| 政策法规 | ✅ | 法规库 CRUD、筛选、导入导出 |

### 技术改进
- 统一使用 `onMounted` + `watch` 实现数据初始化和筛选监听
- 统一使用 `computed` 处理数据格式化
- 统一分页参数传递 `page` 和 `page_size`
- 统一错误处理使用 `message.error()`

---

## 第三阶段：审理与结案功能开发
**时间**：2026-01-28

### 完成内容

#### 1. 后端模型扩展
| 模型 | 功能 |
|------|------|
| `Trial` | 案件审理记录（受理编号、案件关联、审理期限、审理意见等） |
| `Conclusion` | 结案报告（结案编号、处分类型、执行状态、归档状态等） |

#### 2. 后端序列化器和视图
- `TrialSerializer` / `TrialCreateSerializer` - 审理记录序列化
- `ConclusionSerializer` / `ConclusionCreateSerializer` - 结案报告序列化
- `TrialViewSet` - 审理 CRUD API
- `ConclusionViewSet` - 结案报告 CRUD API

#### 3. 前端 API 服务扩展
- `case.ts` 新增类型定义（Trial, Conclusion, TrialStatus, ExecutionStatus, ConclusionType）
- 新增 API 方法（getTrials, createTrial, changeTrialStatus, getConclusions, createConclusion, updateConclusion）

#### 4. 页面数据对接
| 页面 | 状态 | 说明 |
|------|------|------|
| 调查取证 | ✅ | 真实 API 数据 |
| 案件审理 | ✅ | 真实 API 数据，支持状态流转（开始审理、审结） |
| 结案报告 | ✅ | 真实 API 数据，支持归档功能 |

### 技术改进
- 统一使用 `onMounted` + `watch` 实现数据初始化和筛选监听
- 统一使用 `computed` 处理数据格式化
- 审理页面支持按状态筛选（待审理、审理中、已审结）
- 结案页面支持按执行状态和归档状态筛选

---

## 第四阶段：待续...
