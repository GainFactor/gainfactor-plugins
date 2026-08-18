---
description: Test strategy review, 测试策略评审。检查风险覆盖、独立测试分层、环境策略与门禁标准
argument-hint: <Test Strategy 路径> <PRD 路径> <API Contract 路径> <HLD 路径> [Guardrails 路径]
---

# Test Strategy Reviewer

启动测试策略评审流程。作为进入 LLD 和详细测试规格前的门禁，检查测试策略是否完整、可执行、无关键遗漏。

## 使用方式

提供测试策略和上游基线路径：

$ARGUMENTS

## 在研发流程中的位置

```text
Test Strategy → [Test Strategy Reviewer] → Test Strategy（准出）→ LLD → Test Spec
```

## 审查框架

采用四道门审查：

1. **Gate 1 - 基线与范围**：版本、范围、must-not-regress、豁免
2. **Gate 2 - 风险覆盖与测试分层**：高风险能力与分层合理性
3. **Gate 3 - 环境/数据/依赖**：执行可行性
4. **Gate 4 - 门禁与自动化**：入口/出口、回归与自动化策略

## 准出门槛

- **P0 = 0**
- **P1 = 0**
- **P2 ≤ 2**

## 必需产出

- 审查报告
- 准出证书（通过时）

## 强制脚本校验

在人工评审前必须先执行：

```bash
python3 plugins/gainfactor-pm/scripts/trace_lint.py --format json <Test Strategy 路径>
python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py --format json <PRD 路径> <Test Strategy 路径>
```

`trace-lint` blocking issue 和 `RTM001 / RTM002 / RTM003 / RTM004` 都按 `P0` 处理。

请提供 Test Strategy 路径开始评审。建议同时提供 PRD、API Contract、HLD 与 Guardrails。
