---
name: user-persona
description: Build realistic behavior-based user personas, explain their concrete usage paths and trust decisions, and derive a user-to-feature priority roadmap from isolated virtual-user Agent feedback or supplied user materials. Use for 用户画像、目标用户选择、Persona、用户行为分析或基于用户需求推导产品功能，并直接产出面向产品负责人与产品经理的可视化门户文档。
---

> **宿主兼容规则（必读）**：执行前完整读取 `../../references/host-compatibility.md`，并按当前宿主选择交互提问、独立 Agent 和文件操作方式。

# User Persona

> **语言规则**：默认跟随用户输入语言；用户显式指定时以用户指定为准。稳定 artifact type 使用 `USER_PERSONA`。详见 `../../references/language-policy.md`。

先理解具体的人在真实情境中怎样行动，再判断产品应该优先帮助谁。不得从产品功能反向拼接人物，不得用人口属性、MBTI、接受程度或抽象四字标签代替真实需求和行为。

## 适用边界

适用于：

- 通过相互隔离的虚拟用户 Agent 建立真实、具体且有代表性的用户画像；
- 从访谈、评论、工单、问卷或行为材料归纳用户画像；
- 解释用户的使用背景、目标、实际行为、痛点、决策与信任因素；
- 从多个用户画像归纳共性与特殊需求，并形成 `用户 × 功能优先级路线图`；
- 在竞品分析、BRD 或 PRD 前形成可直接复用的用户与产品机会输入。

不适用于只制作营销人设、按人口属性贴标签，或在没有具体行为依据时直接罗列功能。

产品定义不清时优先复用已有 `PRODUCT_DEFINITION`；缺口会改变画像方向时只追问 2–3 个关键问题，或建议先运行 `$define-product`。

## 必读参考

1. 始终读取 [输入诊断与研究模式](references/intake-and-modes.md)。
2. 始终读取 [增量工作流与阶段门禁](references/incremental-workflow-and-gates.md)。
3. 使用 Agent 收集反馈时读取 [虚拟用户探索与归纳协议](references/simulation-and-synthesis.md)。
4. 形成单个画像时读取 [用户画像结构](references/persona-schema.md)。
5. 开始写门户文档前读取 [报告结构与质量门禁](references/report-structure-and-quality.md)，并调用 `$document-publisher` 按 Shortcut 进入 `authoring-workflow`，随后只读取实际使用的组件参考。
6. 生成人物图片时读取 [Persona 人物图片生成](references/persona-image-generation.md)。
7. 形成首屏视图和发布时读取 [门户呈现](references/portal-presentation.md)。
8. 只有用户要求详细假设管理时读取 [假设审计](references/assumption-audit.md)。

## 核心工作方式

采用“完成一部分、检查一部分、写入一部分”的增量工作方式：

1. 明确产品定义与研究范围，通过产品上下文门禁后，创建最终 `.mdx` 并写入已确定的产品定义。
2. 选择 Agent 模拟、材料综合或混合路径；工作证据写入内部 research sidecar，不把研究过程堆入面向读者的报告。
3. Agent 模拟先建立具体现实的人物设定并通过真实性门禁，再运行相互隔离的无产品盲测。
4. 每个行为 Step 必须说明目标、工具或现实方法、使用方式、操作对象、获得的反馈、用户判断、顾虑、决定和下一步；字段按情境适用，不强行加入软件、品牌或搜索词。
5. 无产品路径通过门禁后，逐项测试中性最小产品命题；不得根据回答临时补功能说服 Agent。
6. 收齐反馈后比较使用背景、核心目标、期望结果、当前行为、痛点、决策与信任因素、产品前后变化和放弃路径，再选择目标用户；不足时减少画像，不凑数。
7. 每个保留用户先通过画像内容门禁，再生成人物图片并组装最终人物档案；图片与文档表达门禁通过后立即写入模块二，然后处理下一个人物。
8. 模块二使用已注册的 `PersonaBrief`、`FieldList`、`Steps/Step` 和 `Panel` 直接写最终阅读结构；`PersonaBrief` 只承担人物章节导读，不包裹后续正文。每个人物必须作为一个连续内容块完整写入，当前人物的全部功能结束后才能开始下一个人物。
9. 所有画像完成后才归纳共性与特殊需求；先按解决的问题和服务能力归一化跨人物功能，保留人物来源与差异顾虑，再使用 `Board` 按 P0、P1、P2、暂不纳入形成 `用户 × 功能优先级路线图`；需要精确核对人物与功能关系时另加 Markdown 矩阵。模块一概览、模块二人物块、模块三人物引用和 Presentation cards 必须沿用同一份人物顺序清单。
10. 全部模块完成后进行一次整体内容、语言、推导、可视化和页面节奏优化；优化不得制造新结论。
11. 生成并校验 `.portal.json`，再由 `$document-publisher` 挂载、构建并验证门户；发布阶段只校验和发布已经写好的最终内容，不二次推导语义。

