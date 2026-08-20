# PRODUCT_METRICS 门户模块与增量写入

开始写门户正文前读取本文件，并同时遵守 `$document-publisher` 的当前能力注册表与发布流程。正文直接写成最终 MDX；发布器不负责从普通 Markdown 推导业务模块。

## 写入属性

```text
source: docs/Product-Metrics-{product-slug}.mdx
presentation: docs/Product-Metrics-{product-slug}.portal.json
type: Product-Metrics
collection: 产品文档
layout: report
slug: {product-slug}-metrics
```

同一产品的三次阶段交付复用相同文件和 slug。每次更新后验证并从实际路由读回；不得生成三份阶段文档，也不得覆盖门户内其他文档。

## 页面表达基线

| 正文内容 | 阅读任务 | 首选表达 | 回退 |
|---|---|---|---|
| 指标摘要、最终判断、关键缺口 | 快速判断 | `Callout` 加紧凑表格 | 引用块加表格 |
| 产品价值链、多边价值交集 | 理解顺序和汇合 | Mermaid | 编号列表 |
| 相似产品、候选、门禁 | 精确比较与核验 | Markdown 表格 | 分项小节 |
| 指标公式 | 精确复算 | 公式正文加口径表 | 字段列表 |
| 指标驱动树 | 理解层级和因果假设 | Mermaid | 嵌套列表 |
| 过程、虚荣、底线、伪底线指标 | 精确核对 | Markdown 表格 | 分项小节 |
| 最不能发生的事 | 识别风险 | warning `Callout` | 警告引用块 |
| 测量与行动契约 | 执行和查阅 | Markdown 表格 | 分项列表 |

默认不使用 Cards、Tabs、Steps、NodeGraph、TypeTable 或 AntV Infographic。候选和口径需要同时精确比较，价值链与驱动树由 Mermaid 更直接表达；只有出现新的阅读任务且能说明收益时才改变选择。

图形前说明为什么需要看，图后概括关键结论。表格负责精确，Mermaid 负责关系，正文负责解释；三者不机械重复。隐藏推理过程不写入门户，只写候选、证据、取舍、门禁结果和已确认结论。

## 正文规则

- 只使用一个一级标题，章节按 artifact schema 顺序出现；
- 未开始阶段不写空标题、空表格或“待补充”占位；
- `Callout` 只用于主要结论、不可接受失败和高影响缺口；
- Mermaid 使用 fenced `mermaid`，不直接写 `<Mermaid>`；
- 关键关系必须在图附近有正文概括；
- 证据链接直接指向来源，官方披露、公开经营指标和分析推断分开；
- 不使用任意 HTML、脚本、内联样式、未注册 JSX 或远程运行时资源。

## Portal Presentation

首屏只使用两个稳定 module：

1. `metric-summary`：`metrics`，压缩本次任务、主要指标、当前阶段，以及完成后的首要杠杆和首要底线；
2. `metric-status`：`callout`，说明当前结论或最重要缺口。

不要把完整公式、候选比较、门禁表或证据放入首屏，也不要再用 Cards 或 Steps 重复正文。

```json
{
  "schemaVersion": 1,
  "layout": "report",
  "modules": [
    {
      "id": "metric-summary",
      "type": "metrics",
      "title": "指标体系摘要",
      "items": [
        {"label": "指标任务", "value": "长期产品指标体系"},
        {"label": "主要指标", "value": "已确认指标名称"},
        {"label": "当前阶段", "value": "主要指标已确认"}
      ]
    },
    {
      "id": "metric-status",
      "type": "callout",
      "title": "当前状态",
      "tone": "info",
      "content": "主要指标已确认，过程指标与底线指标仍待定义。"
    }
  ]
}
```

后续阶段只更新相同 module ID：过程指标确认后增加首要杠杆；全部完成后增加首要底线，无缺口时使用 `success`；存在基线、数据源、责任人或阈值缺口时使用 `warning` 并明确 `Draft` 限制。manifest 只能重组正文已有信息。

## 三次增量更新

### 第一次：主要指标确认

写入正文 0–4 节，创建 presentation：`Status: draft`，`Stage: primary-metric-confirmed`。

### 第二次：过程指标确认

更新摘要与 presentation，增加正文 5–6 节：`Status: draft`，`Stage: process-metrics-confirmed`。

### 第三次：底线指标确认

更新摘要与 presentation，增加正文 7–9 节。全部门禁通过时使用 `confirmed / complete`；仍有执行缺口时使用 `draft / complete-with-gaps`。

每次更新前验证最终 MDX 和 `.portal.json`，更新后从实际门户路由读回标题、阶段、主要指标、关键表格和首屏模块。自动写入不自动启动预览服务。
