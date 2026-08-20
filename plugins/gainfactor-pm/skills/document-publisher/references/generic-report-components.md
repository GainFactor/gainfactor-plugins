# 通用报告组件

Profile、InfoGrid、StructuredSteps、ContentPanel 和 GroupedBoard 只负责布局与呈现。业务 Skill 决定内容、字段名称、顺序和使用场景。使用这些组件时源文件必须为 `.mdx`。

下文“Markdown 降级”均指在同一份最终 `.mdx` 内使用标准 Markdown 语法替代富组件；不得生成独立 `.md`、临时稿或转换任务。

五个组件都支持响应式布局、深浅色主题、打印/PDF、中文长文本、自动换行和空字段省略，不依赖 CDN 或远程字体。颜色只辅助层级，标签、字段名、步骤编号和提示文字仍需明确表达语义。

## Profile

用于图片、主体身份、摘要信息、结构化字段、标签与详细正文的组合。适合人物、成员、公司、产品或案例主体；不适合只展示几项元数据。

```ts
type ProfileProps = {
  name: string
  role?: string
  summary?: string
  image?: { src: string; alt: string }
  facts?: Array<{ label: string; value: ReactNode }>
  tags?: string[]
  children?: ReactNode
}
```

```mdx
<Profile
  name="赵宁"
  role="视觉设计师"
  summary="计划假期短途旅行，但没有时间制作详细攻略"
  image={{ src: "./assets/zhao-ning.png", alt: "赵宁的人物画像" }}
  facts={[
    { label: "年龄", value: "29 岁" },
    { label: "地区", value: "成都" },
    { label: "职业", value: "视觉设计师" },
    { label: "性格", value: "谨慎、重视体验" }
  ]}
  tags={["自然景观", "小众目的地", "短途旅行"]}
>
  人物或对象的详细背景正文。
</Profile>
```

图片可省略；填写 `image` 时 `src` 和非空 `alt` 都是必需字段。本地相对图片由导入器搬运并重写为门户路径。空字段、空标签和空正文不渲染。Markdown 降级为图片、标题、四列表格、标签列表和背景正文。

## InfoGrid

用于紧凑展示多组字段和值，适合概况、范围、参数、条件和元数据。它不用于精确横向比较或长篇正文。

```ts
type InfoGridProps = {
  columns?: 2 | 3 | 4 | "auto"
  items: Array<{
    label: string
    value: ReactNode
    span?: 1 | 2 | "full"
  }>
}
```

```mdx
<InfoGrid
  columns="auto"
  items={[
    { label: "产品阶段", value: "概念验证" },
    { label: "目标用户", value: "缺少攻略时间的短途旅行者" },
    { label: "使用场景", value: "节假日前临时规划" },
    { label: "研究范围", value: "行程生成与结果核验", span: 2 }
  ]}
/>
```

`auto` 在桌面端按容器选择二至四列，平板通常为两列，移动端为一列。空字段省略，内容不设固定高度。Markdown 降级优先使用多列表格；长文本改用定义列表或分组列表。

## StructuredSteps

用于带结构化字段的连续步骤。字段名称完全由调用方定义；复杂分支、并行关系和回路继续使用 Mermaid。

```ts
type StructuredStepsProps = {
  items: Array<{
    id?: string
    title: string
    content?: ReactNode
    fields?: Array<{
      label: string
      value: ReactNode
      tone?: "default" | "muted" | "attention"
    }>
  }>
}
```

```mdx
<StructuredSteps
  items={[
    {
      id: "search-destination",
      title: "搜索可选目的地",
      content: "寻找适合三天假期的旅行目的地",
      fields: [
        { label: "工具", value: "小红书" },
        { label: "使用方式", value: "搜索五一杭州周边小众景点" },
        { label: "获得反馈", value: "大量内容推荐西湖和热门古镇" },
        { label: "顾虑", value: "担心节假日游客过多", tone: "attention" }
      ]
    }
  ]}
/>
```

`id` 用于稳定锚点；省略时生成 `structured-step-1` 等顺序锚点。`tone` 只辅助显示，字段名和值必须独立表达含义。内容始终展开。Markdown 降级为编号标题、主体段落和字段列表。

## ContentPanel

