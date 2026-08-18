# LLD review report and Approval Certificate Template

This document provides the standard output template for LLD review.

---

## Review Report Template

### Full Report (General)

```markdown
#LLD Review Report

## Basic Information

| Project | Content |
|------|------|
| **LLD Documentation** | {file path} |
| **PRD Baseline** | {file path} v{version} |
| **HLD Baseline** | {file path} v{version} |
| **API Contract** | {file path} v{version} |
| **Guardrails** | {file path} / N/A |
| **Review Time** | {YYYY-MM-DD HH:MM} |
| **Review Round** | Round {N} |
| **Review Conclusion** | 🟢 Pass / 🔴 Fail |

---

## Problem statistics

| Level | Quantity | Threshold | Status |
|------|------|------|------|
| P0 (Block) | {n} | = 0 | ✅ Passed / ❌ Failed |
| P1 (Severe) | {n} | = 0 | ✅ Pass / ❌ Fail |
| P2 (recommended) | {n} | ≤ 2 | ✅ Passed / ❌ Failed |

---

## Gate 1: Baseline and Manifest Check

### Baseline reference checking

| Check Item | Result | Evidence Location | Question |
|--------|------|----------|------|
| PRD version annotation | ✅/⚠️/❌ | LLD:{Chapter} | {Problem description} |
| HLD version annotation | ✅/⚠️/❌ | LLD:{chapter} | {problem description} |
| Contract version annotation | ✅/⚠️/❌ | LLD:{Chapter} | {Problem description} |

### Manifest integrity check

| Module | Status | N/A Reason | Check Result |
|------|------|----------|----------|
| Core | Included | — | ✅ |
| API Contract | Included | — | ✅ |
| Storage & Migration | Excluded | {Reason} | ✅/⚠️ |
| Async/Event | Excluded | {Reason} | ✅/⚠️ |
| Infra/IaC | Included | — | ✅ |
| Observability | Included | — | ✅/⚠️ |
| Security/Compliance | Excluded | {Reason} | ✅/⚠️ |
| Deployment/Release | Included | — | ✅/⚠️ |
| Frontend UX | Excluded | {Reason} | ✅/⚠️ |
| External Integration | Excluded | {Reason} | ✅/⚠️ |
| SDK/Library | Excluded | {Reason} | ✅/⚠️ |

### Guardrails Coverage Check

| Guardrail Requirements | LLD Coverage Locations | Results |
|----------------|--------------|------|
| {Requirement 1} | LLD:{Chapter} | ✅/❌ |
| {Requirement 2} | LLD:{Chapter} | ✅/❌ |

### New boundary detection

| Test items | Results | Evidence |
|--------|------|------|
| Introduction of new services | ✅ None / ❌ Yes | {Description of evidence} |
| New interface introduced | ✅ None / ❌ Yes | {Description of evidence} |
| New boundary introduction | ✅ None / ❌ Yes | {Description of evidence} |

**Gate 1 Conclusion**: ✅ Passed / ❌ P0 Blocked

---

## Gate 2: Consistency and Drift Detection

### HLD→LLD coverage table

| HLD design decisions | LLD coverage locations | Status | Description |
|--------------|-------------|------|------|
| HLD:{Chapter} {Decision Description} | LLD:{Chapter} | ✅ Covered | — |
| HLD:{Chapter} {Decision description} | LLD:{Chapter} | ⚠️ Partial coverage | {Description} |
| HLD:{Chapter} {Decision Description} | — | ❌ Not Covered | {Description} |

**Coverage**: {Number covered}/{Total} = {Percent}%

### List of drift issues

| # | Type | HLD Location | LLD Location | Description | Severity |
|---|------|----------|----------|------|--------|
| 1 | Missing | HLD:{location} | — | {description} | P0 |
| 2 | Expansion | — | LLD:{location} | {description} | P1 |
| 3 | Transformation | HLD:{Position} | LLD:{Position} | {Description} | P1 |
| 4 | Downgrade | HLD:{location} | LLD:{location} | {description} | P1 |

### Contract consistency check

| Interface | Contract Definition | LLD Definition | Results | Question |
|------|--------------|----------|------|------|
| {Interface name} | Contract:{Location} | LLD:{Location} | ✅/❌ | {Question} |

**Gate 2 Conclusion**: ✅ No drift / ⚠️ Drift present

---

## Gate 3: Module integrity check

| Module | Status | Required | Missing | Severity |
|------|------|--------|--------|--------|
| Core | Included | 5/5 | — | — |
| API Contract | Included | 3/3 | — | — |
| Storage & Migration | Included | 4/4 | — | — |
| Async/Event | Included | 4/4 | — | — |
| Infra/IaC | Included | 3/3 | — | — |
| Observability | Included | 4/4 | — | — |
| Security/Compliance | Included | 3/3 | — | — |
| Deployment/Release | Included | 3/3 | — | — |
| Frontend UX | Included | 4/4 | — | — |
| External Integration | Included | 3/3 | — | — |
| SDK/Library | Included | 3/3 | — | — |

**Gate 3 Conclusion**: ✅ Complete / ⚠️ Missing

---

## Gate 4: Feasibility and Risk Assessment

| Assessment Item | Result | Evidence Location | Question |
|--------|------|----------|------|
| Key process pseudocode | ✅/⚠️/❌ | LLD:{location} | {question} |
| Error handling completeness | ✅/⚠️/❌ | LLD:{location} | {issue} |
| Concurrency/Transactions/Impotent | ✅/⚠️/❌ | LLD:{Location} | {Question} |
| Test strategy feasibility | ✅/⚠️/❌ | LLD:{location} | {question} |
| Observational Design | ✅/⚠️/❌ | LLD:{Location} | {Question} |
| Publishing Policy | ✅/⚠️/❌ | LLD:{Location} | {Question} |

**Gate 4 Conclusion**: ✅ Achievable / ⚠️ Risky

---

## Question list summary

### 🔴 P0 blocking problem (must be fixed)

| # | Gate | Problem Description | Evidence Location | Suggested Modifications |
|---|------|----------|----------|----------|
| 1 | Gate 1 | {Description} | LLD:{Location} | {Suggestion} |
| 2 | Gate 2 | {Description} | HLD:{Location} vs LLD:{Location} | {Suggestion} |

### 🟡 P1 serious problem (must be fixed)

| # | Gate | Problem Description | Evidence Location | Suggested Modifications |
|---|------|----------|----------|----------|
| 1 | Gate 2 | {Description} | LLD:{Location} | {Suggestion} |
| 2 | Gate 3 | {Description} | LLD:{Location} | {Suggestion} |

### 🔵 P2 suggested question (optional optimization)

| # | Gate | Problem Description | Evidence Location | Suggested Modifications |
|---|------|----------|----------|----------|
| 1 | Gate 4 | {Description} | LLD:{Location} | {Suggestion} |

---

## Release decision

### Exit threshold inspection

| Threshold | Requirement | Actual | Status |
|------|------|------|------|
| P0 | = 0 | {n} | ✅/❌ |
| P1 | = 0 | {n} | ✅/❌ |
| P2 | ≤ 2 | {n} | ✅/❌ |

### in conclusion

**🟢 Passed**: Meets the approval standards and can enter the code implementation stage.

or

**🔴 Failed**: There are {n} P0 issues and {n} P1 issues, which need to be repaired and reviewed.

---

## Next step

### If passed
- Enter the code implementation stage
- Keep this report as a design baseline
- Refer to LLD design when implementing

### If not passed
1. LLD author fixes the following issues:
- {Question 1}
- {Question 2}
2. After the repair is completed, initiate a review (round +1)
3. The review will re-execute the four-door inspection
```

