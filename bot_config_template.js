/**
 * Coze 智能体配置模板
 * 
 * 使用说明：
 * 1. 复制此文件内容到 index.html 的配置区域（第404-408行）
 * 2. 根据需要选择不同的智能体配置
 * 3. 修改 CURRENT_BOT 变量即可快速切换
 * 
 * 最后更新：2025-12-17
 */

// ========== 智能体配置库 ==========
const BOT_CONFIGS = {
    /**
     * 配置1：微信聊天机器人（当前使用）
     * 功能：日常聊天、情感陪伴
     * 适用场景：通用对话、轻松交流
     */
    'wechat_chat': {
        bot_id: '7584642107525824539',
        api_key: 'pat_XAXCUN8690km9Kp0sXJbiYzxZkNOB3Bm4taHyDc29FcMkXHLg1akdTwXZIUTnTxz',
        name: '微信聊天机器人',
        description: '和微信朋友轻松聊天',
        welcome_message: '嗨！我来陪你聊天啦，以后咱们可以畅聊各种话题😃。',
        model: '豆包·1.5·Pro·32k',
        suggested_questions: [
            '给我分享个最近遇到的趣事呗。',
            '要是工作压力大咋缓解呀？',
            '你有啥宝藏歌推荐不？'
        ]
    },

    /**
     * 配置2：纪检监察知识库助手（推荐用于本项目）
     * 功能：党纪法规解读、案例分析、政策咨询
     * 适用场景：纪检监察业务咨询
     */
    'discipline_inspection': {
        bot_id: 'YOUR_DISCIPLINE_BOT_ID',  // ← 替换为您的纪检监察Bot ID
        api_key: 'YOUR_DISCIPLINE_API_KEY',  // ← 替换为对应的API密钥
        name: '纪检监察智能助手',
        description: '专业的纪检监察知识库',
        welcome_message: '您好！我是纪检监察智能助手，可以为您解答纪检监察相关问题。请问有什么可以帮助您的？',
        model: '豆包·1.5·Pro·32k',
        suggested_questions: [
            '什么是八项规定？',
            '如何举报违纪行为？',
            '党员受到警告处分的影响期是多久？'
        ]
    },

    /**
     * 配置3：法律顾问助手
     * 功能：法律咨询、法规解读
     * 适用场景：法律问题咨询
     */
    'legal_advisor': {
        bot_id: 'YOUR_LEGAL_BOT_ID',  // ← 替换为您的法律顾问Bot ID
        api_key: 'YOUR_LEGAL_API_KEY',  // ← 替换为对应的API密钥
        name: '法律顾问助手',
        description: '专业法律咨询服务',
        welcome_message: '您好！我是法律顾问助手，可以为您提供法律咨询服务。请问有什么可以帮助您的？',
        model: '豆包·1.5·Pro·32k',
        suggested_questions: [
            '劳动合同纠纷如何处理？',
            '什么是诉讼时效？',
            '如何申请法律援助？'
        ]
    },

    /**
     * 配置4：政策解读助手
     * 功能：政策文件解读、政策咨询
     * 适用场景：政府政策查询
     */
    'policy_advisor': {
        bot_id: 'YOUR_POLICY_BOT_ID',  // ← 替换为您的政策解读Bot ID
        api_key: 'YOUR_POLICY_API_KEY',  // ← 替换为对应的API密钥
        name: '政策解读助手',
        description: '政府政策专业解读',
        welcome_message: '您好！我是政策解读助手，可以为您解读各类政府政策文件。请问有什么可以帮助您的？',
        model: '豆包·1.5·Pro·32k',
        suggested_questions: [
            '最新的税收优惠政策有哪些？',
            '如何申请创业补贴？',
            '社保缴纳基数如何计算？'
        ]
    },

    /**
     * 配置5：自定义智能体模板
     * 功能：根据您的需求自定义
     * 适用场景：特定业务场景
     */
    'custom_bot': {
        bot_id: 'YOUR_CUSTOM_BOT_ID',  // ← 替换为您的自定义Bot ID
        api_key: 'YOUR_CUSTOM_API_KEY',  // ← 替换为对应的API密钥
        name: '自定义智能体',
        description: '根据需求自定义功能',
        welcome_message: '您好！我是智能助手，请问有什么可以帮助您的？',
        model: '豆包·1.5·Pro·32k',
        suggested_questions: [
            '问题1',
            '问题2',
            '问题3'
        ]
    }
};

// ========== 当前使用的智能体（修改这里即可快速切换）==========
const CURRENT_BOT = 'wechat_chat';  // ← 修改为上面配置库中的任意key

// ========== 自动加载配置（无需修改）==========
const currentConfig = BOT_CONFIGS[CURRENT_BOT];

if (!currentConfig) {
    console.error(`❌ 配置错误：找不到智能体配置 "${CURRENT_BOT}"`);
    alert(`配置错误：智能体 "${CURRENT_BOT}" 不存在，请检查 CURRENT_BOT 设置`);
}

// 导出配置常量（用于API调用）
const COZE_BOT_ID = currentConfig.bot_id;
const COZE_API_KEY = currentConfig.api_key;
const COZE_CHAT_URL = "https://api.coze.cn/open_api/v2/chat";
const CRAWLER_API_URL = "http://localhost:5000/api/news";

// 导出智能体信息（用于UI显示）
const BOT_NAME = currentConfig.name;
const BOT_WELCOME_MSG = currentConfig.welcome_message;
const BOT_SUGGESTED_QUESTIONS = currentConfig.suggested_questions;

// ========== 配置验证（开发环境使用）==========
console.log('✅ 当前智能体配置:', {
    name: BOT_NAME,
    bot_id: COZE_BOT_ID,
    api_key: COZE_API_KEY.substring(0, 10) + '...',  // 只显示前10位
    model: currentConfig.model
});

// ========== 使用示例 ==========
/*
// 在 initAIChat() 函数中使用欢迎语：
container.innerHTML = `
    <div class="chat-messages" id="chat-messages">
        <div class="chat-bubble ai-bubble">
            <div class="bubble-content">
                ${BOT_WELCOME_MSG}
            </div>
        </div>
    </div>
    ...
`;

// 显示推荐问题（可选）：
BOT_SUGGESTED_QUESTIONS.forEach(question => {
    const btn = document.createElement('button');
    btn.textContent = question;
    btn.onclick = () => {
        document.getElementById('chat-input').value = question;
        sendMessage();
    };
    container.appendChild(btn);
});
*/

