# FieldList

用于标签和值的定义列表。字段必须可快速扫描；完整论证、长段落和连续正文留在普通正文或 `Panel.children`。

```ts
type FieldListProps = {
  items: Array<{ label: string; value: ReactNode; span?: 1 | 2 | "full" }>
  columns?: 1 | 2 | 3 | 4 | "auto"
  variant?: "plain" | "grid"
}
```

```mdx
<FieldList columns="auto" items={[
  { label: "地区", value: "上海" },
  { label: "同行人", value: "伴侣" },
  { label: "关键约束", value: "两天内确认；住宿体验优先；退改可控", span: "full" }
]} />
```

默认 `plain` 使用留白分组；需要明确单元格边界时才使用 `variant="grid"`。自动模式最多四列，移动端单列；超过 80 字的纯文本值会自动占满整行。显式列数也不能用来横排长句。
