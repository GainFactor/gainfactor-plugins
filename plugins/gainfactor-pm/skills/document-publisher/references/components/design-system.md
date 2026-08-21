# 文档设计系统

本参考只在维护门户主题、组件样式或视觉门禁时读取。业务 Skill 负责内容结构和组件选择，不拥有字号、间距、圆角、阴影或响应式规则。

## 分层边界

1. Fumadocs 负责页面壳、导航、目录和基础主题。
2. 标准 Markdown 由 `.prose` 的统一正文规则负责。
3. 注册富组件通过 `data-doc-component` 声明组件边界，内部标题必须使用稳定角色类，不依赖 `.prose h3` 或 `.prose h4` 的继承结果。
4. artifact 主题只允许调整封面和少量品牌呈现，不得重写正文标题、表格、图片、引用或富组件内部排版。

## Token 契约

默认视觉参考固定为 [Radix Themes Playground](https://www.radix-ui.com/themes/playground) 的以下组合：

```text
Accent: Orange
Gray: Slate（冷灰）
Appearance: Light / Dark
Radius: Medium
Scaling: 100%
Panel background: Solid
```

门户使用 Radix Themes 3.3 作为正文组件视觉基础层，并固定为 Orange + Slate + Medium + 100% + Solid；Fumadocs 继续负责页面壳、导航与文档能力。GainFactor 业务组件保留稳定 MDX API，但 Card、Badge、DataList、Callout 等基础外观必须由 Radix Themes 组件提供，不得重新仿写一套基础组件。

品牌色分为三个语义：`--gf-brand-solid` 与 `--gf-brand` 对应 `#FF6200` 实色，用于导航选中态、Logo 底色、标题图标、步骤圆点和装饰线；`--gf-brand-text` 是同色相的可读文字色，用于链接、标签文字和小字号强调。禁止把 `#FF6200` 直接用于白底小字号正文，也禁止将文字色用于大面积实色背景。

Token 固定分为三层，禁止跨层取值：

```text
Reference (--ref-*) → Semantic (--color-fd-* / --color-status-*) → Component (--doc-*)
```

- Reference：保存 Radix 参考色、状态色、遮罩和打印介质的原始值，只允许在 `:root` 与 `.dark` 中声明；
- Semantic：表达背景、文字、边框、强调和状态意图，页面壳及通用规则消费这一层；
- Component：表达文档字号、圆角、阴影及 Mermaid 图形色，所有 `.gf-*` 富组件必须消费这一层。

布局固有尺寸（视口上限、侧栏宽度、图像比例、控件宽高）不是视觉 Token，不为单次使用制造变量。

门户在 `app/global.css` 中维护以下 `--doc-*` 语义 Token：

- 字体：`text-label`、`text-caption`、`text-body`、`text-component-subtitle`、`text-component-title`、`text-entity-title`、`text-h4`、`text-h3`、`text-h2`；
- 间距：`space-field`、`space-component`、`space-subsection`、`space-section`；
- 外观：`radius-sm`、`radius-md`、`radius-lg`、`surface-subtle`、`border-subtle`、`shadow-none`、`shadow-card`、`shadow-media`；
- 布局：`card-padding`、`field-label-width`。

新增或修改组件时优先消费现有 Token。只有至少两个独立组件需要同一新尺度时才增加 Token，不把单次页面调整提升为设计系统能力。

组件组合层仍使用统一的文档间距：普通卡片使用 `card-padding` 与 `space-component`，紧凑字段使用 `space-field`。页面内静态组件以 Radix `surface` 变体为主，嵌套面板不得叠加投影；业务 CSS 只负责文档特有的响应式布局、图片尺寸、锚点偏移和打印规则。

MDX `Callout` 使用 Fumadocs 与 Radix 的公开样式；需要提示时在 `Panel.children` 中组合 `Callout`。语义图标在左，标题和正文上下排列，不得覆盖为粗左色条或额外投影。

视觉层级必须保持：

```text
H2 > H3 > H4 > component title > component subtitle
```

实体标题（例如 PersonaBrief 姓名）位于 H3 与 H4 之间或与上下文相称，但不得被当作正文目录标题。

## 组件标题角色

- `gf-entity-title`：PersonaBrief 等主体名称；
- `gf-component-title`：步骤、面板、分组标题；
- `gf-component-subtitle`：面板内部小节、看板条目标题。

组件内出现 `h3` 或 `h4` 时必须同时具备其中一个角色类。不要通过提高选择器优先级修复字号冲突。

## 组件细节契约

一致性不只来自 Token，还来自组件内部的对齐关系。所有注册组件必须遵守：

1. **首行对齐**：语义图标与标题位于同一布局行，图标盒按标题首行的视觉中心对齐；Grid 组件必须同时声明相同的 `grid-row`，不得依赖自动放置。
2. **左边界一致**：同一内容列中的标题、摘要、字段标签和值共享左边界。`dt`、`dd`、段落和列表必须显式清除浏览器默认 margin、padding 或缩进。
3. **层级可辨**：组件标题使用主文字色和 `component-title`；摘要、标签及来源使用次文字色和更小字号；正文不得与标题使用相同字号和字重。
4. **字段可扫读**：短字段可横向分列，但标签和值均左对齐；长值自动占整行，正文行长不超过约 `72ch`。
5. **单层表面**：一个独立内容组最多一层背景或边框，嵌套内容通过留白或分隔线组织，不叠加圆角和阴影。
6. **统一节奏**：紧凑字段使用 `space-field`，组件内容使用 `space-component`，章节之间使用 `space-subsection`；不得用额外空白补偿错误对齐。

陈列页必须使用正式导出的公共组件，不直接使用底层原语伪造示例，否则视觉检查无法代表 MDX 中的实际结果。

## 验证

`/portal-release-check` 是永久组件样板页，使用真实长度中文覆盖所有注册组件。视觉发布门禁至少验证：

- 320、390、768、1280、1920px 与明暗主题；
- 默认预设保持 Orange + Slate + Medium + 100% + Solid；
- TS/TSX 组件不得直接写颜色值，CSS 原始颜色只能出现在 Token 声明中；
- `.gf-*` 富组件的 `font-size`、`border-radius`、`box-shadow` 必须使用 `--doc-*` Token；
- 标题字号严格递减；
- `--doc-*` 核心 Token 存在；
- 富组件内部标题全部隔离；
- 每个组件无横向溢出；
- 图形、图片、引用、灯箱和裁切检查继续通过。

不得只在某一份业务报告上人工确认样式。
