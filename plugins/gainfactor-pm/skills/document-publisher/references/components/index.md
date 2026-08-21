# 正文组件索引

只读取已选组件的参考，不批量读取本目录。

维护门户主题、组件样式或视觉门禁时读取 [`design-system`](design-system.md)；普通文档写作不需要读取。

| 阅读需求 | 组件 | 参考 |
|-|-|-|
| 标准正文、表格、提示、卡片、Tabs、文件树、类型表、图片缩放 | Markdown / Fumadocs | [`standard-mdx`](standard-mdx.md) |
| 带图标、稳定锚点和目录语义的标题 | `SectionHeading` | [`section-heading`](section-heading.md) |
| 画像章节的人物、处境、特征与短事实 | `PersonaBrief` | [`persona-brief`](persona-brief.md) |
| 紧凑扫描短字段 | `FieldList` | [`field-list`](field-list.md) |
| 线性过程及步骤内字段 | `Steps/Step` + `FieldList` | [`steps`](steps.md) |
| 眉题、标题、摘要与组合正文 | `Panel` | [`panel`](panel.md) |
| 多个并列分组 | `Board` | [`board`](board.md) |
| 可点击引用与来源索引 | `Citation` / `SourceIndex` / `Source` | [`citations`](citations.md) |
| 产品截图、截图画廊或步骤旁证据 | `Screenshot` / `ScreenshotGallery` / `EvidenceStep` | [`screenshots`](screenshots.md) |

精确横向比较优先 Markdown 表格；连续论证保留正文；复杂节点关系进入 [`visuals`](../visuals/index.md)；视觉叙事只有在确有收益时进入 [`infographic`](../infographic/index.md)。
