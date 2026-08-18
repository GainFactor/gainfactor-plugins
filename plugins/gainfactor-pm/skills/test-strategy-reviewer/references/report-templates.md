# Test Strategy 审查模板

## 审查报告模板

```markdown
# Test Strategy 审查报告

## 基本信息

| 项目 | 内容 |
|------|------|
| **Strategy 文档** | {路径} |
| **PRD 基线** | {路径} v{版本} |
| **API Contract 基线** | {路径} v{版本} |
| **HLD 基线** | {路径} v{版本} |
| **Guardrails** | {路径} / N/A |
| **审查轮次** | 第 {N} 轮 |
| **审查结论** | 🟢 通过 / 🔴 不通过 |

## 脚本校验摘要

| 检查 | 命令 | 结果 | 备注 |
|------|------|------|------|
| Lint | `python3 <gainfactor-pm-plugin-root>/scripts/trace_lint.py --format json {strategy_path}` | PASS / FAIL | {关键 issue / 无} |
| RTM 聚合 | `python3 <gainfactor-pm-plugin-root>/scripts/trace_build_rtm.py --format json {prd_path} {strategy_path}` | PASS / FAIL | {关键 issue / 无} |

## 问题统计

| 级别 | 数量 | 门槛 | 状态 |
|------|------|------|------|
| P0 | {n} | = 0 | ✅/❌ |
| P1 | {n} | = 0 | ✅/❌ |
| P2 | {n} | ≤ 2 | ✅/❌ |

## Gate 1：基线与范围
- {结论与证据}

## Gate 2：风险覆盖与独立测试分层
- {结论与证据}

## Gate 3：环境/数据/依赖
- {结论与证据}

## Gate 4：门禁与自动化
- {结论与证据}

## 问题清单

### P0
- {问题}（证据：{位置}）

### P1
- {问题}（证据：{位置}）
- {缺少阶段化执行规则 / 把后续阶段门禁误记为当前阶段失败 / 用环境替代阶段定义}（证据：{位置}）

### P2
- {问题}（证据：{位置}）

## 放行结论

- **通过**：可作为 `test-spec-writer` 的基线
或
- **不通过**：修复后复审
```

## 准出证书模板

```markdown
# ✅ Test Strategy 准出证书

- **Strategy 文档**：{路径}
- **基线**：PRD/API/HLD/Guardrails
- **审查轮次**：第 {N} 轮
- **结论**：通过
- **脚本校验**：`trace-lint` 通过，`trace-build-rtm` 无 build error
- **阶段说明**：已明确当前阶段出口与后续阶段环境级门禁边界
- **说明**：该测试策略可作为详细测试规格与测试用例包的基线
```
