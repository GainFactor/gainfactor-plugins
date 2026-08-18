# Project Guardrails Template

> Use this template to produce a project-level Guardrails baseline or an incremental update. It should answer three questions: what the default path is, what is explicitly forbidden, and which changes should trigger downstream re-review.

---

# Project Guardrails

## 0. Metadata

| Item | Content |
|------|---------|
| Version | vX.Y |
| Status | draft / in_review / approved |
| Owner | [Owner / Team] |
| Effective Date | YYYY-MM-DD |
| Review Cadence | Quarterly / Every major release / As needed |
| Action Type | create_baseline / update_impacted_domains / restructure |
| Generation Mode | interview_first / repository_scan_first |
| Trigger Reason | [Project kickoff / architecture change / compliance requirement / incident review / repeated review findings] |
| Output Mode | Single document / index + domain docs |
| Applicable Scope | [System / team / repository / runtime environment] |

---

## 1. Positioning and Boundaries

- **In Scope**:
- **Out of Scope**:
- **Items that should not be used as feature-level design input**:
- **Domains updated in this round only**:

---

## 2. Update Triggers and Workflow Hooks

### 2.1 When Guardrails Must Be Created or Updated

| Trigger Type | Typical Signal | Action |
|--------------|----------------|--------|
| create_baseline | The repository does not yet have Guardrails | Establish a minimum viable baseline |
| update_impacted_domains | Default boundaries changed in architecture / platform / auth / data / release, etc. | Update impacted domains only |
| restructure | The single document is too large or domain-specific updates are frequent | Restructure into index + domain docs |
| no_change | Only feature-local changes | Fall back to HLD / LLD / ADR |

### 2.2 Downstream Re-review Hooks

| Change Domain | Impacted Artifacts / Skills | Recommended Action | Blocking Level |
|---------------|-----------------------------|--------------------|----------------|
| API / Contract | API Contract, HLD, LLD | Align default boundaries before continuing design | [block_before_design / review_before_merge / sync_next_cycle] |
| Data and Migration | HLD, LLD, Runbook | Re-review data model, migration, and rollback | [...] |
| Security and Compliance | API Contract, HLD, LLD, Runbook | Re-review auth, audit, and access control | [...] |
| Release / Rollback / Observability | HLD, Runbook | Re-review deployment, rollback, SLO, and alerting | [...] |
| Other Domains | [Path / Skill] | [Action] | [...] |

---

## 3. Fact Standards and Evidence Layers

### 3.1 Observed Facts

- [Code / configuration / CI / IaC / Runbook / tests / incident records]

### 3.2 Declarative Standards

- [ADR / existing standards / README / security policy / existing Guardrails]

### 3.3 Conflicts and Drift

| Conflict Item | Fact | Standard / Intent | Resolution |
|---------------|------|-------------------|------------|
| [Example] |  |  | [Codify current state / Keep target state / Pending decision] |

---

## 4. Rule Levels and Exception Mechanism

- **Must**: Mandatory. Violations are blocking.
- **Should**: Strongly recommended. Deviations require an explicit rationale.
- **Nice**: Recommended. Not blocking.

**Exception Process**: Requester / Approver / Validity period / Record location / Expiration review method

---

## 5. Default Choices and Prohibited Items

- **Default technical path**:
- **Allowed range**:
- **Explicitly prohibited items**:
- **Required upstream standards / ADRs / external policies**:

---

## 6. LLD Module Requirements (Mandatory)

| Module | Requirement (Required / Optional / Forbidden) | Rationale | Source |
|--------|-----------------------------------------------|-----------|--------|
| Core | Required |  |  |
| API Contract | Required |  |  |
| Storage & Migration |  |  |  |
| Async / Event |  |  |  |
| Infra / IaC |  |  |  |
| Observability |  |  |  |
| Security / Compliance | Required |  |  |
| Deployment / Release |  |  |  |
| Frontend UX |  |  |  |
| External Integration |  |  |  |
| SDK / Library |  |  |  |

---

## 7. Guardrails Rule Table Template

| Rule ID | Level | Rule | Rationale | Applies To | Verification | Owner | Source |
|---------|-------|------|-----------|------------|--------------|-------|--------|
| GR-001 | Must |  |  |  |  |  |  |

---

## 8. Rules for High-Risk Domains

### 8.1 API / Contract Guardrails

[Use the rule table template]

### 8.2 Data and Migration Guardrails

[Use the rule table template]

### 8.3 Security and Compliance Guardrails

[Use the rule table template]

### 8.4 Release / Rollback / Observability Guardrails

[Use the rule table template]

---

## 9. Rules for Other Domains (As Needed)

### 9.1 Frontend UX / Engineering

[Fill in only if applicable]

### 9.2 Infrastructure / IaC

[Fill in only if applicable]

### 9.3 External Integrations / SDK / Event Messaging

[Fill in only if applicable]

---

## 10. Summary of Impact for This Change

- **Reason for this update**:
- **If this is the initial baseline, which mode was used**:
- **Impacted domains**:
- **Downstream documents / skills that require re-review**:
- **Blocking recommendation**:
- **Items not covered but requiring follow-up**:

---

## 11. Change Log

| Version | Change | Reason | Date | Author |
|---------|--------|--------|------|--------|
| vX.Y |  |  |  |  |
