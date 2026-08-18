# Test Strategy Template

```markdown
# Test strategy: {project/function name}

<!-- TRACEABILITY-METADATA:BEGIN -->
```yaml
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-strategy-profile-v1
artifact:
  id: TSTRAT-[DOMAIN]-001
  type: TEST_STRATEGY
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
- **Guardrails**: {path} / N/A
- **Writing time**: {YYYY-MM-DD}
- **Status**: Draft/Reviewed/Approved

## Context Collection Report

### Baseline Confirmed
- {Baseline 1}
- {Baseline 2}

### Key constraints
- {constraint 1}
- {Constraint 2}

### Risks identified
- {Risk 1}
- {Risk 2}

## Test target

- {Target 1}
- {Target 2}

## scope

### In-scope
- {content}

### Out-of-scope
- {content}

### Must-not-regress
- {Capabilities/Processes}

## Quality Risk List

| Risk ID | Risk Description | Source Baseline | Impact | Probability | Priority |
|---------|----------|----------|------|------|--------|
| RISK-XXX-001 | {Description} | PRD/HLD/API | High/Medium/Low | High/Medium/Low | High/Medium/Low |

## Independent test layer allocation matrix

| Risk/Capability | System Integration | E2E / Journey | Regression | Compatibility | Non-functional | Owner |
|-----------|--------------------|---------------|------------|---------------|----------------|-------|
| {Capacity/Risk} | Main/Auxiliary/No | Main/Auxiliary/No | Main/Auxiliary/No | Main/Auxiliary/No | Main/Auxiliary/No | {Role} |

## API Contract Verification Strategy

- **Responsibility Boundary**: QA is responsible for approving the black box verification and regression of the API Contract; if development/SDET provides provider-side contract suite, it is only used as supplementary evidence
- **Validation Scope**: {Interface Group/Operation/Verification Point List}
- **Coverage dimensions**: {path/method/parameters/headers/request fields/response fields/status codes/error semantics/permissions/idempotent/compatible semantics}
- **Execution layer and evidence**: {System Integration / Regression / Evidence requirements}

## Staged execution rules

### Stage definition

| Phase | Phase goal | Current phase must be completed | Current phase should not be executed | Not ready item status |
|------|----------|------------------|------------------|--------------|
| {stage name} | {goal} | {content} | {content} | PASS / FAIL / BLOCKED / DEFERRED / N/A |

### Stage and environment mapping principles

- **Phase is a hard constraint**: You must first define which test phase the current node belongs to, and then decide which tests should be executed.
- **Environment is a soft boundary**: The environment is used to carry the capabilities and evidence sources required for this stage and cannot directly replace the stage definition.
- **Multiple environments are acceptable in the same stage**: as long as these environments can meet the verification capabilities, data conditions and observation requirements of the stage.
- **Subsequent stage access control**: Test items belonging to the subsequent stage. If the environment is not ready in the current stage, it should be marked as `Blocked / Deferred` instead of being directly recorded as a function failure.

## Environment, data, dependency strategy

### Environmental Strategy
- {Environmental Description}
- It must be written clearly: which testing phase the environment serves, what capabilities it provides, and whether it is only a recommended environment rather than the only environment

### Data Strategy
- {Data Preparation/Isolation/Cleaning}

### Dependency strategy
- {mock/stub/real dependency boundary}

### Observation and Verification
- {log/metrics/trace/DB/event}

## Develop built-in validation preconditions

- **Unit Test**: Responsible for development, status/requirements: {Description}
- **Code-level Integration Test**: Responsible for development, status/requirements: {Description}
- **Optional supplementary evidence**: If development/SDET provides provider-side contract suite/calling script, record status: {Description}
- **Note**: Approval of the black box verification of the API Contract belongs to the In-scope of this testing strategy and cannot be excluded as an upstream precondition

## Entry standards

- {Standard 1}
- {Standard 2}
- {Entrance prerequisite for the current stage}

## Export standards

- {Standard 1}
- {Standard 2}
- {Exit threshold at current stage}
- {Transfer conditions for retaining access control in subsequent stages}

## Automation and regression strategies

### Smoke
- {content}

### Critical Regression
- {content}

### Compatibility Regression
- {content}

## Assumptions, exemptions, items to be confirmed

| Type | Content | Impact | Owner | Deadline |
|------|------|------|-------|----------|
| Assumptions/Exemptions/To Be Confirmed | {Description} | {Impact} | {Person/Role} | {Date} |
```
