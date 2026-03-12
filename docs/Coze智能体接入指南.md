# Coze 智能体接入完整指南

## 📋 目录
- [1. 前置准备](#1-前置准备)
- [2. 获取智能体信息](#2-获取智能体信息)
- [3. 配置到项目中](#3-配置到项目中)
- [4. API调用说明](#4-api调用说明)
- [5. 切换智能体步骤](#5-切换智能体步骤)
- [6. 常见问题排查](#6-常见问题排查)
- [7. 附录：API测试工具](#7-附录api测试工具)

---

## 1. 前置准备

### 1.1 注册Coze账号
1. 访问 [Coze官网](https://www.coze.cn/)
2. 注册并登录账号
3. 进入控制台

### 1.2 创建或选择智能体
- **新建智能体**：在控制台点击"创建Bot"
- **使用现有智能体**：在"我的Bot"列表中选择

### 1.3 获取API访问权限
1. 进入 **个人设置** → **API密钥**
2. 点击 **生成新密钥**
3. 复制并保存密钥（格式：`pat_xxxxxxxxxxxxxx`）

⚠️ **重要**：API密钥只显示一次，请妥善保存！

---

## 2. 获取智能体信息

### 2.1 获取Bot ID

#### 方法1：从URL获取（推荐）
打开您的智能体编辑页面，URL格式如下：
```
https://www.coze.cn/space/[workspace_id]/bot/[bot_id]
                                              ^^^^^^^^
                                              这就是Bot ID
```

**示例**：
```
URL: https://www.coze.cn/space/123456/bot/7584642107525824539
Bot ID: 7584642107525824539
```

#### 方法2：通过API查询
使用以下curl命令获取Bot信息：
```bash
curl -X GET 'https://api.coze.cn/v1/bot/get_online_info?bot_id=YOUR_BOT_ID' \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**响应示例**：
```json
{
  "code": 0,
  "data": {
    "bot_id": "7584642107525824539",
    "name": "微信聊天机器人",
    "description": "和微信朋友聊天",
    "model_info": {
      "model_name": "豆包·1.5·Pro·32k"
    }
  }
}
```

### 2.2 需要记录的信息

| 参数名 | 说明 | 示例值 |
|--------|------|--------|
| `bot_id` | 智能体唯一标识 | `7584642107525824539` |
| `api_key` | API访问密钥 | `pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz` |
| `bot_name` | 智能体名称（可选） | `微信聊天机器人` |

---

## 3. 配置到项目中

### 3.1 修改配置常量

打开 `index.html` 文件，找到第 **404-408 行**：

```javascript
// ========== API配置常量 ==========
const COZE_BOT_ID = "7584642107525824539";  // ← 修改这里
const COZE_API_KEY = "pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz";  // ← 修改这里
const COZE_CHAT_URL = "https://api.coze.cn/open_api/v2/chat";  // ← 保持不变
const CRAWLER_API_URL = "http://localhost:5000/api/news";  // ← 保持不变
```

### 3.2 配置步骤

**步骤1**：替换 `COZE_BOT_ID`
```javascript
const COZE_BOT_ID = "YOUR_NEW_BOT_ID";  // 粘贴您的Bot ID
```

**步骤2**：替换 `COZE_API_KEY`
```javascript
const COZE_API_KEY = "YOUR_NEW_API_KEY";  // 粘贴您的API密钥
```

**步骤3**：保存文件并刷新浏览器

---

## 4. API调用说明

### 4.1 当前使用的API版本

本项目使用 **Coze v2 Chat API**（同步返回）

**API端点**：
```
POST https://api.coze.cn/open_api/v2/chat
```

### 4.2 请求格式

```javascript
{
  "conversation_id": "unique_conversation_id",  // 会话ID（可选）
  "bot_id": "7584642107525824539",              // 智能体ID
  "user": "web_user_1234567890",                // 用户ID
  "query": "用户输入的问题",                     // 用户消息
  "stream": false                                // 是否流式返回
}
```

### 4.3 响应格式

```json
{
  "messages": [
    {
      "role": "assistant",
      "type": "answer",
      "content": "AI的回复内容",
      "content_type": "text"
    },
    {
      "role": "assistant",
      "type": "follow_up",
      "content": "推荐的后续问题"
    }
  ],
  "conversation_id": "7584645248548536370",
  "code": 0,
  "msg": "success"
}
```

### 4.4 关键字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `messages` | Array | 消息列表 |
| `messages[].role` | String | 角色：`assistant`（AI）或 `user`（用户） |
| `messages[].type` | String | 消息类型：`answer`（回答）、`follow_up`（推荐问题）、`verbose`（调试信息） |
| `messages[].content` | String | 消息内容 |
| `conversation_id` | String | 会话ID（用于多轮对话） |

---

## 5. 切换智能体步骤

### 场景1：切换到纪检监察专用智能体

假设您创建了一个专门的"纪检监察知识库助手"：

**步骤1**：获取新智能体信息
- Bot ID: `7584999999999999999`（示例）
- API Key: 使用同一个账号的密钥即可

**步骤2**：修改配置
```javascript
const COZE_BOT_ID = "7584999999999999999";  // 新的Bot ID
const COZE_API_KEY = "pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz";  // 保持不变
```

**步骤3**：测试验证
- 刷新页面
- 在AI助手中输入测试问题
- 检查回复是否符合新智能体的设定

### 场景2：切换到不同账号的智能体

**步骤1**：获取新账号的API密钥
- 登录新的Coze账号
- 生成新的API密钥

**步骤2**：同时替换Bot ID和API Key
```javascript
const COZE_BOT_ID = "NEW_ACCOUNT_BOT_ID";
const COZE_API_KEY = "NEW_ACCOUNT_API_KEY";
```

---

## 6. 常见问题排查

### 问题1：AI一直显示"正在查询知识库"

**原因**：API请求失败或响应解析错误

**排查步骤**：
1. 按 `F12` 打开浏览器开发者工具
2. 切换到 **Console** 标签
3. 查看错误信息：
   ```
   ❌ Coze API错误响应: ...
   ```

**常见错误码**：
| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `401` | API密钥无效 | 检查 `COZE_API_KEY` 是否正确 |
| `404` | Bot不存在 | 检查 `COZE_BOT_ID` 是否正确 |
| `403` | 无权限访问 | 确认Bot已发布且API密钥有权限 |
| `429` | 请求频率过高 | 等待1分钟后重试 |

### 问题2：AI回复"抱歉，我暂时无法回答这个问题"

**原因**：响应中没有找到 `type: "answer"` 的消息

**解决方案**：
1. 查看Console中的完整响应：
   ```javascript
   console.log('✅ Coze API响应:', data);
   ```
2. 检查 `data.messages` 数组中是否有内容
3. 如果有其他类型的消息，可能需要调整解析逻辑

### 问题3：CORS跨域错误

**错误信息**：
```
Access to fetch at 'https://api.coze.cn/...' from origin 'null' has been blocked by CORS policy
```

**原因**：直接打开本地HTML文件（`file://` 协议）

**解决方案**：
使用本地服务器运行：
```bash
# 方法1：使用Python
python -m http.server 8000

# 方法2：使用Node.js
npx http-server

# 然后访问 http://localhost:8000/index.html
```

---

## 7. 附录：API测试工具

### 7.1 使用提供的测试脚本

项目中包含 `test_coze_api.py` 测试脚本：

```bash
# 安装依赖
pip install requests

# 运行测试
python test_coze_api.py
```

**脚本会自动测试**：
- ✅ 获取Bot信息
- ✅ v2 Chat API调用
- ✅ 响应解析

### 7.2 手动测试（curl命令）

#### 测试1：获取Bot信息
```bash
curl -X GET 'https://api.coze.cn/v1/bot/get_online_info?bot_id=YOUR_BOT_ID' \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

#### 测试2：发送对话消息
```bash
curl -X POST 'https://api.coze.cn/open_api/v2/chat' \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "bot_id": "YOUR_BOT_ID",
    "user": "test_user",
    "query": "你好",
    "stream": false
  }'
```

**预期响应**：
```json
{
  "messages": [
    {
      "role": "assistant",
      "type": "answer",
      "content": "你好！有什么可以帮助你的吗？"
    }
  ],
  "code": 0
}
```

---

## 📝 快速参考卡片

### 配置位置
```
文件：index.html
行号：404-408
```

### 必填参数
```javascript
COZE_BOT_ID   = "你的Bot ID"
COZE_API_KEY  = "你的API密钥"
```

### 测试命令
```bash
# 1. 测试API连接
python test_coze_api.py

# 2. 启动本地服务器
python -m http.server 8000

# 3. 访问页面
http://localhost:8000/index.html
```

---

## 🎯 最佳实践

1. **安全性**：
   - ❌ 不要将API密钥提交到公开的Git仓库
   - ✅ 使用环境变量或配置文件管理密钥
   - ✅ 定期轮换API密钥

2. **性能优化**：
   - 使用 `conversation_id` 保持多轮对话上下文
   - 设置合理的超时时间（建议30秒）
   - 对频繁请求做防抖处理

3. **用户体验**：
   - 显示加载状态（"正在查询知识库..."）
   - 使用打字机效果渲染回复
   - 提供友好的错误提示

---

**📞 技术支持**

- Coze官方文档：https://www.coze.cn/docs
- API参考：https://www.coze.cn/docs/developer_guides/coze_api_overview
- 问题反馈：在Coze控制台提交工单

---

**✅ 文档版本**：v1.0  
**最后更新**：2025-12-17  
**适用项目**：纪检监察大数据可视化平台

