# List 与 Sequence

- 并列摘要使用 `list-*`，主数据字段为 `lists`。
- 严格顺序或阶段演进使用 `sequence-*`，主数据字段为 `sequences`，可选 `order asc|desc`。
- 多角色或多系统交互使用 `sequence-interaction-*`：每个泳道写入 `sequences`，泳道内节点放在 `children`，关系写入 `relations`。

```infographic
infographic sequence-ascending-steps
data
  title 发布流程
  sequences
    - label 需求确认
      icon clipboard-check
    - label 发布上线
      icon rocket
  order asc
```

每个语义条目必须有简短 label；图标型模板为主要条目填写本地 Lucide icon。存在分支和复杂回路时改用 Mermaid。
