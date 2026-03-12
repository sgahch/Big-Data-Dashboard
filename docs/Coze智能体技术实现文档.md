# Coze 智能体技术实现详解

## 📋 文档概述

本文档详细说明了在"纪检监察大数据可视化平台"中集成Coze智能体的技术实现细节，包括代码结构、API调用流程、错误处理机制等。

---

## 1. 架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端页面 (index.html)                 │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 违规事项图表 │  │ 实时情报列表 │  │ 案件统计图表 │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│  ┌───────────────────────────────────────────────┐    │
│  │          AI智能助手 (Coze集成)                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │    │
│  │  │ 聊天界面  │  │ API调用层 │  │ 响应解析  │   │    │
│  │  └──────────┘  └──────────┘  └──────────┘   │    │
│  └───────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTPS
┌─────────────────────────────────────────────────────────┐
│              Coze API (api.coze.cn)                     │
│  ┌─────────────────────────────────────────────┐       │
│  │  Bot: 微信聊天机器人 (ID: 7584642...)        │       │
│  │  Model: 豆包·1.5·Pro·32k                    │       │
│  │  Knowledge Base: (可选)                     │       │
│  └─────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### 1.2 核心组件

| 组件名 | 文件位置 | 功能 |
|--------|---------|------|
| **配置层** | `index.html` 行404-408 | 存储API密钥和Bot ID |
| **UI层** | `index.html` 行690-717 | 聊天界面渲染 |
| **业务逻辑层** | `index.html` 行719-820 | 消息发送、接收、解析 |
| **工具函数层** | `index.html` 行822-865 | 打字机效果、消息管理 |

---

## 2. 代码实现详解

### 2.1 配置层

**位置**：`index.html` 第 404-408 行

```javascript
// ========== API配置常量 ==========
const COZE_BOT_ID = "7584642107525824539";
const COZE_API_KEY = "pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz";
const COZE_CHAT_URL = "https://api.coze.cn/open_api/v2/chat";
const CRAWLER_API_URL = "http://localhost:5000/api/news";
```

**设计说明**：
- 使用常量存储配置，便于统一管理和切换
- `COZE_CHAT_URL` 使用v2 API（同步返回），避免轮询复杂度
- 所有配置集中在文件顶部，方便快速定位

---

### 2.2 UI初始化

**位置**：`index.html` 第 690-717 行

```javascript
function initAIChat() {
    const container = document.getElementById('ai-chat-container');
    
    // 生成唯一会话ID（用于多轮对话）
    conversationId = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    container.innerHTML = `
        <div class="chat-messages" id="chat-messages">
            <div class="chat-bubble ai-bubble">
                <div class="bubble-content">
                    您好！我是纪检监察智能助手，可以为您解答纪检监察相关问题。请问有什么可以帮助您的？
                </div>
            </div>
        </div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" id="chat-input" placeholder="请输入您的问题..." />
            <button class="chat-send-btn" id="chat-send-btn" onclick="sendMessage()">
                <i class="fas fa-paper-plane"></i> 发送
            </button>
        </div>
    `;
    
    // 回车发送
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}
```

**关键设计**：
1. **会话ID生成**：`conversationId` 用于保持多轮对话上下文
2. **欢迎语**：预置AI欢迎消息，提升用户体验
3. **快捷键支持**：回车键发送消息

---

### 2.3 消息发送核心逻辑

**位置**：`index.html` 第 719-820 行

```javascript
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    // 1. 添加用户消息到界面
    addMessage('user', message);
    input.value = '';

    // 2. 显示加载状态
    const loadingId = addMessage('ai', '<span class="loading-dots">正在查询知识库</span>');

    try {
        // 3. 调用Coze API
        const response = await fetch(COZE_CHAT_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${COZE_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: conversationId,  // 多轮对话上下文
                bot_id: COZE_BOT_ID,
                user: 'web_user_' + Date.now(),
                query: message,
                stream: false  // 非流式返回
            })
        });

        // 4. 错误处理
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Coze API错误响应:', errorText);
            throw new Error(`API返回错误: ${response.status}`);
        }

        // 5. 解析响应
        const data = await response.json();
        console.log('✅ Coze API响应:', data);
        
        let aiReply = '';
        
        // 6. 提取AI回复
        if (data.messages && Array.isArray(data.messages)) {
            const answerMsg = data.messages.find(msg => 
                msg.role === 'assistant' && msg.type === 'answer'
            );
            
            if (answerMsg && answerMsg.content) {
                aiReply = answerMsg.content;
            } else {
                const firstAssistant = data.messages.find(msg => msg.role === 'assistant');
                aiReply = firstAssistant?.content || '';
            }
        }
        
        if (!aiReply) {
            console.error('❌ 无法解析AI回复，完整响应:', data);
            aiReply = '抱歉，我现在有点忙，请稍后再试～';
        }
        
        // 7. 移除加载状态，显示AI回复（打字机效果）
        removeMessage(loadingId);
        typewriterEffect(aiReply);

    } catch (error) {
        // 8. 异常处理
        console.error('发送消息失败:', error);
        removeMessage(loadingId);
        addMessage('ai', '⚠️ 连接服务器失败，请检查网络配置或稍后再试。');
    }
}
```

