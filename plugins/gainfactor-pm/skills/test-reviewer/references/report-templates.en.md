# Test Reviewer Template

## Review Report Template

```markdown
# Test review report

## Basic Information

| Project | Content |
|------|------|
| **Test Package** | {path} |
| **Review Mode** | Design preparation review / test access control before release |
| **PRD Baseline** | {path} v{version} |
| **API Contract Baseline** | {path} v{version} |
| **HLD Baseline** | {path} v{version} |
| **LLD Baseline** | {path} v{version} |
| **Test Strategy** | {path} v{version} |
| **Review Conclusion** | 🟢 Pass / 🔴 Fail |

## Script verification summary

| Check | Command | Result | Notes |
|------|------|------|------|
| Lint | `python3 <gainfactor-pm-plugin-root>/scripts/trace_lint.py --format json {test_spec_path}` | PASS / FAIL | {critical issue / none} |
| RTM aggregation | `python3 <gainfactor-pm-plugin-root>/scripts/trace_build_rtm.py --format json {prd_path} {test_strategy_path} {test_spec_path}` | PASS / FAIL | {critical issue / none} |

## Problem statistics

| Level | Quantity | Threshold | Status |
|------|------|------|------|
| P0 | {n} | = 0 | ✅/❌ |
| P1 | {n} | = 0 | ✅/❌ |
| P2 | {n} | ≤ 2 | ✅/❌ |

## Coverage Summary

| Metrics | Results | Thresholds | Status | Not Covered |
|------|------|------|------|----------|
| Demand Coverage | {x/y = z%} | = 100% | ✅/❌ | {List/None} |
| API Contract Coverage | {x/y = z%} | = 100% | ✅/❌ | {List/None} |
| Risk coverage | {x/y = z%} | Explicit display | ✅/❌ | {List / None} |
| High Risk Coverage | {x/y = z%} | = 100% | ✅/❌ | {List/None} |
| Must-not-regress coverage | {x/y = z%} | = 100% | ✅/❌ | {list/none} |
| External behavior coverage | {x/y = z%} | Explicit display | ✅/❌ | {List / None} |
| scene coverage | {x/y = z%} | explicit display | ✅/❌ | {list/none} |
| Must-test NFR coverage | {x/y = z%} | = 100% | ✅/❌ | {List/None} |

### RTM Aggregation Summary

| Indicators | Results |
|------|------|
| Requirement Covered / Total | {x / y} |
| Risk Covered / Total | {x / y} |
| Must-not-regress Covered / Total | {x / y} |
| External Behavior Covered / Total | {x / y} |
| Test Cases | {n} |
| Unresolved Relation Targets | {n} |
| Orphan Entities | {n} |

## Gate 1: Baseline and traceback
- {Conclusion and Evidence}

## Gate 2: Coverage and Drift
- {Conclusion and Evidence}

## Gate 3: Enforceability and Evidence Design
- {Conclusion and Evidence}

## Gate 4: Execution Evidence and Residual Risk
- {Conclusion and Evidence}

## Question list

### P0
- {Question} (Evidence: {Location})

### P1
- {Question} (Evidence: {Location})

### P2
- {Question} (Evidence: {Location})

## in conclusion

- **Passed**: {Test design approved/Test access control passed}
or
- **Fail**: Review after fixing the problem
```

## Approval Certificate Template

```markdown
#✅ Test approval certificate

- **Test Package**: {path}
- **Review Mode**: Design preparation review / test access control before release
- **Conclusion**: Passed
- **Script verification**: `trace-lint` passed, `trace-build-rtm` had no build error
- **Description**: {can enter the test execution phase / can enter the release preparation phase}
```
