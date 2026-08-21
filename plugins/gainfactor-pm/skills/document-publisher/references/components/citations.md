# 引用与来源索引

正文引用使用 `Citation`，来源集中在 `SourceIndex` 中声明。

```ts
type CitationProps = { source: string; children?: ReactNode }
type SourceProps = { id: string; children: ReactNode }
type SourceIndexProps = { children: ReactNode; label?: string }
```

```mdx
结论来自公开报告 <Citation source="S01" />。

<SourceIndex>
  <Source id="S01">报告名称、机构、日期与链接</Source>
</SourceIndex>
```

来源 ID 必须唯一；每个引用目标必须存在，每个来源也必须被正文引用。`SourceIndex.label` 可覆盖来源区标题。校验会阻止重复、缺失或孤立映射。来源锚点自动考虑固定导航偏移。建议使用 `S01`、`S02` 等稳定 ID，不以标题或数组顺序临时生成。