**流程图**：
```
用户输入消息
    ↓
显示用户消息气泡
    ↓
显示"正在查询知识库"加载状态
    ↓
发送POST请求到Coze API
    ↓
┌─────────────────┐
│  响应成功？      │
└─────────────────┘
    ↓ Yes              ↓ No
解析messages数组    显示错误提示
    ↓
找到type="answer"的消息
    ↓
移除加载状态
    ↓
打字机效果显示AI回复
```

---

### 2.4 响应解析策略

**核心代码**：
```javascript
// 策略1：优先查找type为"answer"的消息
const answerMsg = data.messages.find(msg => 
    msg.role === 'assistant' && msg.type === 'answer'
);

// 策略2：如果没有answer类型，获取第一条assistant消息
if (!answerMsg) {
    const firstAssistant = data.messages.find(msg => msg.role === 'assistant');
    aiReply = firstAssistant?.content || '';
}

// 策略3：兜底处理
if (!aiReply) {
    aiReply = '抱歉，我现在有点忙，请稍后再试～';
}
```

**为什么需要多策略？**
- Coze API可能返回多种类型的消息（`answer`, `follow_up`, `verbose`）
- 不同Bot配置可能导致响应结构差异
- 确保在各种情况下都能给用户友好的反馈

---

### 2.5 打字机效果实现

**位置**：`index.html` 第 822-850 行

```javascript
function typewriterEffect(text) {
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ai-bubble';
    
    const content = document.createElement('div');
    content.className = 'bubble-content';
    bubble.appendChild(content);
    
    document.getElementById('chat-messages').appendChild(bubble);
    scrollToBottom();
    
    let index = 0;
    const speed = 30; // 每个字符显示间隔（毫秒）
    
    function type() {
        if (index < text.length) {
            content.textContent += text.charAt(index);
            index++;
            scrollToBottom();
            setTimeout(type, speed);
        }
    }
    
    type();
}
```

**技术要点**：
- 使用递归 `setTimeout` 实现逐字显示
- 每次添加字符后自动滚动到底部
- 速度设置为30ms，平衡流畅度和可读性

---

## 3. API详细说明

### 3.1 请求参数完整说明

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `conversation_id` | String | 否 | 会话ID，用于多轮对话 | `conv_1734567890_abc123` |
| `bot_id` | String | 是 | 智能体ID | `7584642107525824539` |
| `user` | String | 是 | 用户唯一标识 | `web_user_1734567890` |
| `query` | String | 是 | 用户输入的问题 | `什么是八项规定？` |
| `stream` | Boolean | 否 | 是否流式返回（默认false） | `false` |

### 3.2 响应结构完整说明

```json
{
  "messages": [
    {
      "role": "assistant",           // 角色：assistant/user
      "type": "answer",               // 类型：answer/follow_up/verbose
      "content": "AI的回复内容",      // 消息内容
      "content_type": "text",         // 内容类型：text/image/card
      "reasoning_content": ""         // 推理过程（可选）
    },
    {
      "role": "assistant",
      "type": "follow_up",
      "content": "推荐的后续问题",
      "content_type": "text"
    }
  ],
  "conversation_id": "7584645248548536370",  // 会话ID
  "code": 0,                                  // 状态码：0=成功
  "msg": "success"                            // 状态消息
}
```

### 3.3 消息类型说明

| type值 | 说明 | 是否显示 | 用途 |
|--------|------|---------|------|
| `answer` | AI的正式回答 | ✅ 是 | 主要回复内容 |
| `follow_up` | 推荐的后续问题 | ⚠️ 可选 | 引导用户继续对话 |
| `verbose` | 调试信息 | ❌ 否 | 开发调试用 |

