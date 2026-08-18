# Guardrails 审查清单

## Gate 1：触发判定与元信息

- 已明确本次是 `create_baseline`、`update_impacted_domains`、`restructure` 或 `no_change`
- 若为 `no_change`，已给出充分理由，且没有遗漏本应上升为项目级规则的变化
- 元信息完整：版本、状态、Owner、生效日期、复审周期、动作类型、触发原因、适用范围
- 范围与非范围明确
- 变更记录存在

## Gate 2：证据与事实标准

- 关键证据来源明确
- 若为 `repository_scan_first`，已区分 `fact`、`declared_standard`、`future_intent`
- 事实与标准冲突时，已明确标记为 drift / 待决策 / 按现状更新 / 维持目标状态
- 没有把局部实现、技术债、漂移现状直接升格为 Guardrail

## Gate 3：规则质量与治理完整性

- 每条关键规则都有 `Rule ID / Level / Rule / Rationale / Applies To / Verification / Owner / Source`
- Must / Should / Nice 分级清晰
- 默认选择、允许范围、禁止项明确
- 例外流程完整可执行
- 未混入 feature-specific 设计细节
- 分域模式下，index 与领域文档职责清楚

## Gate 4：工作流钩子与下游影响

- 已明确本次变更影响了哪些领域
- 已列出需要重审的下游文档/技能
- 阻塞建议清晰且一致：`block_before_design` / `review_before_merge` / `sync_next_cycle`
- API/HLD/LLD/Runbook 等关键下游未遗漏
- 与 `workflow-hooks.md` 的映射口径一致

## Gate 5：一致性与可落地性

- 与现有技术栈、批准标准、稳定仓库事实不冲突
- 若存在冲突，已给出明确处理路径
- 规则能通过 lint / review / CI / 运行检查等方式验证
- Owner 与执行责任清楚
