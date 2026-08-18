# Test Strategy 模板

```markdown
# 测试策略：{项目/功能名称}

<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-strategy-profile-v1
artifact:
  id: TSTRAT-[DOMAIN]-001
  type: TEST_STRATEGY
  title: {项目/功能名称}
  status: draft
  owners: []
  created_at: YYYY-MM-DD
  updated_at: YYYY-MM-DD
  source_documents: []
entities:
  requirements: []
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions: []
  flows: []
  test_cases: []
relations: []
waivers: []
```
<!-- TRACEABILITY-METADATA:END -->

## 基本信息

- **PRD 基线**：{路径} v{版本}
- **API Contract 基线**：{路径} v{版本}
- **HLD 基线**：{路径} v{版本}
- **Guardrails**：{路径} / N/A
- **编写时间**：{YYYY-MM-DD}
- **状态**：Draft / Reviewed / Approved

## 上下文收集报告

### 已确认基线
- {基线 1}
- {基线 2}

### 关键约束
- {约束 1}
- {约束 2}

### 已识别风险
- {风险 1}
- {风险 2}

## 测试目标

- {目标 1}
- {目标 2}

## 范围

### In-scope
- {内容}

### Out-of-scope
- {内容}

### Must-not-regress
- {能力/流程}

## 质量风险清单

| 风险 ID | 风险描述 | 来源基线 | 影响 | 概率 | 优先级 |
|---------|----------|----------|------|------|--------|
| RISK-XXX-001 | {描述} | PRD/HLD/API | 高/中/低 | 高/中/低 | 高/中/低 |

## 独立测试层分配矩阵

| 风险/能力 | System Integration | E2E / Journey | Regression | Compatibility | Non-functional | Owner |
|-----------|--------------------|---------------|------------|---------------|----------------|-------|
| {能力/风险} | 主/辅/否 | 主/辅/否 | 主/辅/否 | 主/辅/否 | 主/辅/否 | {角色} |

## API Contract 验证策略

- **责任边界**：QA 主责批准 API Contract 的黑盒验证与回归；若开发/SDET 提供 provider-side contract suite，仅作为补充证据
- **验证范围**：{接口组 / 操作 / 验证点清单}
- **覆盖维度**：{路径/方法/参数/headers/请求字段/响应字段/状态码/错误语义/权限/幂等/兼容语义}
- **执行层与证据**：{System Integration / Regression / 证据要求}

## 阶段化执行规则

### 阶段定义

| 阶段 | 阶段目标 | 当前阶段必须完成 | 当前阶段不应执行 | 未就绪项状态 |
|------|----------|------------------|------------------|--------------|
| {阶段名} | {目标} | {内容} | {内容} | PASS / FAIL / BLOCKED / DEFERRED / N/A |

### 阶段与环境映射原则

- **阶段是硬约束**：必须先定义当前节点属于哪个测试阶段，再决定应该执行哪些测试。
- **环境是软边界**：环境用于承载该阶段所需能力与证据来源，不能直接替代阶段定义。
- **同一阶段可接受多个环境**：只要这些环境能满足该阶段的验证能力、数据条件和观测要求。
- **后续阶段门禁**：属于后续阶段的测试项，在当前阶段若环境未就绪，应标记为 `Blocked / Deferred`，而不是直接记为功能失败。

## 环境、数据、依赖策略

### 环境策略
- {环境说明}
- 必须写清：该环境服务于哪个测试阶段、提供哪些能力、是否只是推荐环境而非唯一环境

### 数据策略
- {数据准备/隔离/清理}

### 依赖策略
- {mock/stub/real dependency 边界}

### 观测与验证
- {日志/指标/trace/DB/事件}

## 开发内建验证前置条件

- **Unit Test**：由开发负责，状态/要求：{说明}
- **Code-level Integration Test**：由开发负责，状态/要求：{说明}
- **可选补充证据**：若开发/SDET 提供 provider-side contract suite / 调用脚本，记录状态：{说明}
- **说明**：批准 API Contract 的黑盒验证属于本测试策略 In-scope，不得作为上游前置条件排除

## 入口标准

- {标准 1}
- {标准 2}
- {当前阶段的入口前提}

## 出口标准

- {标准 1}
- {标准 2}
- {当前阶段的出口门槛}
- {后续阶段保留门禁的移交条件}

## 自动化与回归策略

### Smoke
- {内容}

### Critical Regression
- {内容}

### Compatibility Regression
- {内容}

## 假设、豁免、待确认项

| 类型 | 内容 | 影响 | Owner | 截止时间 |
|------|------|------|-------|----------|
| 假设/豁免/待确认 | {描述} | {影响} | {人/角色} | {日期} |
```
