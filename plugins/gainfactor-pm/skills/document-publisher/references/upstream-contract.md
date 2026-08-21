# 上游业务 Skill 集成契约

仅在创建或维护会调用 `$document-publisher` 的业务 Skill 时读取。

上游 Skill 必须直接交付：

1. 可独立阅读、无需发布器二次理解的最终源文件；纯标准 Markdown 可以使用 `.md`，使用任何注册组件时必须使用 `.mdx`。
2. 仅在首屏摘要确实降低阅读成本时生成同名 `.portal.json`。

新建或定位正式产物时先遵守 [`artifact-management`](artifact-management.md)。上游只声明 artifact key 与业务阻断条件，不自行拼接 portal target、group、route 或 collection。

业务 Skill 自己负责业务结论、章节顺序和领域质量门禁；`document-publisher` 提供已注册表达能力、格式校验和发布动作。发布器不得从普通 Markdown 猜测组件、图形或首屏。

业务 Skill 的参考应声明稳定 artifact type、推荐 layout、导航 collection、稳定 slug、正文与首屏的边界、图片 alt 映射及业务阻断条件。需要整体表达设计时进入 [`authoring-workflow`](authoring-workflow.md)；只查询字段时直接进入 [`components/index`](components/index.md)。

富能力不可用时，在同一最终源文件内改用标准 Markdown；不创建独立降级稿。新增门户能力时先更新注册表、MDX 注册入口、实现、对应组件参考与验证测试，再允许上游写入。
