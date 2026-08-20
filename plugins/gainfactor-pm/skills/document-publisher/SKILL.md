---
name: document-publisher
description: Expose the GainFactor document portal's supported authoring capabilities and the workflows for creating, importing, validating, updating, and previewing final MDX portal documents. Use when another skill needs to choose standard Markdown syntax within MDX, MDX components, Mermaid, AntV Infographic, or portal presentation tools while constructing content, or when a completed portal document must be published or updated. This is a capability and workflow skill, not a semantic document converter.
---

# 文档门户能力与工作流

像 lark-cli 的文档 Skill 一样，对外说明门户能表达什么、应该怎样写、如何创建或更新。调用本 Skill 的业务 Skill 在构建内容时直接产出符合门户契约的最终 MDX、图形 DSL 和可选 Portal Presentation；标准 Markdown 语法可以嵌在 MDX 内，本 Skill 不把一份普通 Markdown 二次理解成业务报告。

## 必读参考

1. **表达设计 / 内容构建**：先读取 [表达决策框架](references/expression-design.md)，产出页面蓝图；再读取 [能力与格式](references/capabilities.md)、[工具目录与写法](references/tool-catalog.md) 和 [写入契约](references/authoring-contract.md)。使用 Profile、InfoGrid、StructuredSteps、ContentPanel 或 GroupedBoard 时读取 [通用报告组件](references/generic-report-components.md)；使用图标时读取 [Lucide 图标渠道与写法](references/lucide-icons.md)；选择 AntV Infographic 时，再读取 [官方 Infographic 语法规范](references/antv-infographic-syntax.md)。

最终交付始终直接写入 `.mdx`。本文所称“Markdown 降级”仅指：某个富组件不可用时，在**同一份最终 `.mdx`** 中改用标准 Markdown 语法表达；它不是独立 `.md` 文件、临时稿，也不是 Markdown→MDX 转换流程。
2. **创建 / 导入 / 更新 / 验证 / 预览**：读取 [发布工作流](references/publish-workflow.md)。

## 边界

- 本 Skill 定义通用格式、组件能力、选择规则和操作流程，不判断业务文档应该写哪些结论。
- 业务 Skill 负责文档体裁、内容结构、组件选择、图形 DSL 及 presentation manifest，并直接写出最终内容。
- `../../assets/document-review-portal/portal-capabilities.json` 是机器可读的唯一能力注册表；工具目录、格式校验器和门户组件注册必须与其一致。
- 最终 MDX 是完整、可独立阅读的正文来源；presentation manifest 是可选的首屏视图，不替代正文。
- 导入脚本只能机械处理 frontmatter、相对资源、清单和导航；不得按标题、文档类型或正文语义生成视觉模块。
- 校验器只能验证已写格式，不得补写、改写或推导内容。
- 同一 slug 表示更新，保留门户内其他文档和评审数据。

## 表达设计要求

调用方不能从“有什么组件”直接跳到“写哪个组件”。在写正文前，先按 `expression-design.md` 判断读者任务、信息关系、阅读层级与证据密度，并形成简短页面蓝图。蓝图决定正文结构、可视化位置和工具选择，但不改变业务结论。

页面蓝图是写作过程产物，不要求原样出现在最终文档。没有明确阅读收益时保留 Markdown；有表达需求但无已注册工具时记录能力缺口，不得用近似组件硬凑。