---

## Approval Certificate Template

### Output when passed

```markdown
#✅ LLD approval certificate

---

## Basic Information

| Project | Content |
|------|------|
| **LLD Documentation** | {file path} |
| **PRD Baseline** | {file path} v{version} |
| **HLD Baseline** | {file path} v{version} |
| **API Contract** | {file path} v{version} |
| **Exact time** | {YYYY-MM-DD HH:MM} |
| **Review Rounds** | {N} rounds in total |
| **Review Conclusion** | 🟢 **Passed** |

---

## Review Process

| Round | Date | P0 | P1 | P2 | Conclusion |
|------|------|----|----|----| -----|
| 1 | {YYYY-MM-DD} | 2 | 3 | 1 | 🔴 Fail |
| 2 | {YYYY-MM-DD} | 0 | 1 | 2 | 🔴 Fail |
| 3 | {YYYY-MM-DD} | 0 | 0 | 1 | 🟢 Pass |

---

## Consistency confirmation

- ✅ HLD→LLD coverage 100%
- ✅ No missing requirements (all covered by HLD design)
- ✅ No unlabeled demand inflation
- ✅ No need to deform
- ✅ No quality downgrade
- ✅ API Contract 100% consistent

---

## Confirmation of passing the threshold

| Threshold | Requirement | Actual | Status |
|------|------|------|------|
| P0 | = 0 | 0 | ✅ |
| P1 | = 0 | 0 | ✅ |
| P2 | ≤ 2 | {n} | ✅ |

---

## Review coverage

- ✅ **Gate 1**: Baseline and Manifest checks completed
- ✅ **Gate 2**: Consistency and drift detection completed
- ✅ **Gate 3**: Module integrity check completed
- ✅ **Gate 4**: Feasibility and risk assessment completed

---

## Legacy Suggestions (P2)

The following issues do not block release and are recommended to be optimized during the implementation phase:

| # | Question | Suggestion |
|---|------|------|
| 1 | {P2 problem description} | {Optimization suggestions} |

---

## Confirmation of accurate departure

This LLD has been fully reviewed by **lld-reviewer** and meets the approval standards.

### ✅ You can enter the code implementation stage

---

**Reviewer**: lld-reviewer

**Accurate signature**: `PASSED-{YYYYMMDD}-{First 6 digits of MD5 (LLD file name)}`

Example: `PASSED-20250115-a3f2b1`
```

---

## Blocking report template (Gate 1 P0)

When there is a P0 problem in Gate 1, the review is immediately stopped and a simplified report is output:

```markdown
# LLD Audit Report - Gate 1 Blocked

## Basic Information

| Project | Content |
|------|------|
| **LLD Documentation** | {file path} |
| **Review Time** | {YYYY-MM-DD HH:MM} |
| **Review Conclusion** | 🔴 **Gate 1 Blocking** |

---

## Gate 1 blocking reason

| # | Problem | Severity | Description |
|---|------|--------|------|
| 1 | {Problem description} | P0 | {Detailed description} |

---

## Next step

1. Fix Gate 1 P0 problem
2. Reinitiate LLD review
3. Review will restart from Gate 1

---

**Note**: Gate 2/3/4 is not executed due to P0 blocking problem in Gate 1.
```

---

## Instructions for use

1. **Select Template**: Select the corresponding template based on the review results
2. **Fill content**: Replace `{placeholder}` with actual content
3. **Keep Format**: Strictly follow the table and chapter structure
4. **Evidence Reference**: All questions must refer to specific locations (e.g. `LLD:3.2`, `HLD:4.1`)
