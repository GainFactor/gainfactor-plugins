# 文档门户能力与格式

## 三层模型

1. **内容层**：`.md` / `.mdx`，保存完整正文、引用和资源关系。
2. **呈现层**：可选 `.portal.json`，只定义正文之前的重点视图。
3. **门户层**：导航、元数据、评审、搜索、版本与静态站点输出。

## 内容层能力

机器可读注册表位于 `../../assets/document-review-portal/portal-capabilities.json`。只有其中 `status: registered` 的工具才能写入交付文档；具体语法见 [工具目录与写法](tool-catalog.md)。

| 内容关系 | 首选写法 | 门户能力 |
|-|-|-|
| 段落、标题、列表、引用、表格、链接 | 标准 Markdown | 原生 |
| 代码与多语言示例 | fenced code / CodeBlock | 原生 |
| 流程、时序、状态、依赖、用户旅程 | `mermaid` fenced block | 已接入 Mermaid |
| 报告摘要、路线图、对比、层级和视觉故事 | AntV Infographic DSL | 已本地接入 `@antv/infographic@0.2.20` |
| 提示、限制、结论 | MDX Callout 或 admonition | Fumadocs 组件/插件 |
| 互斥视图、平台差异 | Tabs / Tab | Fumadocs 组件 |
| 操作步骤 | Steps 或带 `[step]` 标题 | Fumadocs remark plugin/组件 |
| 文档正文中的节点关系 | NodeGraph | 门户组件；简单可访问节点图，复杂拓扑优先 Mermaid |
| 整站页面关系 | Graph View | Fumadocs 官方示例，不是正文写入工具，未列入注册表 |
| 文件层级、接口类型、图片缩放 | Files、TypeTable、ImageZoom | 已注册 Fumadocs 组件 |
| 标题、状态、步骤和关键概念的图标补充 | `Icon` / AntV `icon` 字段 | 已本地接入完整 Lucide 图标集合 |
| 主体档案、紧凑字段、结构化步骤、可重复内容单元、通用分组展示 | Profile、InfoGrid、StructuredSteps、ContentPanel、GroupedBoard | 已注册通用报告组件；字段由业务 Skill 定义 |
| 任意交互或专用图形 | 自定义 MDX React 组件 | 扩展点，需在门户模板注册 |

优先使用语义最直接的表达。Mermaid 适合有节点和边的关系；精确字段比较仍用表格；不要为了“丰富”把连续正文拆成大量卡片。

## Portal Presentation v1

顶层：

```json
{"schemaVersion":1,"layout":"report","modules":[]}
```

`layout`：`document | report | reference`。已支持模块：

- `metrics`：少量关键数字或判断，`items: [{label,value}]`。
- `cards`：对象/方案/Persona 等同构条目，支持 `title`、`eyebrow`、`description`、`quote`、`fields`、`image`。
- `steps`：线性阶段或理想路径，`items: [{title?,content}]`。
- `callout`：一个关键结论或风险，支持 `tone: info | success | warning`。

卡片图片可写 `sourceImageAlt`。发布器会在导入后的 MDX 中，从标准 Markdown 图片 `![alt](src)` 和已注册的 `<Profile image={{ src, alt }} />` 图片声明中按相同 alt 找到已搬运的门户 URL，避免业务 Skill 预测资产路径。相同 alt 指向相同 src 时合并；相同 alt 指向不同 src 时映射有歧义，引用该 alt 的 presentation 校验失败，调用方必须改用唯一 alt。显式 `cards.image` 不依赖此映射。

正文层还能承载 Mermaid、Tabs 等复杂块；它们不必全部重复进 presentation manifest。未注册或标为实验性的工具不得由上游 Skill 写入正式文档。
