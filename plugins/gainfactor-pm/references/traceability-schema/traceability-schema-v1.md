# gainfactor-pm Traceability Schema v1 设计稿

## 1. 目标

这套 schema 用于给 `gainfactor-pm` 全链路文档提供统一、可脚本处理的追溯元数据契约，支持：

- 为 `USER_JOURNEY / PRD / HLD / LLD / Test Strategy / Test Spec` 提供统一的机器可读元数据
- 自动生成和校验 RTM（Requirements Traceability Matrix）
- 自动计算测试设计覆盖率
- 检查 ID 稳定性、引用合法性、漏项、孤儿项、未批准豁免项
- 允许分阶段接入：先接 `USER_JOURNEY / PRD`，再逐步接 `Test Strategy / Test Spec / HLD / LLD`

## 2. 非目标

v1 不解决以下问题：

- 不替代人类可读的正文文档；schema 只承载元数据，不承载完整叙述
- 不要求第一阶段就接入所有实体
- 不建模开发内建验证层的详细测试设计：
  - `unit`
  - `code-level integration`
  - `provider-side contract`
- 不要求第一阶段就产出完整 JSON Schema 实现；本稿先定义 canonical contract 和 profile

## 3. 设计原则

### 3.1 Workflow-first，不是 RTM-first

schema 先服务 `gainfactor-pm` 的文档流转，再服务最终 RTM 聚合。  
因此它必须支持：

- 文档内嵌元数据
- 渐进式接入
- profile 分层启用

### 3.2 稳定 ID 优先

所有可追溯对象必须有稳定 ID。  
ID 一旦发布，不应在同一条业务语义仍存在时被重写。

### 3.3 关系独立建模，不在上游对象里内嵌下游桶

不采用下面这种模式：

- `hld_info`
- `test_info`
- `risk_info`
- `change_request_info`

原因：

- 上游文档不应知道未来所有下游结构
- 容易造成重复字段和漂移
- 不利于 phased rollout

v1 采用统一的 `relations[]` 来表达追溯关系。

### 3.4 Human-first，Machine-readable

正文仍由人阅读；schema 只负责：

- 稳定提取
- 稳定校验
- 稳定聚合

### 3.5 显式 scope 和 waiver

脚本计算覆盖率和 RTM 时，必须能区分：

- `in-scope`
- `out-of-scope`
- `approved waiver`

否则覆盖率分母不稳定。

## 4. Canonical Envelope

v1 的 canonical 元数据块结构如下：

