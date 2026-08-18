# HLD Review Report and Approval Certificate Templates

## Review Report Template

```markdown
# HLD Review Report

## Basic Information
| Item | Content |
|------|---------|
| **HLD Document** | [Path] |
| **PRD Baseline** | [Path] v[Version] |
| **Review Time** | YYYY-MM-DD HH:MM |
| **Review Round** | Round N |
| **Risk Level** | [Low / Medium / High] |
| **Enabled Perspectives** | [Tech Lead / Senior / Security / DBA / SRE / Architect / QA ...] |
| **Review Decision** | 🟢 Pass / 🔴 Fail |

---

## Gate 1 Summary: PRD↔HLD Alignment

### Requirement Coverage Matrix
| PRD Item | Acceptance Criteria | HLD Section | Status | Notes |
|----------|---------------------|-------------|--------|-------|
| [REQ-*] | [Acceptance Criteria] | [HLD Section] | ✅ / ⚠️ / ❌ | [Notes] |

### Drift Findings
| # | Type | PRD Location | HLD Location | Description | Severity |
|---|------|--------------|--------------|-------------|----------|
| 1 | Missing / Distorted / Out of Scope / Defocused | [PRD Location] | [HLD Location] | [Description] | P0 / P1 |

### Gate 1 Decision
- **Decision**: Pass / Fail
- **Coverage**: [x/y = z%]
- **Blocking Reason**: [If any]

---

## Findings

### 🔴 Blocking Issues (P0)
| # | Perspective | Issue | Evidence | Recommended Fix |
|---|-------------|-------|----------|-----------------|
| 1 | [Tech Lead / Security / ...] | [Description] | [HLD:Section / PRD:Section] | [Recommendation] |

### 🟡 Major Issues (P1)
| # | Perspective | Issue | Evidence | Recommended Fix |
|---|-------------|-------|----------|-----------------|
| 1 | [Tech Lead / Security / ...] | [Description] | [HLD:Section / PRD:Section] | [Recommendation] |

### 🔵 Improvement Suggestions (P2)
| # | Perspective | Issue | Evidence | Recommended Fix |
|---|-------------|-------|----------|-----------------|
| 1 | [Tech Lead / Security / ...] | [Description] | [HLD:Section / PRD:Section] | [Recommendation] |

---

## Missing Info / Questions

- [Missing information or pending clarifications; write "None" if not applicable]

## Decision Gates

- [Decision gates that require user confirmation, baseline completion, or missing index documents; write "None" if not applicable]

## Optional Improvements

- [Non-blocking improvements; write "None" if not applicable]

---

## Release Decision

| Threshold | Requirement | Actual | Status |
|-----------|-------------|--------|--------|
| P0 | = 0 | [n] | ✅ / ❌ |
| P1 | = 0 | [n] | ✅ / ❌ |
| P2 | ≤ 2 | [n] | ✅ / ❌ |

**Decision**: 🟢 Pass / 🔴 Fail

---

## Next Steps

- [Fix recommendations / re-review requirements / approval to move into implementation]
```

## Approval Certificate Template

```markdown
# ✅ HLD Approval Certificate

## Basic Information
| Item | Content |
|------|---------|
| **HLD Document** | [Path] |
| **PRD Baseline** | [Path] v[Version] |
| **Approval Time** | YYYY-MM-DD HH:MM |
| **Review Round** | Total N rounds |
| **Review Decision** | 🟢 Pass |

---

## Alignment Confirmation
- Requirement coverage is 100%
- No missing requirements
- No unmarked requirement expansion
- No requirement distortion

## Release Threshold Confirmation
- P0 = 0
- P1 = 0
- P2 ≤ 2

## Review History
| Round | Date | Issue Counts | Decision |
|-------|------|--------------|----------|
| 1 | YYYY-MM-DD | P0: X, P1: Y, P2: Z | Fail |
| 2 | YYYY-MM-DD | P0: 0, P1: 0, P2: Z | Pass |

## Review Coverage
- No P0 issues in Gate 1
- Core technical review completed
- Role-specific incremental review completed (if applicable)

## Reviewer
- `hld-reviewer`

## Approval Confirmation

This HLD has passed the review and may proceed to implementation.

## Approval Stamp

`PASSED-{YYYYMMDD}-{first6_of_HLD_filename_hash}`
```
