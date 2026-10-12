# 给 AI 的 3D 地图搭建提示词（简洁版）

## 一句话提示词

```
请使用 ECharts GL 创建一个 3D 地图，包含自动旋转、城市标记点击跳转功能，
使用双层标记系统（透明大热区 + 可见标记）解决点击难题。
```

## 完整提示词

```
请帮我创建一个基于 ECharts GL 的 3D 地图可视化页面：

【核心需求】
1. 使用 ECharts 5.x + ECharts GL 2.x
2. 地图数据：阿里云 DataV GeoJSON API
3. 自动旋转 + 鼠标交互（拖拽、缩放）
4. 点击城市标记跳转到指定链接

【关键技术】
1. 双层标记系统：
   - 第一层：透明大圆（symbolSize: 200, opacity: 0.001）负责捕捉点击
   - 第二层：可见 pin 标记（symbolSize: 30）负责视觉展示

2. 点击判断：
   - 使用 ZRender 的 mousedown/mouseup 事件
   - 时间差 < 300ms = 点击，否则 = 拖拽
   - mousemove 记录当前悬停城市

3. 防弹窗拦截：
   - 创建隐藏 <a> 标签
   - 设置 target='_blank'
   - 模拟点击

【地图配置】
- 省份：陕西省（行政区划代码：610000）
- 城市：西安、宝鸡、咸阳、渭南、铜川、延安、榆林、汉中、安康、商洛
- GeoJSON: https://geo.datav.aliyun.com/areas_v3/bound/610000_full.json

【样式要求】
- 背景透明（可嵌入 iframe）
- 3D 立体效果 + 光照阴影
- 不同区域不同高度和颜色
- 悬停高亮显示

请提供完整的 HTML 代码，包含所有 CDN 引用。
```

## 核心代码片段

### 1. 双层标记系统

```javascript
series: [
    // 第一层：隐形大热区
    {
        type: 'scatter3D',
        coordinateSystem: 'geo3D',
        symbol: 'circle',
        symbolSize: 200,  // 超大
        itemStyle: { color: '#fff', opacity: 0.001 },  // 透明
        silent: false,
        data: cities.map(c => ({ name: c.name, value: [...c.coord, 3] }))
    },
    // 第二层：可见标记
    {
        type: 'scatter3D',
        coordinateSystem: 'geo3D',
        symbol: 'pin',
        symbolSize: 30,
        itemStyle: { color: '#ea4335' },
        label: { show: true },
        data: cities.map(c => ({ name: c.name, value: [...c.coord, 15] }))
    }
]
```

### 2. 点击事件处理

```javascript
let activeRegion = '';
let mouseDownTime = 0;

chart.on('mousemove', params => {
    if (params.seriesType === 'scatter3D') {
        activeRegion = params.name;
    }
});

chart.getZr().on('mousedown', () => {
    mouseDownTime = Date.now();
});

chart.getZr().on('mouseup', () => {
    if (Date.now() - mouseDownTime < 300 && activeRegion) {
        handleClick(activeRegion);
    }
});
```

### 3. 防弹窗拦截跳转

```javascript
function handleClick(cityName) {
    const link = document.createElement('a');
    link.href = cityLinks[cityName];
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
```

## 快速配置

### 更换地图区域

```javascript
// 行政区划代码
// 100000 = 全国
// 110000 = 北京
// 310000 = 上海
// 440000 = 广东
// 610000 = 陕西

const geoJsonUrl = 'https://geo.datav.aliyun.com/areas_v3/bound/610000_full.json';
```

### 添加城市

```javascript
const cities = {
    '城市名': {
        coord: [经度, 纬度],  // 百度地图拾取
        url: '跳转链接'
    }
};
```

### 调整样式

```javascript
const config = {
    hotspotSize: 200,      // 热区大小（越大越容易点击）
    markerSize: 30,        // 标记大小
    markerColor: '#ea4335', // 标记颜色
    rotateSpeed: 1.5       // 旋转速度
};
```

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| 点击不灵敏 | 增大 hotspotSize 到 300-500 |
| 地图加载失败 | 检查行政区划代码是否正确 |
| 如何获取坐标 | 百度地图拾取：https://api.map.baidu.com/lbsapi/getpoint/ |
| 禁用自动旋转 | 设置 `viewControl.autoRotate: false` |

## 完整示例

参考文件：
- `docs/3d_map_template.html` - 完整可用模板
- `shaanxi_3d_map.html` - 陕西省实际案例

## 技术亮点

✅ **双层标记系统** - 解决3D地图点击难题  
✅ **智能点击判断** - 区分点击和拖拽  
✅ **防弹窗拦截** - 确保链接正常打开  
✅ **配置化设计** - 易于定制和扩展  
✅ **纯前端实现** - 无需后端支持  

---

**使用建议**：直接复制 `3d_map_template.html`，修改配置区域即可使用！