---

## 4. 错误处理机制

### 4.1 错误分类

```javascript
try {
    // API调用
} catch (error) {
    // 分类处理
    if (error.message.includes('401')) {
        // 认证失败
        showError('API密钥无效，请检查配置');
    } else if (error.message.includes('404')) {
        // Bot不存在
        showError('智能体不存在，请检查Bot ID');
    } else if (error.message.includes('429')) {
        // 请求过于频繁
        showError('请求过于频繁，请稍后再试');
    } else {
        // 通用错误
        showError('连接服务器失败，请检查网络配置');
    }
}
```

### 4.2 用户友好提示

| 错误场景 | 技术错误 | 用户提示 |
|---------|---------|---------|
| API密钥错误 | `401 Unauthorized` | "API密钥无效，请联系管理员" |
| Bot不存在 | `404 Not Found` | "智能体配置错误，请联系技术支持" |
| 网络超时 | `TimeoutError` | "网络连接超时，请检查网络后重试" |
| 响应解析失败 | `JSON Parse Error` | "服务器响应异常，请稍后再试" |

---

## 5. 性能优化

### 5.1 防抖处理（建议添加）

```javascript
let sendTimeout;
function sendMessage() {
    clearTimeout(sendTimeout);
    sendTimeout = setTimeout(() => {
        // 实际发送逻辑
    }, 300);  // 300ms防抖
}
```

### 5.2 请求超时控制

```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000);  // 30秒超时

const response = await fetch(COZE_CHAT_URL, {
    signal: controller.signal,
    // ... 其他配置
});

clearTimeout(timeoutId);
```

---

## 6. 安全建议

### 6.1 API密钥保护

**❌ 不安全的做法**：
```javascript
// 直接硬编码在前端代码中（当前实现）
const COZE_API_KEY = "pat_xxxxx";
```

**✅ 推荐做法**：
```javascript
// 方案1：通过后端代理
const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message })
});

// 方案2：使用环境变量（需构建工具支持）
const COZE_API_KEY = process.env.COZE_API_KEY;
```

### 6.2 输入验证

```javascript
function sendMessage() {
    const message = input.value.trim();
    
    // 长度限制
    if (message.length > 2000) {
        alert('消息长度不能超过2000字符');
        return;
    }
    
    // 敏感词过滤（示例）
    const forbiddenWords = ['违禁词1', '违禁词2'];
    if (forbiddenWords.some(word => message.includes(word))) {
        alert('消息包含敏感内容');
        return;
    }
    
    // 继续发送...
}
```

---

## 7. 调试技巧

### 7.1 启用详细日志

在 `sendMessage()` 函数中添加：
```javascript
console.log('📤 发送请求:', {
    bot_id: COZE_BOT_ID,
    user: 'web_user_' + Date.now(),
    query: message
});

console.log('📥 收到响应:', data);
console.log('💬 提取的回复:', aiReply);
```

### 7.2 使用浏览器Network面板

1. 打开开发者工具（F12）
2. 切换到 **Network** 标签
3. 筛选 **Fetch/XHR** 请求
4. 找到 `api.coze.cn` 的请求
5. 查看 **Headers**、**Payload**、**Response**

---

## 8. 扩展功能建议

### 8.1 多轮对话历史

```javascript
let chatHistory = [];

function sendMessage() {
    // 添加到历史
    chatHistory.push({
        role: 'user',
        content: message,
        timestamp: Date.now()
    });
    
    // 发送时携带历史（可选）
    body: JSON.stringify({
        // ...
        chat_history: chatHistory.slice(-10)  // 最近10条
    })
}
```

### 8.2 语音输入支持

```javascript
function startVoiceInput() {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'zh-CN';
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('chat-input').value = transcript;
    };
    
    recognition.start();
}
```

---

## 📚 参考资源

- **Coze官方文档**：https://www.coze.cn/docs
- **API参考**：https://www.coze.cn/docs/developer_guides/chat_v2
- **错误码说明**：https://www.coze.cn/docs/developer_guides/error_codes

---

## 9. 切换智能体快速指南

### 9.1 准备工作清单

在切换智能体前，请准备以下信息：

- [ ] 新智能体的Bot ID
- [ ] 对应的API密钥
- [ ] 新智能体的功能说明（用于更新欢迎语）
- [ ] 测试问题列表（验证切换成功）