```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: prd-profile-v1

artifact:
  id: PRD-CHECKOUT-001
  type: PRD
  title: 优惠券结算
  status: draft
  owners:
    - product.checkout
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - BRD-CHECKOUT-001
    - JOURNEY-CHECKOUT-001

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

## 5. 顶层对象定义

### 5.1 `schema`

用于描述当前元数据块本身。

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 固定值：`gainfactor-pm-traceability` |
| `version` | 是 | schema 版本，v1 从 `1.0.0` 开始 |
| `profile` | 是 | 当前文档启用的 profile，例如 `prd-profile-v1` |

### 5.2 `artifact`

用于描述当前文档。

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 文档 ID，例如 `PRD-CHECKOUT-001` |
| `type` | 是 | 文档类型 |
| `title` | 是 | 文档标题 |
| `status` | 是 | `draft` / `in_review` / `approved` / `deprecated` / `archived` |
| `owners` | 否 | 责任团队或责任人列表 |
| `created_at` | 是 | `YYYY-MM-DD` |
| `updated_at` | 是 | `YYYY-MM-DD` |
| `source_documents` | 否 | 上游文档 ID 列表 |

`artifact.type` v1 保留如下枚举：

- `BRD`
- `USER_JOURNEY`
- `PRD`
- `API_CONTRACT`
- `HLD`
- `LLD`
- `TEST_STRATEGY`
- `TEST_SPEC`
- `RUNBOOK`

### 5.3 `entities`

`entities` 是按类型分桶的业务对象集合。v1 先定义完整 superset，但允许 profile 只启用其中一部分：

- `requirements`
- `risks`
- `must_not_regress`
- `external_behaviors`
- `decisions`
- `flows`
- `test_cases`

### 5.4 `relations`

所有跨对象追溯关系都放在 `relations[]` 里，而不是分散在对象内部的阶段特定字段里。

### 5.5 `waivers`

用于承载经批准的豁免项。  
覆盖率脚本和 reviewer 必须识别 waiver，而不是把豁免项算成“静默漏测”。

## 6. ID 规范

### 6.1 文档 ID

| 类型 | 前缀 | 示例 |
|------|------|------|
| BRD | `BRD-` | `BRD-CHECKOUT-001` |
| User Journey | `JOURNEY-` | `JOURNEY-CHECKOUT-001` |
| PRD | `PRD-` | `PRD-CHECKOUT-001` |
| API Contract | `API-` | `API-CHECKOUT-001` |
| HLD | `HLD-` | `HLD-CHECKOUT-001` |
| LLD | `LLD-` | `LLD-CHECKOUT-001` |
| Test Strategy | `TSTRAT-` | `TSTRAT-CHECKOUT-001` |
| Test Spec | `TSPEC-` | `TSPEC-CHECKOUT-001` |
| Runbook | `RUNBOOK-` | `RUNBOOK-CHECKOUT-001` |

### 6.2 实体 ID

| 实体 | 前缀 | 示例 |
|------|------|------|
| Requirement | `REQ-` | `REQ-CHECKOUT-001` |
| Risk | `RISK-` | `RISK-CHECKOUT-001` |
| Must-not-regress | `MR-` | `MR-CHECKOUT-001` |
| External Behavior | `BEH-` | `BEH-CHECKOUT-001` |
| Decision | `DEC-` | `DEC-CHECKOUT-001` |
| Flow | `FLOW-` | `FLOW-CHECKOUT-001` |
| Test Case | `CASE-` | `CASE-CHECKOUT-001` |
| Waiver | `WVR-` | `WVR-CHECKOUT-001` |
| Relation | `REL-` | `REL-CHECKOUT-001` |

### 6.3 ID 命名规则

- 使用全大写前缀
- 业务域使用大写短名或大写下划线风格
- 尾号使用三位数字，按同一文档内出现顺序递增
- 已发布对象不得因重排或改写而换 ID

推荐正则：

```text
^[A-Z]+-[A-Z0-9_]+-\d{3}$
```

## 7. 实体模型

### 7.1 通用字段

除非 profile 明确裁剪，所有实体都应支持以下通用字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 稳定实体 ID |
| `title` | 是 | 短标题 |
| `statement` | 是 | 规范化陈述 |
| `status` | 是 | `proposed` / `approved` / `deprecated` / `replaced` |
| `scope` | 是 | `in` / `out` |
| `owners` | 否 | 责任人/责任团队 |
| `tags` | 否 | 标签 |
| `source_refs` | 否 | 证据来源列表 |
| `notes` | 否 | 备注 |

`source_refs[]` 对象结构：

| 字段 | 必填 | 说明 |
|------|------|------|
| `artifact_id` | 是 | 来源文档 ID |
| `section` | 否 | 章节标识 |
| `locator` | 否 | 行号、锚点、URL、文件路径等 |
| `note` | 否 | 简短说明 |

### 7.2 `requirements[]`

PRD 第一阶段唯一必须落地的实体。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `class` | 是 | `functional` / `non_functional` |
| `priority` | 是 | `P0` / `P1` / `P2` / `P3` |
| `acceptance_criteria` | 是 | 字符串数组，至少 1 条 |
| `dependencies` | 否 | 依赖的其他 Requirement ID 或外部系统名 |

### 7.3 `risks[]`

供 `test-strategy` 阶段使用。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `level` | 是 | `critical` / `high` / `medium` / `low` |
| `likelihood` | 否 | `high` / `medium` / `low` |
| `impact` | 否 | 风险影响描述 |

### 7.4 `must_not_regress[]`

用于定义“本轮必须不退化”的行为或能力。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `priority` | 是 | `P0` / `P1` / `P2` / `P3` |

### 7.5 `external_behaviors[]`

用于定义用户或外部系统可观察到的行为单元，供测试覆盖统计使用。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `actor` | 否 | 发起者 |
| `trigger` | 否 | 触发条件 |
| `observable_outcome` | 否 | 对外可观察结果 |

### 7.6 `decisions[]`

用于 HLD 阶段沉淀架构/设计决策。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `decision` | 是 | 决策结论 |
| `rationale` | 否 | 决策理由 |

### 7.7 `flows[]`

用于承载流程、状态流转、模块级交互流。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `kind` | 是 | `user_journey` / `system_flow` / `state_transition` / `module_interaction` |

### 7.8 `test_cases[]`

供 `test-spec` 阶段使用。  
这里只承载独立测试包范围内的测试项，不承载开发内建测试层。

附加字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `layer` | 是 | `system_integration` / `e2e` / `regression` / `compatibility` / `non_functional` |
| `priority` | 是 | `P0` / `P1` / `P2` / `P3` |
| `automation` | 否 | `must` / `should` / `manual_ok` |
| `preconditions` | 否 | 前置条件列表 |
| `expected_evidence` | 否 | 执行后应产出的证据 |

## 8. 关系模型

`relations[]` 中每条关系结构如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | `REL-*` |
| `type` | 是 | 关系类型 |
| `from` | 是 | 起点对象 ID |
| `to` | 是 | 终点对象 ID |
| `status` | 否 | `active` / `deprecated` |
| `note` | 否 | 说明 |

v1 关系类型：

| 关系类型 | 语义 | 示例 |
|----------|------|------|
| `derived_from` | 来源于上游对象 | `REQ -> BRD/JOURNEY` |
| `depends_on` | 依赖另一个对象 | `REQ -> REQ` |
| `refines` | 细化上游对象 | `FLOW -> REQ`，`DEC -> REQ` |
| `verifies` | 用于验证目标对象 | `CASE -> REQ/RISK/MR/BEH` |
| `mitigates` | 用于缓解风险 | `DEC/CASE -> RISK` |

约束：

- `relations[]` 里所有 `from/to` 都必须引用已声明对象 ID 或 `artifact.source_documents` 中存在的文档 ID
- 同一条关系不应重复建模
- `verifies` 只允许由 `CASE-*` 指向被验证对象

## 9. Waiver 模型

`waivers[]` 每条豁免结构如下：

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | `WVR-*` |
| `target_ids` | 是 | 被豁免对象 ID 列表 |
| `reason` | 是 | 豁免理由 |
| `status` | 是 | `draft` / `approved` / `expired` / `revoked` |
| `approved_by` | 否 | 批准人 |
| `approved_at` | 否 | 日期 |
| `expires_at` | 否 | 日期 |
| `note` | 否 | 补充说明 |

脚本和 reviewer 的默认行为：

- `status != approved` 的 waiver 不生效
- 已过期 waiver 不生效
- 生效 waiver 对应对象可从覆盖率分母中排除，但必须在报告中显式列出

## 10. Profiles

### 10.1 Canonical Schema vs Profile

v1 一次性定义完整 canonical schema。  
实际 writer/reviewer skill 通过 profile 启用子集。

### 10.2 `prd-profile-v1`

PRD 阶段的基础 profile。

约束：

- `artifact.type` 必须为 `PRD`
- `entities.requirements` 必须存在且至少 1 条
- `requirements[]` 必填字段：
  - `id`
  - `class`
  - `title`
  - `statement`
  - `priority`
  - `status`
  - `scope`
  - `acceptance_criteria`
- `entities.risks`
- `entities.must_not_regress`
- `entities.external_behaviors`
- `entities.decisions`
- `entities.flows`
- `entities.test_cases`
- `relations`
- `waivers`

在 `prd-profile-v1` 中都允许为空，但建议显式保留空数组，方便脚本稳定提取。

### 10.3 `test-strategy-profile-v1`

用于承载测试策略阶段的独立测试建模结果。

约束：

- `artifact.type` 必须为 `TEST_STRATEGY`
- 以下桶必须存在，即使为空数组：
  - `requirements`
  - `risks`
  - `must_not_regress`
  - `external_behaviors`
  - `decisions`
  - `flows`
  - `test_cases`
- `entities.risks[]` 每条至少包含：
  - `id`
  - `title`
  - `statement`
  - `status`
  - `scope`
  - `level`
- `entities.must_not_regress[]` 每条至少包含：
  - `id`
  - `title`
  - `statement`
  - `status`
  - `scope`
  - `priority`
- `entities.external_behaviors[]` 每条至少包含：
  - `id`
  - `title`
  - `statement`
  - `status`
  - `scope`
- `risks / must_not_regress / external_behaviors` 三者合计至少应有 1 条建模对象
- 推荐使用 `relations[].type=derived_from` / `refines` 将这些对象追溯到 `REQ-*` 或上游文档 ID

### 10.4 `journey-profile-v1`

用于承载 `uc-interviewer` 产出的正式 User Journey baseline。

约束：

- `artifact.type` 必须为 `USER_JOURNEY`
- `artifact.id` 必须使用 `JOURNEY-` 前缀
- `artifact.source_documents` 至少包含 1 个 `BRD-*` baseline ID
- 以下桶必须存在，即使为空数组：`requirements`、`risks`、`must_not_regress`、`external_behaviors`、`decisions`、`flows`、`test_cases`
- `entities.flows` 必须存在且至少 1 条
- 每条 `FLOW-*` 必须包含：`id`、`title`、`statement`、`status`、`scope`、`kind`、`priority`
- `flows[].kind` 必须为 `user_journey`
- 每个 `FLOW-*` 至少应有 1 条 outgoing relation（`derived_from` / `refines` / `depends_on`），指向 `BRD-*`、`REQ-*`、其他 `FLOW-*` 或上游 `JOURNEY-*`
- 示例见 `journey-profile-v1.example.yaml`

### 10.5 `test-spec-profile-v1`

用于承载详细测试规格与测试用例包。

约束：

- `artifact.type` 必须为 `TEST_SPEC`
- 以下桶必须存在，即使为空数组：
  - `requirements`
  - `risks`
  - `must_not_regress`
  - `external_behaviors`
  - `decisions`
  - `flows`
  - `test_cases`
- `entities.test_cases` 必须存在且至少 1 条
- `entities.test_cases[]` 每条至少包含：
  - `id`
  - `title`
  - `statement`
  - `status`
  - `scope`
  - `layer`
  - `priority`
- `layer` 只允许：
  - `system_integration`
  - `e2e`
  - `regression`
  - `compatibility`
  - `non_functional`
- 每个 `CASE-*` 至少应有 1 条 outgoing relation：
  - `verifies`
  - 或 `mitigates`
- 推荐把被验证对象建模为：
  - `REQ-*`
  - `RISK-*`
  - `MR-*`
  - `BEH-*`

### 10.6 `hld-profile-v1`

用于承载高层技术设计的架构决策与关键流程。HLD 是连接需求和实现的关键桥梁，其 profile 确保架构决策可追溯到上游需求。

约束：

- `artifact.type` 必须为 `HLD`
- 以下桶必须存在，即使为空数组：`requirements`、`risks`、`must_not_regress`、`external_behaviors`、`decisions`、`flows`、`test_cases`
- `entities.decisions[]` 每条至少包含：`id`、`title`、`statement`、`status`、`scope`、`decision`、`rationale`
- `entities.flows[]` 每条至少包含：`id`、`title`、`statement`、`status`、`scope`、`kind`
- `flows[].kind` 允许值：`user_journey` / `system_flow` / `state_transition`
- `decisions` 与 `flows` 合计至少应有 **1 条**建模对象
- 每个 `DEC-*` / `FLOW-*` 至少应有 1 条 outgoing relation（`refines` 或 `derived_from`），指向 `REQ-*` 或上游 artifact ID

### 10.7 `lld-profile-v1`

用于承载低层设计的模块级决策与模块交互流程。LLD 更接近实现层，追溯目标包括 HLD 层的 `DEC-*` / `FLOW-*`。

约束：

- `artifact.type` 必须为 `LLD`
- 以下桶必须存在，即使为空数组：`requirements`、`risks`、`must_not_regress`、`external_behaviors`、`decisions`、`flows`、`test_cases`
- `entities.decisions[]` 每条至少包含：`id`、`title`、`statement`、`status`、`scope`、`decision`、`rationale`
- `entities.flows[]` 每条至少包含：`id`、`title`、`statement`、`status`、`scope`、`kind`
- `flows[].kind` 允许值：`user_journey` / `system_flow` / `state_transition` / `module_interaction`
- `decisions` 与 `flows` 合计至少应有 **1 条**建模对象
- 每个 `DEC-*` / `FLOW-*` 至少应有 1 条 outgoing relation（`refines` 或 `derived_from`），指向 `DEC-*` / `FLOW-*` / `REQ-*` 或上游 artifact ID
- LLD Manifest（模块选择/排除列表）建议在 `artifact.notes` 或 `entities` 的 `notes` 字段中体现，供下游 test-spec-writer 程序化消费

## 11. Markdown 内嵌约定

为了不引入额外 sidecar 文件，schema 元数据块应直接嵌入文档正文，并使用稳定边界标记。

推荐格式：

````markdown
<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: prd-profile-v1
artifact:
  ...
entities:
  ...
relations: []
waivers: []
```
<!-- TRACEABILITY-METADATA:END -->
````

