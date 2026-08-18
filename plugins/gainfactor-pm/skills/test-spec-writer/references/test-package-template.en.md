# Test Spec / Test Case Package Template

```markdown
# Test specification: {project/function name}

<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-spec-profile-v1
artifact:
  id: TSPEC-[DOMAIN]-001
  type: TEST_SPEC
title: {project/function name}
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

## Basic Information

- **PRD Baseline**: {path} v{version}
- **API Contract Baseline**: {path} v{version}
- **HLD Baseline**: {path} v{version}
- **LLD Baseline**: {path} v{version}
- **Test Strategy**: {path} v{version}
- **Guardrails**: {path} / N/A
- **Status**: Draft/Reviewed/Approved

## scope

### In-scope
- {content}

### Out-of-scope
- {content}

### API Contract verification scope
- **Responsibility Boundary**: QA is responsible for approving the black box verification and regression of the API Contract; if development/SDET provides provider-side contract suite, it is only used as supplementary evidence
- **Verification Point List**: {interface group/operation/verification point}
- **Coverage dimensions**: {path/method/parameters/headers/request fields/response fields/status codes/error semantics/permissions/idempotent/compatible semantics}

### Develop built-in validation preconditions
- **Unit Test**: {Requirement/Status}
- **Code-level Integration Test**: {Requirement/Status}
- **Optional Supplementary Evidence**: provider-side contract suite / calling script: {requirements/status}
- **Note**: Approval of the black box verification of the API Contract belongs to the In-scope of this test package and cannot be excluded only as an upstream precondition

## Traceability matrix

| Source Type | Source ID/Location | Test Item | Status | Notes |
|----------|----------------|--------|------|------|
| PRD / API / HLD / LLD / Risk | {ID or Location} | {Case ID} | Covered / Partially Covered / Not Covered | {Description} |

## Coverage Summary

| Metrics | Numerator definition | Denominator definition | Coverage | Uncovered items |
|------|----------|----------|--------|----------|
| Requirement Coverage | Number of in-scope requirements that have been traced by at least 1 test item | Total number of in-scope requirements | {x/y = z%} | {ID List / None} |
| API Contract coverage | Number of in-scope API Contract verification points that have been covered by at least 1 test item | Total number of in-scope API Contract verification points | {x/y = z%} | {Verification point list / none} |
| risk coverage | number of in-scope risks that have been covered by at least 1 test item | total number of in-scope risks | {x/y = z%} | {ID list / none} |
| High risk coverage | Number of high risk items covered | Total number of high risk items | {x/y = z%} | {ID list / none} |
| Must-not-regress coverage | Number of must-not-regress items that have been covered by the regression package | Total number of must-not-regress items | {x/y = z%} | {ID list / none} |
| External behavior coverage | Number of in-scope external observable behaviors that have been covered by the test item | Total number of in-scope external observable behaviors | {x/y = z%} | {ID list / none} |
| Scene coverage rate | Number of covered scenes | Total number of identified scenes | {x/y = z%} | {Scene list / None} |
| Must-test NFR coverage | Number of must-test NFR items for the designed verification scheme | Total number of must-test NFR items | {x/y = z%} | {NFR list / none} |

### Description of statistical caliber

- The above is **test design coverage**, not code coverage, nor execution coverage
- The denominator contains only in-scope terms
- The following do not enter the denominator:
  - Out-of-scope
- Exemptions approved
  - unit / code-level integration
- Items that are clearly the responsibility of other independent test packages and have been referenced
- It is not allowed to give only one comprehensive total coverage, it must be displayed item by item

## Test matrix

| Scenario group | Test level | Priority | Required test | Automation candidate | Remarks |
|--------|----------|--------|------|------------|------|
| API Contract / Main Process / Branch / Exception / Boundary / System Integration / Compatible / Non-Functional | API / SYS / E2E / REG / COMPAT / NFT | P0 / P1 / P2 | Yes/No | High/Medium/Low | {Description} |

## Detailed test cases

### {Case ID} - {Use case name}

- **Source Traceability**: {PRD/API/HLD/LLD/Risk}
- **Priority**: P0/P1/P2
- **Precondition**: {content}
- **Data Preparation**: {Content}
- **Execution Steps**:
1. {Step}
2. {Step}
- **Input**: {content}
- **Expected result**: {content}
- **Judgment method/assertion point**: {content}
- **Clean Action**: {content}
- **Automated Suggestions**: {Suggestions}
- **Required Evidence**: {Log/Response/Events/DB/Screenshots/Metrics}

## Environment, data, dependencies

### environment
- {Environmental Description}

### data
- {Prepare / Quarantine / Cleanup}

### Dependencies
- {mock / stub / sandbox / real dependency}

### Observations and Evidence
- {logs/metrics/trace/db/events}

## Regression and implementation suggestions

### Smoke
- {Case ID}

### API Contract Regression
- {Case ID}

### Critical Regression
- {Case ID}

### Compatibility Regression
- {Case ID}

### Non-functional verification
- {scope and method}

## Assumptions, exemptions, items to be confirmed

| Type | Content | Impact | Owner | Deadline |
|------|------|------|-------|----------|
| Assumptions / Waivers / To Be Confirmed | {Content} | {Impact} | {Role} | {Date} |
```
