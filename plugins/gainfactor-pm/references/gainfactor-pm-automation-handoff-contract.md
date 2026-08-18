# GainFactor-PM Automation Handoff Contract

这份契约用于把 `gainfactor-pm` 产出的 **approved Test Spec**，稳定交给 `gainfactor-pm-bot` 的 `$case-writing` 继续落成 GainFactor-PM 自动化资产。

## 目标

- 让 `test-spec-writer` 输出的不只是“自动化建议”，而是**结构化 downstream handoff**
- 让 `test-reviewer` 能判断一个 Test Spec 是否已经具备进入 `gainfactor-pm-bot` 的条件
- 让 `gainfactor-pm-case-writing` 不必每次从整篇 Test Spec 重新猜测如何拆 case

## 适用范围

- 上游：`gainfactor-pm` 的 `test-spec-writer`、`test-reviewer`、`guide`
- 下游：`gainfactor-pm-bot` 的 `case-writing`，以及后续的 `case` / `pipeline` / `trigger` / `execution`

## 强制规则

1. `test-spec-writer` 输出的 Test Spec 应始终包含 `## GainFactor-PM Automation Handoff` 章节
2. 即使当前**不**计划落到 GainFactor-PM，也不要省略该章节；请显式写 `status: not_planned`
3. 若 `status: ready`，则该 handoff 应足以让 `$case-writing` 直接开始工作，而不必重新通读整篇 Test Spec 才能判断拆分
4. 若 `status: partial`，允许继续进入 `$case-writing`，但必须把缺失信息显式列入 `open_questions`
5. `$case-writing` 读取 Test Spec 时，若发现该 handoff 存在，应优先按该 handoff 工作，而不是把整篇 Test Spec 当作唯一主输入

## 状态枚举

| 状态 | 含义 | 下游期望 |
|------|------|----------|
| `ready` | 已明确准备落到 GainFactor-PM，且拆分/Executor/relay/依赖等信息足够 | `guide` 可直接推荐 `$case-writing`；`test-reviewer` 可标记自动化下游已就绪 |
| `partial` | 有明确落地意图，但仍有信息缺口 | `guide` 可低一档置信度推荐 `$case-writing`；`test-reviewer` 应指出缺口；`case-writing` 需补充确认 |
| `not_planned` | 当前不计划落到 GainFactor-PM | 默认不推荐 `$case-writing`；保留文档/Runbook 主线 |

## Canonical 结构

```yaml
gainfactor_pm_automation_handoff:
  status: ready | partial | not_planned
  recommended_entrypoint: $case-writing | none
  source_test_spec:
    artifact_id: TSPEC-XXX
    version: v0.x
    status: approved | draft | in_review
  scenario_groups:
    - id: AUTO-001
      title: Contract black-box validation
      objective: Validate frozen contract semantics for submission and conclude paths
      source_case_ids: [CASE-001, CASE-002]
      priority: P0 | P1 | P2
      recommended_executor: pyres | postman | playwright | maven | gradle
      platform_case_strategy: single_case | split_cases
      pipeline_required: true
      suggested_platform_cases:
        - alias: LOGIN
          role: setup | action | assertion | cleanup | negative_path
          purpose: Prepare authenticated context
          consumes: [BASE_URL, USERNAME, PASSWORD]
          produces: [AUTH_TOKEN]
      dependencies:
        - { from: LOGIN, to: SUBMIT_TASK, condition: whenPassed }
      relay_map:
        - { from: LOGIN.AUTH_TOKEN, to: SUBMIT_TASK.AUTH_TOKEN }
      branching:
        - { from: SUBMIT_TASK, to: ASSERT_FAIL, condition: expect_fail }
      labels: [smoke, api, p0]
      runtime_hints:
        preferred_runtime: cloudprime
        notes: Use pyres for API assertions and JSON diff
  open_questions:
    - Confirm whether cleanup should be a dedicated platform case
```

## 字段说明

### Top-level

