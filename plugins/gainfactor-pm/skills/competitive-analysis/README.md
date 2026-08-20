# Competitive Analysis Skill

面向产品决策的竞品分析 Skill。运行规则以 [SKILL.md](SKILL.md) 为唯一入口，本文件仅帮助维护者理解目录，不重复定义执行流程。

## 前置条件

必须先有已确认的 `PRODUCT_DEFINITION`，并由用户明确选择主产品。缺少上游定义时返回 `define-product`，不在本 Skill 内临时补定义绕过门禁。

## 唯一节点链

```text
A0 任务启动
→ A1 市场分析并创建门户文档
→ A2 竞品检索与确认
→ A3 单品分析循环（选择并锁定一个对象）
→ B1 基础
→ B2 功能分析
→ B3 AI 探针（条件）
→ B4 体验
→ B5 增长
→ B6 单品审阅
→ A3 选择下一对象，或进入 A4 单品分析阶段收口与横向比较
→ C1 最终成稿
```

每个节点都在 `SKILL.md` 中定义：前序输入、本节点任务、正式写入和完成门禁。参考文件只补充节点内部方法，不能改变顺序。

## 文档策略

- 正式报告：`COMPETITIVE_ANALYSIS`，使用 MDX/DSL，直接进入共享文档门户。
- 研究底稿：`COMPETITIVE_ANALYSIS_WORKLOG`，保存证据、过程和恢复点，不发布。
- A1 完成后立即创建正式报告，不等待竞品确认或全部分析结束。
- 之后每个正式写入节点都更新同一文件和稳定 slug。
- 页面蓝图、文件写入、门户更新、校验、回读五项全部通过，节点才能完成。

默认路径：

```text
docs/Competitive-Analysis-{产品名}-{YYYYMMDD}.mdx
docs/Competitive-Analysis-{产品名}-{YYYYMMDD}.research.md
```

正式文档的表达与发布遵循 `document-publisher`。数据趋势、结构和关系优先使用 `antv-infographic-syntax`，不以大表格代替可视表达。

每次正式写入先按 `references/09-report-writing-and-visual-design.md` 明确读者任务、核心判断、信息关系、MDX 组件或图形及证据落点，再调用 `document-publisher` 直接创建或更新最终 MDX 与门户条目；不存在中间 Markdown 文档或 Markdown→MDX 转换阶段。

## 参考文件

- `references/01-a0-a2-start-market-and-competitor-selection.md`：A0–A2 任务启动、市场分析与竞品检索确认。
- `references/02-b1-foundation-analysis.md`：B1 基础分析。
- `references/03-b2-feature-analysis.md`：B2 功能分析。
- `references/04-b3-ai-probe-testing.md`：B3 AI 探针（条件节点）。
- `references/05-b4-experience-analysis.md`：B4 体验分析。
- `references/06-b5-growth-analysis.md`：B5 增长分析。
- `references/07-b6-a4-closure-and-comparison.md`：B6 单品完整性审阅与交付门禁、A4 单品分析阶段收口与横向比较。
- `references/08-c1-final-report.md`：C1 最终成稿与交付。
- `references/09-report-writing-and-visual-design.md`：全流程正式报告的页面蓝图、MDX 组件职责、逐节点结构与视觉门禁。

## 维护原则

- 流程、门禁、状态枚举和节点跳转只在 `SKILL.md` 定义一次；参考文件只能引用这些定义，不得创建近义状态名或第二套完成条件。
- 参考文件只解释“本节点怎么做”，不得另起流程。
- 新增报告模块前先与用户确认其读者问题、必须内容、证据、表达方式和完成标准。
- “竞品分析结论”在全部正文、比较和建议完成后最后生成，再置于报告正文最前面。
- 正文外部引用统一关联到文档最底部的“外部来源索引”。
- mock 内容不得写入公共门户模板。