用于可重复的结构化内容单元，组合标题、辅助分类、说明、标签、字段、正文与可选提示。适合方案、发现、案例、建议、风险或决策项，但组件自身不理解这些业务概念。

```ts
type ContentPanelProps = {
  id?: string
  title: string
  eyebrow?: string
  description?: ReactNode
  tags?: string[]
  fields?: Array<{ label: string; value: ReactNode }>
  notice?: {
    label?: string
    content: ReactNode
    tone?: "info" | "warning" | "success" | "neutral"
  }
  href?: string
  children?: ReactNode
}
```

```mdx
<ContentPanel
  id="time-and-crowding"
  title="根据时间和拥挤程度推荐目的地"
  eyebrow="P0"
  description="帮助用户在有限时间内快速缩小选择范围"
  tags={["赵宁", "周远"]}
  fields={[
    { label: "需求来源", value: "用户没有时间逐个比较目的地" },
    { label: "解决问题", value: "降低前期筛选和信息整理成本" },
    { label: "期望结果", value: "快速获得可靠候选" }
  ]}
  notice={{
    label: "主要顾虑",
    content: "推荐依据不透明可能降低用户信任",
    tone: "warning"
  }}
>
  更详细的说明、依据或限制条件。
</ContentPanel>
```

`id` 提供本组件锚点，`href` 让标题链接到另一个位置。空 notice 不显示；tone 不替代可见 label。短内容不会设置固定高度。Markdown 降级为三级标题、辅助信息、字段列表、正文和可选引用块。

## GroupedBoard

用于把同构条目组织进多个并列分组，帮助读者按分类浏览。分组名称和顺序完全由调用方决定；组件不理解优先级、状态、阶段或路线图，也不会按分组名称自动着色、排序或推导关系。

```ts
type GroupedBoardProps = {
  label?: string
  columns?: 2 | 3 | 4 | "auto"
  groups: Array<{
    id?: string
    title: string
    description?: ReactNode
    items: Array<{
      id?: string
      title: string
      description?: ReactNode
      href?: string
      tags?: string[]
      fields?: Array<{ label: string; value: ReactNode }>
      children?: ReactNode
    }>
  }>
}
```

```mdx
<GroupedBoard
  label="方案分组"
  columns="auto"
  groups={[
    {
      id: "user-side",
      title: "用户侧",
      description: "直接影响用户理解与操作的内容",
      items: [
        {
          id: "explain-result",
          title: "解释推荐依据",
          description: "说明候选结果为何适合当前约束",
          tags: ["可解释性", "信任"],
          fields: [
            { label: "输入", value: "用户时间与偏好" },
            { label: "输出", value: "带依据的候选结果" }
          ]
        }
      ]
    },
    {
      id: "system-side",
      title: "系统侧",
      items: [
        {
          title: "核验关键信息",
          description: "在结果呈现前检查时效性和一致性"
        }
      ]
    }
  ]}
/>
```

`label` 为整个分组区域提供可访问名称。`columns="auto"` 根据容器宽度自动排列，桌面最多形成多列，移动端降为一列，打印固定为两列。空标题、空条目和空字段不渲染；分组没有有效条目时整个分组省略。

`group.id` 和 `item.id` 提供稳定锚点。省略时生成 `grouped-board-group-1` 和相应的顺序条目锚点；需要外部长期引用时应显式填写。`href` 只负责标题跳转，不改变条目内容。

GroupedBoard 用于浏览分组，不用于精确交叉比较、连续步骤或节点关系：精确比较用表格，连续过程用 StructuredSteps，复杂关系用 Mermaid。Markdown 降级为“三级分组标题 + 分组说明 + 四级条目标题 + 标签和字段列表 + 正文”。

## 写入与验证

1. 页面蓝图先说明为什么该组件比 Markdown 更利于当前阅读任务。
2. 只使用 `portal-capabilities.json` 中 registered 的组件和上述字段。
3. 导入时搬运 Profile 的本地相对图片，并校验 image alt。
4. 发布前运行 `compile_portal_document.py --validate`；门户随后运行 `npm run types:check` 和静态构建，验证 MDX、组件属性和打印样式可编译。
5. 预览时检查桌面、移动端、深浅色和浏览器打印预览；无法渲染组件时，在同一最终 `.mdx` 内使用本节给出的标准 Markdown 回退。
