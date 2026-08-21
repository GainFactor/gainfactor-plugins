# Board

用于同时浏览多个并列类别。分组中的内容由调用方组合；基础组件不理解 P0、P1、P2 等业务枚举。

```ts
type BoardProps = {
  label?: string
  columns?: 1 | 2 | 3 | "auto"
  groups: Array<{
    id?: string
    title: string
    icon?: string
    tone?: "neutral" | "info" | "warning" | "critical"
    description?: ReactNode
    children: ReactNode
  }>
}
```

```mdx
<Board label="用户价值优先级" groups={[
  {
    id: "priority-core",
    title: "核心闭环",
    tone: "critical",
    description: "P0 在内容层映射为 critical。",
    children: <FieldList items={[{ label: "能力", value: "约束确认与候选生成" }]} />
  }
]} />
```

色调只提供轻量语义提示，标题与正文必须独立表达含义。P0/P1/P2 映射由上游内容决定，不能作为 `Board` API。
