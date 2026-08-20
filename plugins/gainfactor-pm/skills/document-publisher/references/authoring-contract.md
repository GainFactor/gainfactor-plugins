# 上游 Skill 写入契约

业务 Skill 在内容构建阶段直接完成两项交付：

1. 一份直接完成、无需二次转换且脱离门户装饰仍能完整阅读的最终 `.mdx`。
2. 只有在首屏摘要确实降低阅读成本时，生成同名 `.portal.json`。

## 决策顺序

先按 `expression-design.md` 形成页面蓝图，再从 `tool-catalog.md` 中状态为 registered 的工具选择表达。不得凭记忆编造组件名、属性或语法。业务 Skill 的参考文件应声明：

- 稳定 artifact type、推荐 layout 与导航 collection；
- 哪些内容保留为正文，哪些内容值得成为首屏模块；
- 所用模块字段及阻断校验；
- 是否需要 Mermaid、Tabs 或其他正文组件；
- 本地图片的 alt 与 manifest 的 `sourceImageAlt` 对应规则；可解析来源及重复 alt 规则见 `capabilities.md` 的 Portal Presentation v1。

页面蓝图至少说明：

```yaml
presentationDecision:
  audience: 谁阅读
  readerTasks: [需要快速做出的判断]
  readingPath: executive-first | sequential | reference | exploratory
  sections:
    - purpose: 本段帮助读者完成什么
      relation: prose | comparison | sequence | hierarchy | network | evidence | warning
      density: low | medium | high
      expression: markdown | table | cards | tabs | steps | mermaid | infographic | node-graph | image-zoom
      reason: 为什么该表达比正文更容易理解
      fallback: 工具不可用时，在同一最终 .mdx 内采用的标准 Markdown 表达
```

这是决策记录，不是固定模板。业务 Skill 可以采用适合自身领域的字段名，但必须保留“阅读任务 → 信息关系 → 表达方式 → 选择理由 → 降级方案”这条链路。

如果没有合适工具，在同一最终 `.mdx` 内退回标准 Markdown 语法；不要另建 `.md`、中间稿或转换步骤，也不要输出门户未注册的 JSX。需要新增工具时，先更新能力注册表、MDX 注册入口、用法目录和验证，再让业务 Skill 使用。

不要把“先写普通 Markdown，再让发布器美化”作为工作流。业务 Skill 必须在写作时完成表达决策并直接写入最终组件或 DSL；发布器不会按标题猜测业务语义，也不维护“每种报告一个转换器”。新文档类型只需在业务 Skill 内声明写入决策，不修改发布器业务逻辑。

AntV Infographic 被选中时，当前 Skill 读取 `antv-infographic-syntax.md`，按官方模板选择规则生成 DSL，再由业务 Skill 把 DSL 直接写入最终 MDX。不得生成独立 HTML，也不得引用 CDN。

## 示例

```json
{
  "schemaVersion": 1,
  "layout": "report",
  "modules": [
    {
      "id": "summary",
      "type": "metrics",
      "items": [{"label": "核心判断", "value": "先解决信息核验"}]
    },
    {
      "id": "path",
      "type": "steps",
      "title": "理想路径",
      "items": [{"title": "表达", "content": "说清约束"}, {"title": "核验", "content": "检查关键事实"}]
    }
  ]
}
```

完整正文仍保留上述结论的依据和上下文。manifest 不得引入正文中没有的事实。
