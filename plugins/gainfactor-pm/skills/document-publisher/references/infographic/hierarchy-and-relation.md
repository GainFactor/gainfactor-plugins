# Hierarchy 与 Relation

- 普通层级使用 `hierarchy-*`：单一 `root`，通过 `children` 递归嵌套。
- `hierarchy-structure` 使用 `items`。
- 节点关系使用 `relation-*`：节点放入 `nodes`，边放入 `relations`；需要稳定引用时显式填写 node id。

```infographic
infographic relation-dagre-flow-tb-badge-card
data
  title 发布关系
  nodes
    - id source
      label 来源
    - id publish
      label 发布
  relations
    source - 校验后进入 -> publish
```

复杂技术拓扑、多种边语义、时序和回路优先 Mermaid。
