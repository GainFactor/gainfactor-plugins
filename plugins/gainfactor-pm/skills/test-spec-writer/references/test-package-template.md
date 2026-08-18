# Test Spec / Test Case Package 模板

```markdown
# 测试规格：{项目/功能名称}

<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-spec-profile-v1
artifact:
  id: TSPEC-[DOMAIN]-001
  type: TEST_SPEC
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
- **LLD 基线**：{路径} v{版本}
- **Test Strategy**：{路径} v{版本}
- **Guardrails**：{路径} / N/A
- **状态**：Draft / Reviewed / Approved

## 范围

### In-scope
- {内容}

### Out-of-scope
- {内容}

### API Contract 验证范围
- **责任边界**：QA 主责批准 API Contract 的黑盒验证与回归；若开发/SDET 提供 provider-side contract suite，仅作为补充证据
- **验证点清单**：{接口组 / 操作 / 验证点}
- **覆盖维度**：{路径/方法/参数/headers/请求字段/响应字段/状态码/错误语义/权限/幂等/兼容语义}

### 开发内建验证前置条件
- **Unit Test**：{要求/状态}
- **Code-level Integration Test**：{要求/状态}
- **可选补充证据**：provider-side contract suite / 调用脚本：{要求/状态}
- **说明**：批准 API Contract 的黑盒验证属于本测试包 In-scope，不得仅作为上游前置条件排除

## 追溯矩阵

| 来源类型 | 来源 ID / 位置 | 测试项 | 状态 | 备注 |
|----------|----------------|--------|------|------|
| PRD / API / HLD / LLD / Risk | {ID 或位置} | {Case ID} | 已覆盖 / 部分覆盖 / 未覆盖 | {说明} |

## 覆盖率摘要

| 指标 | 分子定义 | 分母定义 | 覆盖率 | 未覆盖项 |
|------|----------|----------|--------|----------|
| 需求覆盖率 | 已被至少 1 个测试项追溯的 in-scope 需求数 | in-scope 需求总数 | {x/y = z%} | {ID 列表 / 无} |
| API Contract 覆盖率 | 已被至少 1 个测试项覆盖的 in-scope API Contract 验证点数 | in-scope API Contract 验证点总数 | {x/y = z%} | {验证点列表 / 无} |
| 风险覆盖率 | 已被至少 1 个测试项覆盖的 in-scope 风险数 | in-scope 风险总数 | {x/y = z%} | {ID 列表 / 无} |
| 高风险覆盖率 | 已被覆盖的高风险项数 | 高风险项总数 | {x/y = z%} | {ID 列表 / 无} |
| Must-not-regress 覆盖率 | 已被回归包覆盖的 must-not-regress 项数 | must-not-regress 项总数 | {x/y = z%} | {ID 列表 / 无} |
| 外部行为覆盖率 | 已被测试项覆盖的 in-scope 外部可观察行为数 | in-scope 外部可观察行为总数 | {x/y = z%} | {ID 列表 / 无} |
| 场景覆盖率 | 已覆盖场景数 | 已识别场景总数 | {x/y = z%} | {场景列表 / 无} |
| 必测 NFR 覆盖率 | 已设计验证方案的必测 NFR 项数 | 必测 NFR 项总数 | {x/y = z%} | {NFR 列表 / 无} |

### 统计口径说明

- 以上为**测试设计覆盖率**，不是代码覆盖率，也不是执行覆盖率
- 分母仅包含 in-scope 项
- 以下内容不进入分母：
  - Out-of-scope
  - 已批准豁免项
  - unit / code-level integration
  - 已明确由其他独立测试包承担且已引用的项
- 不允许只给一个综合总覆盖率，必须分项展示

## 测试矩阵

| 场景组 | 测试层次 | 优先级 | 必测 | 自动化候选 | 备注 |
|--------|----------|--------|------|------------|------|
| API 契约 / 主流程 / 分支 / 异常 / 边界 / 系统集成 / 兼容 / 非功能 | API / SYS / E2E / REG / COMPAT / NFT | P0 / P1 / P2 | 是/否 | 高/中/低 | {说明} |

## 详细测试用例

### {Case ID} - {用例名称}

- **来源追溯**：{PRD/API/HLD/LLD/Risk}
- **优先级**：P0 / P1 / P2
- **前置条件**：{内容}
- **数据准备**：{内容}
- **执行步骤**：
  1. {步骤}
  2. {步骤}
- **输入**：{内容}
- **预期结果**：{内容}
- **判定方式 / 断言点**：{内容}
- **清理动作**：{内容}
- **自动化建议**：{建议}
- **必需证据**：{日志/响应/事件/DB/截图/指标}

## 环境、数据、依赖

### 环境
- {环境说明}

### 数据
- {准备 / 隔离 / 清理}

### 依赖
- {mock / stub / sandbox / real dependency}

### 观测与证据
- {日志 / 指标 / trace / DB / 事件}

## 回归与执行建议

### Smoke
- {Case ID}

### API Contract Regression
- {Case ID}

### Critical Regression
- {Case ID}

### Compatibility Regression
- {Case ID}

### 非功能验证
- {范围与方法}

## GainFactor-PM Automation Handoff

> 即使当前不计划落到 GainFactor-PM，也要保留本节，并显式写 `status: not_planned`。字段定义见 `../../references/gainfactor-pm-automation-handoff-contract.md`。

```yaml
gainfactor_pm_automation_handoff:
  status: ready | partial | not_planned
  recommended_entrypoint: $case-writing | none
  source_test_spec:
    artifact_id: {TSPEC-ID}
    version: {vX.Y}
    status: approved | draft | in_review
  scenario_groups:
    - id: AUTO-{nnn}
      title: {场景组标题}
      objective: {验证目标}
      source_case_ids: [{CASE-ID}, {CASE-ID}]
      priority: P0 | P1 | P2
      recommended_executor: pyres | postman | playwright | maven | gradle
      platform_case_strategy: single_case | split_cases
      pipeline_required: true
      suggested_platform_cases:
        - alias: {短别名}
          role: setup | action | assertion | cleanup | negative_path
          purpose: {职责}
          consumes: [{ENV_VAR}]
          produces: [{OUTPUT_VAR}]
      dependencies:
        - { from: {ALIAS}, to: {ALIAS}, condition: whenPassed }
      relay_map:
        - { from: {ALIAS}.{OUTPUT}, to: {ALIAS}.{ENV} }
      branching:
        - { from: {ALIAS}, to: {ALIAS}, condition: whenFailed / expect_fail }
      labels: [{label}]
      runtime_hints:
        preferred_runtime: {cloudprime / 其他}
        notes: {限制/说明}
  open_questions:
    - {待确认项；无则留空数组}
```

## 假设、豁免、待确认项

| 类型 | 内容 | 影响 | Owner | 截止时间 |
|------|------|------|-------|----------|
| 假设 / 豁免 / 待确认 | {内容} | {影响} | {角色} | {日期} |
```
