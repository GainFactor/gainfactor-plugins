# SectionHeading

用于需要稳定锚点、正确 h2/h3/h4 语义、可选 Lucide 图标并进入右侧目录的章节标题。不自动替换普通 Markdown 标题。

```ts
type SectionHeadingProps = {
  title: string
  level?: 2 | 3 | 4
  icon?: string
  id?: string
}
```

```mdx
<SectionHeading title="研究结论" level={2} icon="chart-no-axes-combined" id="findings" />
<SectionHeading title="行为特征" level={4} icon="scan-face" id="persona-behavior" />
```

`level` 默认 `2`。省略 `id` 时从标题生成锚点；标题可能改名或需要长期引用时显式填写。目录只使用 `title`，图标不进入目录文本。画像等复合组件内部章节可用 `level={4}`。降级为同层级 Markdown 标题。
