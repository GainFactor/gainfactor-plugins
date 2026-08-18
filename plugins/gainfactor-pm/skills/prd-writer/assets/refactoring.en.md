# PRD Template: functional refactoring

This template is suitable for architectural adjustment, technical debt cleanup, module splitting and other needs that do not change external functions but change internal implementation.

---

## Document structure

```markdown
# PRD: [refactoring name]

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
title: [refactoring name]
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

### 2.1 Reconstruction background

[Describe why refactoring is needed]

### 2.2 Refactoring goals

[Describe the desired state after refactoring]

1. **Goal 1**: [Specific description]
2. **Goal 2**: [Specific description]

### 2.3 Success Indicators

| Indicator | Current value | Target value | Data source | Measurement method |
|------|--------|--------|----------|----------|
| [Indicator] | [Current] | [Target] | Already monitored/need to add | [Measurement method] |

### 2.4 What not to do

Clearly state that this refactoring does not include functional changes:

- Does not change the behavior of [Feature A]
- Does not change user experience
- Do not change the external interface contract

### 2.5 Relevant capability identification (mandatory)

| Existing capabilities | Capability scope | Matching degree with current needs | Capability gaps | Suggested directions | Source |
|----------|---------|--------------|---------|---------|------|
| [Capability name] | [Scope covered by this capability] | Complete match/Partial match/No match | [Gap description, fill in "None" if there is no gap] | Recommended reuse/Recommended reference/Need to create new | [Document/code path] |

> **Description**:
> - This table is a mandatory output, identifying existing capabilities that can assist refactoring (such as existing design patterns, tool libraries, test frameworks, etc.)
> - **"Source" column is required**: You must indicate which document or code the capability was identified from, and no baseless guessing is allowed.
> - "Recommended directions" are only PRD suggestions, and the final reuse decision falls within the scope of HLD
> - If it is confirmed that there is no relevant ability, fill in "After investigation, there is no relevant ability" and explain the **scope of investigation** (which paths/keywords were searched)

---

## 3. Scope

### Within the scope of 3.1

- [Module/Component to be refactored]

### 3.2 Out of range

- [Modules that are not within the scope of this reconstruction]

### 3.3 Matters to be confirmed

- [ ] [Items to be confirmed]

---

## 4. Current situation analysis

### 4.1 Problems

| Issue Number | Issue Description | Impact | Severity |
|----------|----------|------|----------|
| P-001 | [Problem Description] | [Impact Description] | High/Medium/Low |
| P-002 | [Problem Description] | [Impact Description] | High/Medium/Low |

### 4.2 Root cause of the problem

[Analyze the root cause of the problem]

### 4.3 Current situation assessment

| Dimensions | Current Status | Issues |
|------|----------|------|
| [Dimension] | [Status Description] | [Problem Description] |

---

## 5. Reconstruct target state

### 5.1 Desired state

[Describe the expected state after reconstruction, not involving specific technical solutions]

| Dimensions | Current status | Target status |
|------|----------|----------|
| [dimension] | [current] | [target] |

### 5.2 Problem Solving Mapping

| Problem number | Problem description | How to resolve |
|----------|----------|----------|
| P-001 | [Problem description] | [Solution direction, non-technical solution] |
| P-002 | [Problem description] | [Solution direction, non-technical solution] |

> For specific technical solutions, see HLD

---

## 6. Compatibility requirements

### 6.1 Functional compatibility

| Requirements | Description |
|------|------|
| Functional Behavior | All existing functional behaviors remain unchanged |
| User experience | User insensible |
| External interface | The interface contract remains unchanged |

### 6.2 Data Compatibility

| Requirements | Description |
|------|------|
| Existing Data | [Compatibility Requirements] |
| Data migration | [Whether migration is required] |

### 6.3 Release requirements

| Requirements | Description |
|------|------|
| Grayscale strategy | [Whether grayscale is required, grayscale range] |
| Rollback capability | [Whether rollback needs to be supported and rollback conditions] |
| Function switch | [Whether function switch is required] |
| Transition period | [Requirements for parallel operation of old and new, if necessary] |

> Note: For specific grayscale/rollback technical solutions, see HLD

---

## 7. Verification requirements

### 7.1 Function Verification

- [ ] All existing features work properly
- [ ] All automated tests passed
- [ ] Key business process verification passed

### 7.2 Performance Verification

| Indicators | Baseline values ​​| Allowed fluctuations |
|------|--------|----------|
| [Indicator] | [Baseline Value] | ±[X]% |

### 7.3 Regression verification

- [ ] [Regression Test Scope]

---

## 8. Non-functional requirements

### 8.1 Performance requirements

- Performance after reconstruction is not lower than before reconstruction

### 8.2 Observability requirements

- [Monitoring requirements]
- [Log requirements]

---

## 9. Dependencies and constraints

### 9.1 Known constraints

- [Business Constraints]
- [Time constraint]

### 9.2 Risk Constraints

- [Unacceptable risk]

---

## 10. Project Plan

### 10.1 Milestones

| Milestones | Target dates | Deliverables |
|--------|----------|--------|
| Plan review passed | YYYY-MM-DD | PRD, HLD |
| Development completed | YYYY-MM-DD | Code |
| Test completed | YYYY-MM-DD | Test report |
| Grayscale release | YYYY-MM-DD | Grayscale environment |
| Full release | YYYY-MM-DD | Production environment |
| Old code offline | YYYY-MM-DD | Cleanup completed |

### 10.2 Resource Allocation

| Roles | People | Commitment |
|------|------|------|
| [role] | [personnel] | [ratio] |

---

## 11. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|------|------|----------|
| Incomplete scope of impact assessment | High | Medium | Sufficient testing and grayscale |
| Performance rollback | High | Low | Performance test comparison |
| Data Inconsistency | High | Low | Data Verification |
| [Other risks] | [Impact] | [Probability] | [Measures] |

---

## 12. Acceptance Criteria

### AC-001: Function unchanged
- [ ] All existing features work properly
- [ ] All interface contracts remain unchanged
- [ ] All automated tests passed

### AC-002: No performance regression
- [ ] [Indicator 1] Not lower than the baseline before reconstruction
- [ ] [Indicator 2] Not lower than the baseline before reconstruction

### AC-003: Problem Solving
- [ ] [Issue P-001] Resolved
- [ ] [Issue P-002] Resolved

### AC-004: Release completed
- [ ] Grayscale release without exception
- [ ] Full release without exception

---

## 13. Questions to be clarified

| Number | Question | Asked by | Status | Conclusion |
|------|------|--------|------|------|
| Q1 | [Question] | [Asker] | To be discussed/resolved | [Conclusion] |

---

## Appendix

[If any additional content]
```

