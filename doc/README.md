# 纪检监察大数据可视化平台 - 使用说明

## 📋 项目简介

这是一个基于单页HTML的纪检监察数据可视化大屏系统，采用深空蓝/黑科技风格设计。

### 核心功能
- ✅ **违规事项分布**：南丁格尔玫瑰图展示6类违规数据
- ✅ **实时情报滚动**：自动爬取清风网最新通报并滚动显示
- ✅ **案件查处统计**：3D渐变柱状图展示月度数据
- ✅ **AI智能助手**：集成Coze智能体，支持纪检知识问答

---

## 🚀 快速启动

### 方案1：仅查看前端效果（使用Mock数据）

**直接双击打开 `index.html` 即可！**

- 图表和AI助手会使用预置的Mock数据
- 滚动列表显示示例通报信息
- AI对话功能已配置好Coze API，可直接使用

---

### 方案2：启用真实爬虫数据（推荐）

#### 步骤1：安装Python环境
确保已安装 **Python 3.7+**，在命令行输入：
```bash
python --version
```

#### 步骤2：启动爬虫服务
**双击运行 `启动爬虫服务.bat`**

或手动执行：
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python crawler_server.py
```

服务启动后会显示：
```
清风网爬虫服务已启动
API地址: http://localhost:5000/api/news
```

#### 步骤3：打开前端页面
双击 `index.html`，右上角的滚动列表会自动加载爬虫数据。

---

## 🔧 API配置说明

### Coze AI 配置（已配置完成）

在 `index.html` 第 404-408 行：
```javascript
const COZE_BOT_ID = "7584642107525824539";
const COZE_API_KEY = "pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz";
const COZE_CHAT_URL = "https://api.coze.cn/open_api/v2/chat";
const CRAWLER_API_URL = "http://localhost:5000/api/news";
```

**✅ 已使用您提供的Coze智能体信息配置完成！**

#### 切换到其他智能体

如需切换到不同的智能体（如纪检监察专用助手），请参考：

📖 **[智能体切换快速参考.md](./智能体切换快速参考.md)** - 3分钟快速切换指南
📖 **[Coze智能体接入指南.md](./Coze智能体接入指南.md)** - 完整接入流程
📖 **[Coze智能体技术实现文档.md](./Coze智能体技术实现文档.md)** - 技术实现细节

**快速切换步骤**：
1. 获取新智能体的Bot ID和API Key
2. 修改 `index.html` 第404-405行
3. 刷新浏览器测试

### 爬虫服务配置（增强版 v2.0）

**目标网站**：https://www.qinfeng.gov.cn/scdc.htm

**支持的分类**：
- **省管干部**：执纪审查、党纪政务处分
- **其他干部**：执纪审查、党纪政务处分

**启动方式**：
```bash
# 方式1: 使用批处理文件（推荐）
启动爬虫服务.bat

# 方式2: 命令行启动
python crawler_server.py
```

**API接口**：
- 获取所有新闻：`http://localhost:5000/api/news`
- 按分类获取：`http://localhost:5000/api/news?category=省管干部`
- 按子分类获取：`http://localhost:5000/api/news?category=省管干部&subcategory=执纪审查`
- 分类列表：`http://localhost:5000/api/categories`
- 健康检查：`http://localhost:5000/health`

**测试爬虫**：
```bash
python test_crawler.py
```

**详细文档**：参见 [爬虫服务使用说明.md](./爬虫服务使用说明.md)

---

## 📊 功能详解

### 1. 左上角 - 违规事项分布
- **图表类型**：ECharts南丁格尔玫瑰图
- **数据来源**：Mock数据（可在代码中替换为真实数据）
- **交互效果**：Hover放大 + 发光阴影

### 2. 右上角 - 实时情报滚动
- **数据来源**：爬虫服务（自动爬取清风网）
- **滚动速度**：30秒完整循环
- **交互效果**：
  - Hover暂停滚动
  - 点击标题跳转到原文

### 3. 左下角 - 案件查处统计
- **图表类型**：ECharts 3D柱状图
- **数据维度**：12个月案件数量
- **视觉特效**：青紫渐变 + 顶部数值标签

### 4. 右下角 - AI智能助手
- **AI引擎**：Coze智能体（微信聊天机器人）
- **功能**：
  - 纪检知识问答
  - 政策解读
  - 案例分析
- **特性**：
  - 打字机效果回复
  - 深色科技风界面
  - 错误提示友好

---

## 🛠️ 故障排查

### 问题1：AI助手无法回复
**原因**：Coze API配置错误或网络问题

**解决方案**：
1. 检查 `COZE_API_KEY` 是否正确
2. 打开浏览器开发者工具（F12），查看Console错误信息
3. 确认网络可访问 `https://api.coze.cn`

### 问题2：滚动列表显示Mock数据
**原因**：爬虫服务未启动

**解决方案**：
1. 运行 `启动爬虫服务.bat`
2. 确认终端显示 "清风网爬虫服务已启动"
3. 刷新 `index.html` 页面

### 问题3：爬虫服务启动失败
**原因**：Python依赖未安装

**解决方案**：
```bash
pip install flask flask-cors requests beautifulsoup4 lxml
```

---

## 📁 文件结构

```
大数据看板/
├── index.html                          # 主页面（包含所有前端代码）
├── crawler_server.py                   # 爬虫服务后端（增强版v2.0）
├── requirements.txt                    # Python依赖列表
├── 启动爬虫服务.bat                    # 一键启动脚本
├── test_coze_api.py                    # Coze API测试脚本
├── test_crawler.py                     # 爬虫服务测试脚本（⭐新增）
├── README.md                           # 本说明文档
├── 爬虫服务使用说明.md                 # 爬虫服务详细文档（⭐新增）
├── 智能体切换快速参考.md               # 快速切换指南
├── Coze智能体接入指南.md               # 完整接入流程
├── Coze智能体技术实现文档.md           # 技术实现细节
├── bot_config_template.js              # 多智能体配置模板
├── 文档导航.md                         # 文档索引
└── final_review_gate.py                # 开发辅助脚本
```

---

## 🎨 自定义修改

### 修改配色方案
在 `index.html` 的 `<style>` 标签中修改：
```css
--primary-color: #00D2FF;   /* 主色调（青色） */
--secondary-color: #9933FF; /* 辅助色（紫色） */
--bg-color: #0B0F2A;        /* 背景色（深蓝） */
```

### 修改Mock数据
在 `index.html` 第 410-437 行修改：
- `mockViolationsData`：违规事项数据
- `mockCasesData`：案件统计数据
- `mockNewsData`：滚动列表数据

---

## 📞 技术支持

如有问题，请检查：
1. 浏览器控制台（F12 → Console）的错误信息
2. 爬虫服务终端的日志输出
3. 网络连接状态

---

**🎉 祝您使用愉快！**

