# Project Guardrails 模板

> 本模板用于输出项目级 Guardrails 基线或增量更新。目标是回答三件事：默认怎么做、绝对不能做什么、什么变化会触发下游重审。

---

# Project Guardrails

## 0. 元信息

| 项目 | 内容 |
|------|------|
| 版本 | vX.Y |
| 状态 | draft / in_review / approved |
| Owner | [负责人/团队] |
| 生效日期 | YYYY-MM-DD |
| 复审周期 | 每季度 / 每大版本 / 按需 |
| 动作类型 | create_baseline / update_impacted_domains / restructure |
| 生成模式 | interview_first / repository_scan_first |
| 触发原因 | [项目启动 / 架构变化 / 合规要求 / 事故复盘 / 重复评审问题] |
| 输出模式 | 单文档 / index + domain docs |
| 适用范围 | [系统/团队/仓库/运行环境] |

---

## 1. 定位与边界

- **In Scope**：
- **Out of Scope**：
- **不作为功能级设计输入的内容**：
- **本次仅更新的领域**：

---

## 2. 更新触发与工作流钩子

### 2.1 何时必须创建或更新 Guardrails

| 触发类型 | 典型信号 | 处理动作 |
|----------|----------|----------|
| create_baseline | 仓库还没有 Guardrails | 建立最小可用基线 |
| update_impacted_domains | 架构/平台/认证/数据/发布等默认边界变化 | 只更新受影响领域 |
| restructure | 单文档过大、分域更新频繁 | 重构为 index + domain docs |
| no_change | 仅 feature-local 变化 | 回退到 HLD/LLD/ADR |

### 2.2 下游重审钩子

| 变更域 | 受影响产物/技能 | 建议动作 | 阻塞级别 |
|--------|-----------------|----------|----------|
| API / Contract | API Contract, HLD, LLD | 先对齐默认边界，再继续设计 | [block_before_design / review_before_merge / sync_next_cycle] |
| 数据与迁移 | HLD, LLD, Runbook | 重审数据模型、迁移、回滚 | [...] |
| 安全与合规 | API Contract, HLD, LLD, Runbook | 重审认证、审计、访问控制 | [...] |
| 发布 / 回滚 / 可观测性 | HLD, Runbook | 重审部署、回滚、SLO、告警 | [...] |
| 其他领域 | [路径/技能] | [动作] | [...] |

---

## 3. 事实标准与证据分层

### 3.1 观察到的事实

- [代码 / 配置 / CI / IaC / Runbook / 测试 / 事故记录]

### 3.2 声明性标准

- [ADR / 既有规范 / README / 安全政策 / 既有 Guardrails]

### 3.3 冲突与漂移

| 冲突项 | 事实 | 标准/意图 | 处理结论 |
|--------|------|-----------|----------|
| [例] |  |  | [按现状固化 / 维持目标状态 / 待决策] |

---

## 4. 规则分级与例外机制

- **Must**：必须遵守，违反即阻塞
- **Should**：强烈建议，需显式说明理由才能偏离
- **Nice**：推荐项，不阻塞

**例外流程**：申请人 / 审批人 / 有效期 / 记录位置 / 到期复审方式

---

## 5. 默认选择与禁止项

- **默认技术路径**：
- **允许范围**：
- **明确禁止项**：
- **依赖的上游规范/ADR/外部政策**：

---

## 6. LLD 模块要求（强制）

| 模块 | 要求（Required/Optional/Forbidden） | 理由 | 来源 |
|------|-------------------------------------|------|------|
| Core | Required |  |  |
| API Contract | Required |  |  |
| Storage & Migration |  |  |  |
| Async/Event |  |  |  |
| Infra/IaC |  |  |  |
| Observability |  |  |  |
| Security/Compliance | Required |  |  |
| Deployment/Release |  |  |  |
| Frontend UX |  |  |  |
| External Integration |  |  |  |
| SDK/Library |  |  |  |

---

## 7. Guardrails 规则表模板

| Rule ID | Level | Rule | Rationale | Applies To | Verification | Owner | Source |
|---------|-------|------|-----------|------------|--------------|-------|--------|
| GR-001 | Must |  |  |  |  |  |  |

---

## 8. 高风险领域规则

### 8.1 API / Contract Guardrails

[使用规则表模板]

### 8.2 数据与迁移 Guardrails

[使用规则表模板]

### 8.3 安全与合规 Guardrails

[使用规则表模板]

### 8.4 发布 / 回滚 / 可观测性 Guardrails

[使用规则表模板]

---

## 9. 其他领域规则（按需）

### 9.1 前端 UX / 工程

[如适用再填写]

### 9.2 基础设施 / IaC

[如适用再填写]

### 9.3 外部集成 / SDK / 事件消息

[如适用再填写]

---

## 10. 本次变更影响摘要

- **本次更新原因**：
- **若首次生成：采用的模式**：
- **受影响领域**：
- **需要重审的下游文档/技能**：
- **阻塞建议**：
- **未覆盖但需后续跟进的事项**：

---

## 11. 变更记录

| 版本 | 变更内容 | 变更原因 | 日期 | 作者 |
|------|----------|----------|------|------|
| vX.Y |  |  |  |  |
