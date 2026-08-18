# 文档门户数据契约

公共生成器接受 Markdown/MDX 文档和可选评审 JSON。所有数据均在运行时写入生成目录，公共模板不保存业务内容。

## 文档标识

- `slug`：门户内稳定且唯一的文档标识，只允许小写字母、数字和连字符。
- `type`：用户可读的文档类型，例如 `BRD`、`PRD`、`HLD`、`LLD`、`Test Strategy` 或 `Runbook`。
- `collection`：面包屑中展示的集合名称，例如“产品文档”或“研发设计”。
- `group`：左侧一级导航分组。默认按文档类型映射为 `product-requirements`、`technical-design`、`quality-delivery` 或 `other`；文档本身作为二级条目。
- 相同 `slug` 再次导入表示更新；不同 `slug` 会在同一门户中并存。

## 评审 JSON

```json
{
  "conclusion": "通过 / 有条件通过 / 不通过",
  "issues": [
    {
      "id": "PRD-001",
      "severity": "P0 / P1 / P2",
      "title": "问题摘要",
      "sectionId": "目标标题的 HTML id",
      "sectionTitle": "目标章节名称",
      "suggestion": "修改建议"
    }
  ]
}
```

`id`、`severity`、`title` 和 `sectionId` 必填。`sectionTitle` 与 `suggestion` 可选。问题必须属于当前导入的文档，不能跨文档复用错误的章节 ID。
