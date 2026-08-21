# 最终 MDX 构建工作流

仅在新建完整文档、重构整篇文档或需要选择多种表达方式时读取。业务 Skill 负责事实与结论；本工作流只帮助把已经形成的内容直接写成最终 `.mdx`。

## 决策顺序

1. 用一句话说明读者看完后要完成的判断或行动。
2. 识别真正影响阅读的关系：连续论证、精确比较、步骤、层级、网络、证据或警告。
3. 默认使用标准 Markdown；只有富表达能明显降低理解、比较、定位或核验成本时才进入 [`components/index`](components/index.md)、[`visuals/index`](visuals/index.md) 或 [`infographic/index`](infographic/index.md)。
4. 直接写最终 `.mdx`，不创建等待二次转换的普通 Markdown 中间稿。
5. 需要首屏摘要时再读取 [`presentation`](presentation.md)。
6. 完成后进入 [`validation`](validation.md)。

## 何时记录页面蓝图

完整报告、整篇重构或存在多个合理表达候选时，记录简短蓝图；局部标题、字段、引用和文案更新不需要重新制作。

```yaml
audience: 谁阅读
readerTasks: [需要完成的判断]
readingPath: executive-first | sequential | reference | exploratory
sections:
  - purpose: 本段帮助读者完成什么
    relation: prose | comparison | sequence | hierarchy | network | evidence | warning
    expression: markdown | table | component | mermaid | infographic
    reason: 为什么比正文更容易理解
    fallback: 同一最终 MDX 内的标准 Markdown 回退
```

## 选择原则

- 连续论证、背景、限制和完整证据保留为正文。
- 精确核验优先表格；流程、关系和状态统一使用 Mermaid。
- 组件表达关系而非文档类型；不要因为内容叫“画像”或“竞品分析”就机械套模板。
- 首屏只压缩正文已有信息，不创造新结论。
- 图标辅助识别，不代替标题、状态、证据或结论。
- 无法证明富表达更易读时保留 Markdown。

每个视觉块前说明为什么值得看，后面给出结论或证据入口；连续视觉块必须承担不同阅读任务。