| 字段 | 必填 | 说明 |
|------|------|------|
| `status` | 是 | `ready / partial / not_planned` |
| `recommended_entrypoint` | 是 | 推荐进入 `$case-writing`，或明确 `none` |
| `source_test_spec` | 是 | 指向当前 Test Spec artifact，便于下游确认版本和批准状态 |
| `scenario_groups` | 是 | 供 `case-writing` 消费的最小拆分单元；`not_planned` 时可为空数组 |
| `open_questions` | 是 | 所有仍会影响自动化落地的问题；无则显式留空数组 |

### `scenario_groups[*]`

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | handoff 内部稳定 ID，便于 reviewer / bot 引用 |
| `title` | 是 | 该组验证目标的短标题 |
| `objective` | 是 | 业务/系统验证目标 |
| `source_case_ids` | 是 | 来自 Test Spec 的 `CASE-*` 清单 |
| `priority` | 是 | 对应 `P0 / P1 / P2` |
| `recommended_executor` | 是 | `gainfactor-pm-bot` 优先选择的 Executor |
| `platform_case_strategy` | 是 | `single_case` 或 `split_cases` |
| `pipeline_required` | 是 | 在 GainFactor-PM 中几乎总是 `true`；即使只有一个 platform case，也应明确写出 |
| `suggested_platform_cases` | 是 | 预期拆出的 platform case 形态；`single_case` 时通常只含一个 |
| `dependencies` | 否 | `from -> to -> condition` 形式的依赖 |
| `relay_map` | 否 | `上游输出 -> 下游输入` 形式的 relay 映射 |
| `branching` | 否 | `whenFailed` / `expect_fail` / cleanup branch 等 |
| `labels` | 否 | 便于注册和检索的标签建议 |
| `runtime_hints` | 否 | runtime、目录结构、工具链、凭证方式等补充说明 |

### `suggested_platform_cases[*]`

| 字段 | 必填 | 说明 |
|------|------|------|
| `alias` | 是 | 供 handoff 与 pipeline 设计复用的短别名 |
| `role` | 是 | `setup / action / assertion / cleanup / negative_path` |
| `purpose` | 是 | 该 platform case 的职责说明 |
| `consumes` | 是 | 预期输入变量名 |
| `produces` | 是 | 预期输出变量名；无输出时写空数组 |

## Ready 判定基线

若 `status: ready`，最低要求是：

- `source_test_spec.status = approved`
- 至少 1 个 `scenario_group`
- 每个 `scenario_group` 都有 `source_case_ids`
- 每个 `scenario_group` 都给出 `recommended_executor`
- 已说明 `platform_case_strategy`
- 已说明 `pipeline_required`
- 若存在跨 case 依赖或 relay，需要显式给出 `dependencies` / `relay_map`
- `open_questions` 为空数组，或仅剩不会阻塞首轮 case-writing 的非关键问题

## Partial 判定基线

若 `status: partial`，允许存在以下缺口：

- 仅给出场景组，尚未决定最终 `Executor`
- 已知需要 split，但 `suggested_platform_cases` 仍待细化
- 已知需要 pipeline，但 relay / branching 还未完全展开

但仍应满足：

- 已能看出哪些 `CASE-*` 会进入自动化落地
- 已能看出 automation 的主目标与优先级
- 所有阻塞点都在 `open_questions` 中显式列出

## Reviewer 使用方式

`test-reviewer` 检查该 section 时，按以下口径判断：

- 缺失整个 section：下游自动化 handoff 不明确
- `status: ready` 但缺少 executor / split / dependency / relay 关键字段：自动化 readiness 不成立
- `status: partial`：允许通过，但 reviewer 应明确指出还需要哪些补充才能进入 `$case-writing`
- `status: not_planned`：不把 `$case-writing` 作为默认推荐路径

## Bot 使用方式

`gainfactor-pm-case-writing` 读取该 section 时，应遵循：

1. 若 `status: ready`，把它作为**第一优先输入**
2. 若 `status: partial`，以它为基线，并集中追问 `open_questions`
3. 若 `status: not_planned`，默认不要自动进入 GainFactor-PM 落地，除非用户明确要求覆盖该决定