脚本只解析标记间的 YAML，不解析正文自由文本。

## 12. 自动化目标

基于这套 schema，后续脚本至少应支持：

### 12.1 `trace-lint`

详细 I/O 契约见：`trace-lint-contract-v1.md`

检查：

- schema/profile 是否合法
- ID 是否唯一
- 必填字段是否存在
- 枚举值是否合法
- 关系引用是否存在
- waiver 是否有效

### 12.2 `trace-build-rtm`

详细 I/O 契约见：`trace-build-rtm-contract-v1.md`

输入：

- 一个或多个带 traceability block 的文档

输出：

- 汇总 RTM
- orphan entity 列表
- 未被覆盖对象列表
- 重复或冲突关系

### 12.3 `trace-check-coverage`

重点服务 `test-spec`：

- 需求覆盖率
- 风险覆盖率
- 高风险覆盖率
- Must-not-regress 覆盖率
- 外部行为覆盖率
- 场景覆盖率
- 必测 NFR 覆盖率

## 13. 实施顺序

### 阶段 1

- `uc-interviewer` 产出 `journey-profile-v1`
- `prd-writer` 产出 `prd-profile-v1`
- `prd-reviewer` 校验 `REQ-*` 是否完整、唯一、稳定

### 阶段 2

- `test-strategy-writer` 接入 `RISK-*` / `MR-*` / `BEH-*`
- `test-strategy-reviewer` 校验这些对象和边界

### 阶段 3

- `test-spec-writer` 接入 `CASE-*` 和 `verifies` 关系
- `test-reviewer` 根据 schema 计算 coverage 和 gate

### 阶段 4

- 视需要接入 `HLD/LLD`
- 引入 `DEC-*` / `FLOW-*` / `refines`

## 14. 关键设计结论

这套 v1 的核心不是“先把完整 RTM 文档做出来”，而是先建立一个稳定、轻量、可渐进启用的追溯契约：

- **schema 一次定义完整**
- **profile 分阶段启用**
- **第一阶段只强制 PRD**
- **所有跨阶段追溯统一走 relations**
- **测试团队只对独立测试包范围建模，不背开发内建验证层责任**
