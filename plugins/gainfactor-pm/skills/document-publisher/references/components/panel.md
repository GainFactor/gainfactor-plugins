# Panel

用于一个需要独立阅读的分析单元。它只建立眉题、标题、摘要和正文结构，不通过大型 props 对象生成整张内容卡。

```ts
type PanelProps = {
  id?: string
  title: string
  icon?: string
  eyebrow?: string
  description?: ReactNode
  children?: ReactNode
}
```

```mdx
<Panel id="recommendation" title="推荐候选" icon="map-pinned" eyebrow="优先机会"
  description="先给少量差异明确、可核验的候选。">
  <FieldList items={[
    { label: "目标场景", value: "多约束行前决策" },
    { label: "证据强度", value: "中高" }
  ]} />

  正文按“事实—判断—影响—限制”连续展开。

  <Callout type="warn" title="依赖">实时供给需要再次核验。</Callout>
</Panel>
```

短字段组合 `FieldList`，提示组合 Fumadocs `Callout`，状态或分类使用 Badge/Cards。不要给 `Panel` 添加颜色、圆角、阴影或布局类 props。