---

## Writing Guidance

### Reconstructing the core points of PRD

1. **Clear "what not to do"**: Refactoring should not change external behavior and should be clearly stated
2. **Problem-driven**: Explain clearly the problems of the current situation and what should be solved by refactoring
3. **Goal state**: Describes the desired state rather than specific technical solutions
4. **Compatibility**: Clarify compatibility requirements
5. **Verification Requirements**: How to verify successful refactoring

### Current Situation Analysis Chapter

**Correct writing**:
```markdown
| Issue Number | Issue Description | Impact | Severity |
|----------|----------|------|----------|
| P-001 | Module responsibilities are not clear, modifying one place affects many places | Development efficiency is low, bug rate is high | High |
| P-002 | Severe code duplication | High maintenance costs | Medium |
```

**Wrong way of writing (too technical)**:
```markdown
| Issue number | Issue description |
|----------|----------|
| P-001 | UserService has 2000 lines of code and needs to be split into UserQueryService and UserCommandService |
```

### Reconstruct the target state chapter

**Correct writing**:
```markdown
| Dimensions | Current status | Target status |
|------|----------|----------|
| Module responsibilities | Confused responsibilities | Single responsibilities and clear boundaries |
| Code duplication | Repeated logic in many places | Logic reuse, no duplication |
| Testability | Difficult to unit test | Independently testable |
```

**Wrong writing (crossing the boundary to HLD)**:
```markdown
| Changes | Current | Target |
|--------|------|------|
| UserService.ts | Single file 2000 lines | Split into 3 files |
| Database queries | Direct SQL | Using Repository mode |
```

### Example of acceptance criteria

```markdown
### AC-001: Function unchanged
- [ ] The user login process is normal
- [ ] The order creation process is normal
- [ ] All API return formats remain unchanged
- [ ] All automated tests passed

### AC-002: No performance regression
- [ ] Login interface P99 delay is no higher than before reconstruction
- [ ] Order query QPS is not lower than before reconstruction

### AC-003: Problem Solving
- [ ] Modifying the user module no longer affects the order module
- [ ] Improve the development efficiency of new functions (subjective evaluation)
```
