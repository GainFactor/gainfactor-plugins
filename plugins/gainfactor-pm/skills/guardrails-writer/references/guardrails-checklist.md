# Guardrails 自检清单

## 触发判定

- 已明确本次是 `create_baseline`、`update_impacted_domains`、`restructure` 或 `no_change`
- 已记录触发原因，而不是“顺手补规范”
- 如果结论是 `no_change`，已明确回退到 HLD/LLD/ADR，而不是误改 Guardrails
- 若是首次生成，已明确 `interview_first` 或 `repository_scan_first`

## 基线质量

- 元信息完整：版本、Owner、状态、生效时间、复审周期
- 适用范围与非范围明确
- Must/Should/Nice 分级明确
- 每条规则都有 Verification、Owner、Source
- 例外流程清晰可执行
- 变更记录有条目

## 项目级边界

- 没有写入 feature-specific 设计细节
- 规则是跨模块、跨团队、可复用的长期约束
- 默认选择、允许范围、禁止项都写清楚
- 只更新了受影响领域，没有无关重写

## repository_scan_first 事实标准

- 已区分 `fact`、`declared_standard`、`future_intent`
- 没有把局部实现、技术债、漂移现状直接升格成 Guardrail
- 事实与标准冲突时，已显式标记为 drift 或待决策项
- 至少有可交叉验证的事实来源支持关键规则候选

## 工作流钩子

- 已明确写出“何时需要再次更新 Guardrails”
- 已给出受影响的下游文档/技能
- 已给出阻塞建议：先更新再继续 / 合并前重审 / 下周期对齐
- API/HLD/LLD/Runbook 等关键下游的影响没有遗漏

## 输出拓扑

- 单文档模式适合当前范围，或已解释为什么要拆成 index + 分域文档
- 分域模式下，index 负责总则与钩子，领域文档负责具体规则

## 覆盖质量

- 已优先覆盖安全、API、数据、发布、可观测性等高风险领域
- 规则可验证（lint/CI/审查/运行检查）
- 与现有规范、技术栈、运行方式不冲突
