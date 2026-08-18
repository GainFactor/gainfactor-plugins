# PRD Template: Performance/Security Optimization

This template is suitable for non-functional improvement needs such as performance optimization and security hardening.

---

## Document structure

```markdown
# PRD: [Optimization name]

> **Document Version**: X.X
> **Status**: Draft / Under Review / Approved
> **Author**: [Author’s name]
> **Creation Date**: YYYY-MM-DD
> **Last Update**: YYYY-MM-DD

<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: prd-profile-v1
artifact:
  id: PRD-[DOMAIN]-001
  type: PRD
title: [Optimization name]
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

---

## 1. Document Information

### 1.1 Basic Information

| Properties | Values ​​|
|------|-----|
| PRD Number | PRD-XXX |
| Products | [Product Name] |
| Priority | P0 / P1 / P2 / P3 |
| Estimated version | vX.X |
| Optimization Type | Performance Optimization / Security Hardening / Reliability Improvement |
| PRD baseline version | vX.X (HLD is based on this version) |
| Last sync date | YYYY-MM-DD |

### 1.2 Revision History

| Version | Date | Changes | Author |
|------|------|----------|------|
| X.X | YYYY-MM-DD | [Change description] | [Author] |

### 1.3 Glossary

| Terminology | Definition |
|------|------|
| [Term] | [Definition] |

---

## 2. Background and goals

### 2.1 Optimize background

[Describe why optimization is needed and what are the triggers]

- Business growth leads to performance bottlenecks
- Issues discovered by security audits
- User feedback
- Monitor alarms
- other reasons

### 2.2 Optimization goals

| Indicator | Current value (baseline) | Target value | Data source | Improvement |
|------|----------------|--------|----------|----------|
| [Indicator 1] | [Current value] | [Target value] | Already monitored/need to add | [Percent] |
| [Indicator 2] | [Current value] | [Target value] | Already monitored/need to add | [Percent] |

### 2.3 Constraints

- Does not change existing functional behavior
- Does not change user experience
- [Other constraints]

### 2.4 Relevant capability identification (mandatory)

| Existing capabilities | Capability scope | Matching degree with current needs | Capability gaps | Suggested directions | Source |
|----------|---------|--------------|---------|---------|------|
| [Capability name] | [Scope covered by this capability] | Complete match/Partial match/No match | [Gap description, fill in "None" if there is no gap] | Recommended reuse/Recommended reference/Need to create new | [Document/code path] |

> **Description**:
> - This table is a mandatory output to identify existing capabilities that can assist optimization (such as existing caching solutions, monitoring tools, security components, etc.)
> - **"Source" column is required**: You must indicate which document or code the capability was identified from, and no baseless guessing is allowed.
> - "Recommended directions" are only PRD suggestions, and the final reuse decision falls within the scope of HLD
> - If it is confirmed that there is no relevant ability, fill in "After investigation, there is no relevant ability" and explain the **scope of investigation** (which paths/keywords were searched)

---

## 3. Scope

### Within the scope of 3.1

- [Modules/scenarios to be optimized]

### 3.2 Out of range

- [Contents not within the scope of this optimization]

### 3.3 Matters to be confirmed

- [ ] [Items to be confirmed]

---

## 4. Problem analysis

### 4.1 Problem phenomenon

[Describe the observed problem phenomenon]

| Problem number | Problem description | Frequency of occurrence | Impact |
|----------|----------|----------|------|
| P-001 | [Description] | [Frequency] | [Effect] |

### 4.2 Baseline data

**Performance Data** (if applicable):

| Indicators | P50 | P90 | P99 |
|------|-----|-----|-----|
| [Indicator] | [Value] | [Value] | [Value] |

**Security Data** (if applicable):

| Problem type | Severity | How discovered |
|----------|----------|----------|
| [Type] | High/Medium/Low | [Mode] |

### 4.3 Root cause of the problem

[Analyze the root cause of the problem and describe it from a business perspective]

| Problem | Root Cause Analysis |
|------|----------|
| [Problem] | [Root Cause] |

---

## 5. Optimization goals

### 5.1 Target indicators

| Metrics | Current Baseline | Target Value | Priority |
|------|----------|--------|--------|
| [Indicator] | [Baseline] | [Target] | P0/P1/P2 |

### 5.2 Goal constraints

- Functional behavior remains unchanged
- No regression in performance (other indicators)
- [Other constraints]

> For specific optimization plans, see HLD

---

## 6. Verification requirements

### 6.1 Testing requirements

**Performance Test** (if applicable):

| Test items | Test conditions | Acceptance Criteria |
|--------|----------|----------|
| [Test Items] | [Conditions] | [Standards] |

**Security Test** (if applicable):

| Test Type | Coverage | Acceptance Criteria |
|----------|----------|----------|
| [Type] | [Range] | [Standard] |

### 6.2 Regression testing

- [ ] Functional regression testing
- [ ] Other performance indicators will not be rolled back

### 6.3 Benchmark comparison

| Metrics | Baseline before optimization | Target after optimization | Actual results |
|------|------------|------------|----------|
| [Indicator] | [Baseline value] | [Target value] | [To be filled in] |

---

## 7. Monitoring requirements

### 7.1 Monitoring indicators

| Indicator | Description | Alarm threshold |
|------|------|----------|
| [Indicator] | [Description] | [Threshold] |

### 7.2 Grayscale verification

| Stage | Traffic proportion | Duration | Observation indicators | Rollback conditions |
|------|----------|----------|----------|----------|
| Phase 1 | [Proportion] | [Time] | [Indicator] | [Condition] |

### 7.3 Long-term observation

| Observation period | Observation indicators | Expected trends |
|----------|----------|----------|
| 1 day | [Indicator] | [Trend] |
| 1 week | [Indicators] | [Trends] |

---

## 8. Non-functional requirements

### 8.1 Compatibility requirements

- Does not change existing functional behavior
- No changes to the external interface
- Does not affect existing users

### 8.2 Release requirements

| Requirements | Description |
|------|------|
| Grayscale strategy | [Whether grayscale is required, grayscale range] |
| Rollback capability | [Whether rollback needs to be supported and rollback conditions] |
| Function switch | [Whether function switch is required] |

> Note: For specific grayscale/rollback technical solutions, see HLD

### 8.3 Observability requirements

- [Monitoring coverage requirements]
- [Log requirements]

---

## 9. Dependencies and constraints

### 9.1 Known constraints

- [Business Constraints]
- [Time constraint]
- [Resource Constraints]

### 9.2 Risk Constraints

- [Unacceptable risk]

---

## 10. Project Plan

### 10.1 Milestones

| Milestones | Target dates | Deliverables |
|--------|----------|--------|
| Problem analysis completed | YYYY-MM-DD | Analysis report |
| Plan review passed | YYYY-MM-DD | PRD, HLD |
| Development completed | YYYY-MM-DD | Code |
| Test completed | YYYY-MM-DD | Test report |
| Grayscale release | YYYY-MM-DD | - |
| Full release | YYYY-MM-DD | - |
| Effect verification | YYYY-MM-DD | Verification report |

### 10.2 Resource Allocation

| Roles | People | Commitment |
|------|------|------|
| [role] | [personnel] | [ratio] |

---

## 11. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|------|------|----------|
| Optimization effect not up to expectations | Medium | Medium | Phased verification |
| Introduce new issues | High | Low | Fully tested, grayscale release |
| Performance rollback | High | Low | Benchmark comparison, fast rollback |

---

## 12. Acceptance Criteria

### AC-001: Performance Goals Achieved
- [ ] [Indicator 1] reached target value [X]
- [ ] [Indicator 2] Target value reached [Y]

### AC-002: Functionality not affected
- [ ] All functions work properly
- [ ] All automated tests passed

### AC-003: Safety Goal Achieved (if applicable)
- [ ] [Security Issue 1] Fixed
- [ ] No high-risk vulnerabilities found in security scans

### AC-004: Improved monitoring
- [ ] Normal collection of monitoring indicators
- [ ] Alarm rules are configured correctly

---

## 13. Questions to be clarified

| Number | Question | Asked by | Status | Conclusion |
|------|------|--------|------|------|
| Q1 | [Question] | [Asker] | To be discussed/resolved | [Conclusion] |

---

## Appendix

### A. Performance analysis report

[link or inline]

### B. Security Scan Report

[link or inline]
```