## 独立 Agent 纪律

- 当前宿主支持独立 Agent 时，默认实际创建通常 4–6 个相互隔离的 Agent；每个 Agent 只获得自己的身份、现实情境、资源、偏好、风险与行为习惯。
- 当前宿主无法创建独立 Agent 时：材料综合路径照常执行；Agent 模拟路径先询问用户是否接受同一任务内的顺序降级。用户不接受时只交付模拟方案；用户接受时可以交付探索性画像，但必须明确未实现独立上下文，不得声称完成了相互隔离的虚拟访谈。
- 第一阶段不得暴露产品；第二阶段一次只展示一个中性最小命题。
- 允许所有 Agent 接受、犹豫、拒绝或继续使用原方案，不预设正反比例。
- 不根据未采集信息生成精确用户比例、群体规模或市场分布。

## 门禁纪律

- 每个阶段必须产出可检查结果；未通过当前阶段门禁，不得写入依赖该结果的报告章节，也不得进入下一阶段。
- 每个正式板块写入前必须确定阅读价值、内容结构、组件映射和 Markdown 降级；没有明确阅读收益时保留正文，不用组件制造视觉丰富感。
- 门禁失败时只补充或重做失败部分，不推翻已经通过且不受影响的阶段。
- 单个用户画像逐个检查、逐个写入；不得等待全部人物完成后统一补写，也不得先生成图片或功能再反向补人物。
- 每次追加或移动人物内容后检查人物块边界：从当前人物三级标题与 `PersonaBrief` 开始，到下一个人物标题或模块三开始之前，只能出现当前人物的情境、目标、行为、痛点、决策和功能；发现其他人物姓名、persona_id、图片 alt 或功能来源时立即停止并修正。
- 结构校验器只检查确定性格式；真实性、代表性、推导完整性和表达质量必须按参考文件进行语义检查。

## 默认交付

面向读者的正式产物：

```text
docs/gainfactor/{product-slug}/user-persona.mdx
docs/gainfactor/{product-slug}/user-persona.portal.json
docs/gainfactor/{product-slug}/assets/user-persona/*.png
```

内部工作产物建议使用：

```text
docs/gainfactor/{product-slug}/.work/user-persona.research.json
```

research sidecar 保存人物设定、原始反馈、合并记录、功能来源和阶段门禁状态，不导入门户。正式 `.mdx` 必须脱离门户也能完整阅读；只允许使用 `$document-publisher` 能力注册表中已注册的 Markdown、MDX 组件和图形 DSL，不写任意 HTML、脚本、内联样式或未注册组件。

报告只包含三个二级阅读模块：

1. `产品定义与目标用户`；
2. `用户画像`；
3. `用户 × 功能优先级路线图`。

研究与图片通过门禁后，默认把最终报告、图片和呈现清单写入项目并自动导入文档门户，不询问是否保存或是否导入。用户明确要求仅在对话中输出、不要写文件、不要导入门户或指定其他交付方式时再缩减交付。自动导入不等于自动启动服务；只有用户要求预览、打开或启动时才启动门户。

稳定发布身份：

```text
source: docs/gainfactor/{product-slug}/user-persona.mdx
presentation: docs/gainfactor/{product-slug}/user-persona.portal.json
artifact: user-persona
```

调用 `$document-publisher` 的 `artifact-management` 和 `publishing/publish` 完成身份解析与发布，不在本 Skill 拼接 target、group、collection 或 route。默认写入工作区 `.gainfactor/portal`；用户显式指定兼容门户时沿用该 target。未提供发布元信息时使用 `version=1.0`、`status=draft`、`owner=unassigned` 和当前日期；已有项目约定时优先沿用。导入后校验源 MDX、图片、导入结果、门户资产、presentation 和清单；失败时说明具体阻塞并保留已成功写入的源产物。

## 下游复用契约

后续任务读取 `USER_PERSONA` 时：

- 使用产品定义、目标用户选择、人物背景、核心目标、期望结果、关键行为、痛点、决策与信任因素、期望产品功能和功能优先级作为用户上下文；
- 不静默改写上游 `PRODUCT_DEFINITION`；
- 新信息与既有画像冲突时显式列出冲突并更新；
- P0/P1/P2 表示基于用户价值的功能优先级，不等于研发排期或交付承诺；进入 BRD、PRD 时继续结合业务、技术、成本和交付条件决策。
