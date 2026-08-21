# 标准 Markdown 与 Fumadocs 组件

优先使用语义直接的标准 Markdown：段落、标题、列表、引用、链接和精确表格。使用 JSX 组件时源文件必须为 `.mdx`。

| 需求 | 能力 |
|-|-|
| 代码 | fenced code；复杂容器用 `CodeBlock` / `Pre` |
| 2–6 个同构入口 | `Cards` / `Card` |
| 单个结论、风险或限制 | `Callout` |
| 同一主题下互斥视图 | `Tabs` / `Tab` |
| 简短线性步骤 | `Steps` / `Step` |
| 文件目录 | `Files` / `Folder` / `File` |
| 类型或接口字段 | `TypeTable` |
| 一张普通说明图片 | 裸 Markdown 图片或 `ImageZoom` |
| 带图号、图注、证据编号的产品截图 | `Screenshot`；多图与旅程证据见 [`screenshots`](screenshots.md) |

裸 Markdown 图片会被限制在正文与视口范围内，保持原始比例并使用 `object-fit: contain`；它不提供图号、统一说明区或证据校验。Cards 不承载长篇分析；必须同时对照的内容不放入 Tabs；分支流程不用 Steps；多图证据集不要伪装成一张 ImageZoom。精确字段与属性以门户锁定的 Fumadocs 组件类型为准。