### 9.2 切换步骤（5分钟完成）

**步骤1**：备份当前配置
```javascript
// 在index.html中注释掉当前配置
/*
const COZE_BOT_ID = "7584642107525824539";  // 旧配置：微信聊天机器人
const COZE_API_KEY = "pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz";
*/
```

**步骤2**：填入新配置
```javascript
// 新配置：纪检监察知识库助手
const COZE_BOT_ID = "YOUR_NEW_BOT_ID";
const COZE_API_KEY = "YOUR_NEW_API_KEY";
```

**步骤3**：更新欢迎语（可选）
找到 `initAIChat()` 函数中的欢迎语（约第697行）：
```javascript
<div class="bubble-content">
    您好！我是纪检监察智能助手，可以为您解答纪检监察相关问题。请问有什么可以帮助您的？
    <!-- 根据新智能体的功能修改此处 -->
</div>
```

**步骤4**：测试验证
1. 保存文件并刷新浏览器
2. 在AI助手中输入测试问题
3. 检查回复是否符合新智能体的设定
4. 查看浏览器Console确认无错误

### 9.3 多智能体配置管理（高级）

如果需要频繁切换多个智能体，可以使用配置对象：

```javascript
// 智能体配置库
const BOT_CONFIGS = {
    'wechat_chat': {
        bot_id: '7584642107525824539',
        api_key: 'pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz',
        name: '微信聊天机器人',
        welcome: '嗨！我来陪你聊天啦～'
    },
    'discipline_inspection': {
        bot_id: 'YOUR_DISCIPLINE_BOT_ID',
        api_key: 'YOUR_DISCIPLINE_API_KEY',
        name: '纪检监察知识库',
        welcome: '您好！我是纪检监察智能助手，可以为您解答纪检监察相关问题。'
    },
    'legal_advisor': {
        bot_id: 'YOUR_LEGAL_BOT_ID',
        api_key: 'YOUR_LEGAL_API_KEY',
        name: '法律顾问助手',
        welcome: '您好！我是法律顾问助手，可以为您提供法律咨询服务。'
    }
};

// 当前使用的智能体（只需修改这一行即可切换）
const CURRENT_BOT = 'wechat_chat';

// 自动加载配置
const COZE_BOT_ID = BOT_CONFIGS[CURRENT_BOT].bot_id;
const COZE_API_KEY = BOT_CONFIGS[CURRENT_BOT].api_key;
const BOT_WELCOME_MSG = BOT_CONFIGS[CURRENT_BOT].welcome;
```

---

## 10. 常见场景示例

### 场景1：切换到纪检监察专用智能体

**需求**：将通用聊天机器人替换为专门的纪检监察知识库助手

**配置示例**：
```javascript
const COZE_BOT_ID = "7584888888888888888";  // 纪检监察Bot
const COZE_API_KEY = "pat_YourDisciplineInspectionKey";
```

**欢迎语**：
```
您好！我是纪检监察智能助手，专注于：
✅ 党纪法规解读
✅ 违纪案例分析
✅ 举报流程指导
✅ 廉政政策咨询

请问有什么可以帮助您的？
```

**测试问题**：
- "什么是八项规定？"
- "如何举报违纪行为？"
- "党员受到警告处分的影响期是多久？"

---

### 场景2：切换到多语言客服助手

**配置示例**：
```javascript
const COZE_BOT_ID = "7584999999999999999";  // 多语言客服Bot
const COZE_API_KEY = "pat_YourMultilingualKey";
```

**欢迎语**：
```
Hello! 您好! こんにちは!
我是多语言智能客服，支持中文、英文、日文服务。
How can I help you today?
```

---

## 11. 故障排查流程图

```
AI无法正常回复
    ↓
打开浏览器Console (F12)
    ↓
┌─────────────────────────────┐
│ 是否有红色错误信息？         │
└─────────────────────────────┘
    ↓ Yes                  ↓ No
查看错误码              检查响应数据
    ↓                       ↓
401 → 检查API_KEY      messages数组为空？
404 → 检查BOT_ID           ↓ Yes
429 → 等待1分钟        Bot可能未正确配置
CORS → 使用本地服务器      ↓
    ↓                   登录Coze检查Bot状态
修复配置后刷新页面
    ↓
重新测试
```

---

**文档版本**：v1.0
**最后更新**：2025-12-17
**维护者**：技术团队