---

## Writing Guidance

### Core points of optimizing PRD

1. **Data-driven**: Use data to explain problems and goals
2. **Baseline comparison**: Clear comparison before and after optimization
3. **Clear goals**: clear quantitative goals
4. **Verification Complete**: Detailed verification requirements
5. **Grayscale verification**: Verify the optimization effect in stages

### Problem Analysis Chapter

**Correct writing**:
```markdown
| Problem number | Problem description | Frequency of occurrence | Impact |
|----------|----------|----------|------|
| P-001 | The list page loads slowly | 100% during peak periods | Users wait for a long time and the conversion rate drops |
| P-002 | Search timeout | About 5% of requests per day | Poor user experience |
```

**Wrong way of writing (too technical)**:
```markdown
| Issue number | Issue description |
|----------|----------|
| P-001 | MySQL query does not use index, you need to add created_at index |
```

### Optimization target chapter

**Correct writing**:
```markdown
| Metrics | Current Baseline | Target Value | Priority |
|------|----------|--------|--------|
| List page loading time P99 | 3s | ≤ 1s | P0 |
| Search success rate | 95% | ≥ 99.5% | P0 |
```

**Wrong writing (including technical solutions)**:
```markdown
| Optimization items | Plans |
|--------|------|
| Add cache | Use Redis to cache hotspot data, TTL 5 minutes |
| Add index | Add (user_id, created_at) composite index to the orders table |
```

### Grayscale verification form example

```markdown
| Stage | Traffic proportion | Duration | Observation indicators | Rollback conditions |
|------|----------|----------|----------|----------|
| Phase 1 | 1% | 1 hour | Error rate, latency | Error rate > 1% |
| Phase 2 | 10% | 4 hours | Error rate, latency | Error rate > 0.5% |
| Phase 3 | 50% | 1 day | Error rate, latency, throughput | Error rate > 0.1% |
| Full amount | 100% | - | All indicators | - |
```

### Example of acceptance criteria

```markdown
### AC-001: Performance Goals Achieved
- [ ] List page P99 delay ≤ 1s
- [ ] Search success rate ≥ 99.5%
- [ ] Home page loading time ≤ 2s

### AC-002: Functionality not affected
- [ ] All functions work properly
- [ ] All automated tests passed
- [ ] User unaware

### AC-003: Improved monitoring
- [ ] New indicators are collected normally.
- [ ] Alarm rules are configured correctly
- [ ] You can see the optimization effect on the market
```
