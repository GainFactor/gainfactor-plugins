# Guardrails 工作流钩子参考

## 1. 触发类型

| 类型 | 典型信号 | writer 动作 | 默认建议 |
|------|----------|-------------|----------|
| `create_baseline` | 仓库还没有 Guardrails | 建立 v0/v1 基线 | 在 API/HLD 大规模展开前完成 |
| `update_impacted_domains` | 平台、认证、数据、发布、合规等默认边界变化 | 只更新受影响领域 | 受影响设计先对齐 |
| `restructure` | 单文档过大、分域更新频繁、Owner 不清晰 | 改成 index + domain docs | 先收敛治理结构 |
| `no_change` | 只是 feature-local 变化 | 不改 Guardrails | 回到 HLD/LLD/ADR |

## 2. 下游映射

| Guardrails 变更域 | 优先重审的下游产物/技能 | 典型动作 |
|------------------|--------------------------|----------|
| API / Contract | `api-writer`, `api-reviewer`, `hld-writer`, `lld-writer` | 重审认证、版本、兼容性、错误语义、限流 |
| 数据与迁移 | `hld-writer`, `lld-writer`, `runbook-writer` | 重审数据模型、迁移、回滚、保留策略 |
| 安全与合规 | `api-writer`, `hld-writer`, `lld-writer`, `runbook-writer` | 重审访问控制、审计、密钥、隐私处理 |
| 发布 / 回滚 | `hld-writer`, `runbook-writer` | 重审部署方式、发布门禁、回滚流程 |
| 可观测性 | `hld-writer`, `runbook-writer`, `test-strategy-writer` | 重审 SLO、日志、metrics、traces、告警 |
| 前端 / UX | `prototype-designer`, `prototype-reviewer`, `lld-writer` | 重审交互一致性、埋点、错误态、可访问性 |
| 基础设施 / IaC | `hld-writer`, `lld-writer`, `runbook-writer` | 重审环境拓扑、权限边界、资源基线 |

## 3. 阻塞建议

| 条件 | 默认阻塞级别 |
|------|--------------|
| 当前仓库没有 Guardrails，且项目已进入 API/HLD 设计 | `block_before_design` |
| 默认认证、数据、发布、安全边界发生变化 | `block_before_design` |
| 已有设计基本完成，但 Guardrails 新增了强制规则 | `review_before_merge` |
| 只是补充低风险推荐项 | `sync_next_cycle` |

## 4. 使用规则

- 先判断“是否该改 Guardrails”，再决定“改哪些领域”
- 更新时只写受影响领域，不要顺手全量重写
- 如果一次变化会影响多个下游文档，必须在交接摘要里明确列出重审清单
