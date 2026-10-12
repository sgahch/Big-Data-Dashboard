/**
 * demos/index.html 冒烟测试
 * 目的：在 Node 环境用最小 DOM 桩件执行页面内联脚本，
 *       验证无语法/运行时错误，并检查核心算法输出是否合理。
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const base = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(base, 'demos', 'index.html'), 'utf8');
const dataJs = fs.readFileSync(path.join(base, 'demos', 'data', 'cases.js'), 'utf8');

// 抽取最后一个内联 <script>（主逻辑块）
const blocks = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!blocks.length) {
  console.error('未找到内联脚本');
  process.exit(1);
}
const code = blocks[blocks.length - 1];

// ── 最小 DOM 桩件 ──────────────────────────────
function makeEl(id) {
  const el = {
    id, value: '', textContent: '', innerHTML: '',
    className: '', scrollTop: 0, scrollHeight: 0,
    children: [],
    appendChild(c) { this.children.push(c); },
    querySelector: () => makeEl('sub')
  };
  return el;
}
const store = {};
const documentStub = {
  getElementById(id) { return store[id] || (store[id] = makeEl(id)); },
  createElement(tag) { return makeEl(tag); },
  querySelector() { return makeEl('q'); }
};

const sandbox = {
  document: documentStub,
  window: {},
  console,
  Set, Map, Math, JSON, Number, String, Array, Object,
  setTimeout,
  parseInt, escapeHtmlLike: null
};
sandbox.globalThis = sandbox;

// 预设文本域默认值，逼近浏览器真实初始状态
store.caseInput = makeEl('caseInput');
store.caseInput.value = '某市生态环境局分局局长【姓名脱敏】接受监察调查';

// 先加载数据脚本
vm.createContext(sandbox);
try {
  vm.runInContext(dataJs, sandbox, { filename: 'cases.js' });
} catch (e) {
  console.error('数据脚本执行失败:', e.message);
  process.exit(1);
}
console.log('数据加载条数 =', sandbox.window.CASE_DATA.length);

// 再执行页面逻辑
try {
  vm.runInContext(code, sandbox, { filename: 'index.html<inline>' });
} catch (e) {
  console.error('页面脚本执行失败:', e.message, '\n', e.stack.split('\n').slice(0, 4).join('\n'));
  process.exit(1);
}
console.log('页面脚本执行: OK');

// ── 校验输出 ────────────────────────────────────
const check = (name, val, ok) => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}: ${val}`);
  return ok;
};
let allOk = true;
allOk &= check('案件总数', store.c1.textContent, String(store.c1.textContent) === String(sandbox.window.CASE_DATA.length));
allOk &= check('覆盖地市数', store.c2.textContent, Number(store.c2.textContent) > 0);
allOk &= check('问题类型数', store.c3.textContent, Number(store.c3.textContent) > 0);
allOk &= check('时间跨度', store.c4.textContent, String(store.c4.textContent).includes('–'));
allOk &= check('打标覆盖率', store.c5.textContent, /%$/.test(String(store.c5.textContent)));
allOk &= check('地区热度表已渲染', store.heatTable.innerHTML.length, store.heatTable.innerHTML.includes('<table'));
allOk &= check('地区图表已渲染', store.heatChart.innerHTML.length, store.heatChart.innerHTML.includes('<svg'));
allOk &= check('趋势图已渲染', store.trendChart.innerHTML.length, store.trendChart.innerHTML.includes('<svg'));
allOk &= check('趋势说明含预测', store.trendText.innerHTML.length, store.trendText.innerHTML.includes('斜率'));
allOk &= check('判定结果已渲染', store.classifyOut.innerHTML.length, store.classifyOut.innerHTML.includes('判定结果'));

// 抽样验证分类判定合理性
// const 顶层声明不会挂到 vm 全局，需在上下文中取值
const ENRICHED = vm.runInContext('ENRICHED', sandbox);
console.log('\n--- 自动判定抽样 ---');
ENRICHED.slice(0, 6).forEach(d => {
  console.log(`  ${d.date || '无日期'} | ${d.region} | → ${d._auto} | ${(d.title || '').slice(0, 42)}`);
});
const dist = {};
ENRICHED.forEach(d => { dist[d._auto] = (dist[d._auto] || 0) + 1; });
console.log('\n自动判定分布:', JSON.stringify(dist));

// 验证问答意图
console.log('\n--- 自然语言问答抽样 ---');
['哪个地区最多', '2025年有多少起', '执纪审查多少', '预测明年趋势'].forEach(q => {
  const a = sandbox.answer(q);
  console.log(`  Q: ${q}\n  A: ${String(a).split('\n')[0]}`);
});

console.log('\n' + (allOk ? '=== 冒烟测试全部通过 ===' : '=== 存在失败项 ==='));
process.exit(allOk ? 0 : 1);
