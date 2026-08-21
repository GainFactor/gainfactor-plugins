# Compare

- 双方对比使用 `compare-binary-*` 或 `compare-hierarchy-left-right-*`：`compares` 必须只有两个根节点，具体对比项放入各自 `children`。
- SWOT 使用 `compare-swot`，四类可作为根节点并按需包含 children。
- 象限使用 `compare-quadrant-*`，直接放四个象限根节点；只有横纵轴有真实测量依据时使用。

```infographic
infographic compare-binary-horizontal-simple-fold
data
  title 方案对比
  compares
    - label 方案 A
      children
        - label 上手快
    - label 方案 B
      children
        - label 控制强
```

需要逐格核验多个字段时改用 Markdown 表格，不用信息图替代精确证据。
