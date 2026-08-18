# PRD Template: Third Party Integration

This template is suitable for the need to access external services, such as monitoring systems, payment gateways, AI engines, cloud services, etc.

---

## Document structure

```markdown
# PRD: [integration name]

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
title: [integration name]
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

### 2.1 Business Background

[Why you need to integrate this third-party service]

### 2.2 Integration goals

[What effect should be achieved after integration]

### 2.3 Success Indicators

| Indicators | Target values ​​| Data sources | Measurement methods |
|------|--------|----------|----------|
| [Indicators] | [Target value] | Already buried points/Need to add new ones/Manual statistics | [Measurement method] |

### 2.4 Current Business State (such as replacing/enhancing existing capabilities)

#### Current status
[Describe how the business requirement is currently met. If it is a new requirement, mark "not applicable"]

#### Business changes
| Change items | Before change | After change |
|--------|--------|--------|
| [Capability/Process] | [Current Status] | [Post-Integration Status] |

### 2.5 Relevant capability identification (mandatory)

| Existing capabilities | Capability scope | Matching degree with current needs | Capability gaps | Suggested directions | Source |
|----------|---------|--------------|---------|---------|------|
| [Capability name] | [Scope covered by this capability] | Full match/partial match/no match | [Gap description, fill in "none" if there is no gap] | Recommended to reuse/replaceable/complementary/need to create | [Document/code path] |

> **Description**:
> - This table is a mandatory output to ensure that all potentially relevant existing capabilities are identified
> - **"Source" column is required**: You must indicate which document or code the capability was identified from, and no baseless guessing is allowed.
> - "Recommended directions" are only PRD suggestions, and the final reuse decision falls within the scope of HLD
> - If it is confirmed that there is no relevant ability, fill in "After investigation, there is no relevant ability" and explain the **scope of investigation** (which paths/keywords were searched)

---

## 3. Scope

### Within the scope of 3.1

- [Function to be integrated 1]
- [Function to be integrated 2]

### 3.2 Out of range

- [Functions not within the scope of this integration]

### 3.3 Matters to be confirmed

- [ ] [Items to be confirmed]

---

## 4. Solution analysis

### 4.1 Requirements Overview

[Briefly describe core requirements for third-party services]

### 4.2 Comparison of candidate solutions

| Dimensions | [Plan A] | [Plan B] | [Plan C] |
|------|---------|---------|---------|
| Feature Coverage | [Rating/Description] | [Rating/Description] | [Rating/Description] |
| Price | [Price] | [Price] | [Price] |
| Document Quality | [Rating] | [Rating] | [Rating] |
| Community activity | [Rating] | [Rating] | [Rating] |
| Domestic Availability | [Rating] | [Rating] | [Rating] |
| Security Compliance | [Rating] | [Rating] | [Rating] |

### 4.3 Solution suggestions

**Suggested solution**: [Program name]

**Reason for suggestion**:
1. [Reason 1]
2. [Reason 2]

**risk**:
- [Risk of choosing this option]

> See HLD for final solution selection decision

---

## 5. Integration requirements

### 5.1 Required abilities

[List capabilities that need to be obtained from third-party services]

| Capabilities | Description | Priority |
|------|------|--------|
| [Ability 1] | [Description] | P0/P1/P2 |
| [Ability 2] | [Description] | P0/P1/P2 |

### 5.2 Function Mapping

[Describe the correspondence between our functions and third-party capabilities]

| Our functions | Third-party capabilities | Description |
|----------|------------|------|
| [Function] | [Ability] | [Description] |

### 5.3 Data interaction

[Describe data interaction requirements with third parties]

| Data | Direction | Description |
|------|------|------|
| [Data] | Our → Third Party / Third Party → Our | [Description] |

> For specific interface mapping and data conversion, see HLD

---

## 6. Exception handling requirements

### 6.1 Abnormal scenarios

| Scenario | Business Impact | User Perception |
|------|----------|----------|
| Third-party services are unavailable | [Impact] | [What users see] |
| Response Timeout | [Impact] | [What User Sees] |
| Data return exception | [Impact] | [What the user sees] |

### 6.2 Downgrade requirements

| Scenario | Downgrade Plan | User Tips |
|------|----------|----------|
| [Scenario] | [Plan] | [Prompt content] |

> For specific retry and circuit breaker strategies, see HLD

---

## 7. Non-functional requirements

### 7.1 Performance requirements

| Scenario | Requirements |
|------|------|
| Call delay (excluding third-party time-consuming) | P99 ≤ [X]ms |
| Throughput | [X] QPS |

### 7.2 Security requirements

| Requirements | Description |
|------|------|
| Transmission Encryption | [Required] |
| Credential Protection | [Requirements] |
| Sensitive Data | [Processing Request] |

### 7.3 Monitoring requirements

| Monitoring items | Description |
|--------|------|
| Call success rate | [Requirements] |
| response time | [requirements] |
| Error Alert | [Requirement] |

### 7.4 Compatibility requirements

| Requirements | Description |
|------|------|
| Interface Compatibility | [Whether existing callers are affected] |
| Data compatibility | [Whether the existing data format needs to be changed] |
| Third-party version compatibility | [Supported third-party API version range] |

### 7.5 Release requirements

| Requirements | Description |
|------|------|
| Grayscale strategy | [Whether grayscale is required, grayscale range] |
| Rollback capability | [Whether rollback needs to be supported and rollback conditions] |
| Function switch | [Whether function switch is required] |

> Note: For specific grayscale/rollback technical solutions, see HLD

---

## 8. Dependencies and constraints

### 8.1 Third-party service restrictions

| Constraints | Description |
|------|------|
| API version | [version number] |
| Current Limit Limit | [Limit Description] |
| SLA | [SLA description] |

### 8.2 Known constraints

- [Business Constraints]
- [Compliance Constraints]

---

## 9. Project Plan

### 9.1 Milestones

| Milestones | Target dates | Deliverables |
|--------|----------|--------|
| Interface research completed | YYYY-MM-DD | Interface documents, feasibility report |
| Integrated development completed | YYYY-MM-DD | Integrated code |
| Joint debugging test completed | YYYY-MM-DD | Joint debugging report |
| Go online | YYYY-MM-DD | Production environment deployment |

### 9.2 Resource Allocation

| Roles | People | Commitment |
|------|------|------|
| [role] | [personnel] | [ratio] |

---

## 10. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|------|------|----------|
| Third-party services are unstable | High | Medium | Implement downgrade plan |
| API Changes | Medium | Low | Follow Change Notifications |
| [Other risks] | [Impact] | [Probability] | [Measures] |

---

## 11. Acceptance Criteria

### AC-001: Basic functions
- [ ] [Functional Acceptance Conditions]

### AC-002: Exception handling
- [ ] Correctly handle errors returned by third parties
- [ ] Users are given clear prompts when timeout occurs
- [ ] Features available when downgrade plan is in effect

### AC-003: Monitoring
- [ ] Monitoring indicators are collected correctly
- [ ] Alarm rules are triggered correctly

---

## 12. Questions to be clarified

| Number | Question | Asked by | Status | Conclusion |
|------|------|--------|------|------|
| Q1 | [Question] | [Asker] | To be discussed/resolved | [Conclusion] |

---

## Appendix

### A. Third-party document link

- [Official Documentation]: [Link]
- [API Reference]: [Link]

### B. Test account information

| Environment | Account/Key | Purpose |
|------|----------|------|
| Sandbox | [Desensitization Information] | Development Testing |
```

---

## Writing Guidance

### Solution Analysis Chapter

When there are multiple candidates:
1. List the evaluation dimensions (function, price, documentation, community, compliance, etc.)
2. Score or describe each solution
3. Give program suggestions and reasons (note: the final selection decision rests with HLD)

If there is a clear preferred plan, the reasons for the recommendation still need to be stated.

### Integration requirements chapter

**Note**: PRD describes "what capabilities are required" and does not design "how to call them".

**Correct writing**:
```markdown
| Our functions | Third-party capabilities | Description |
|----------|------------|------|
| Send SMS verification code | Send SMS | Used for user registration and login |
| Query sending status | Status query | Used to confirm delivery |
```

**Wrong writing (crossing the boundary to HLD)**:
```markdown
| Our functions | Third-party interface | Calling method |
|----------|------------|----------|
| Send SMS | POST /sms/send | Synchronous call, timeout 3s |
```

### Exception handling requirements chapter

**Correct writing**:
```markdown
| Scenario | Downgrade Plan | User Tips |
|------|----------|----------|
| The payment service is unavailable | Display a maintenance prompt and guide you to try again later | "The payment service is temporarily busy, please try again later" |
| AI service timed out | Returning default results | "AI responded slowly and has returned default results for you" |
```

**Wrong writing (crossing the boundary to HLD)**:
```markdown
Retry strategy: Maximum retries 3 times, exponential backoff, initial interval 1s
Fuse configuration: Error rate > 50% triggers fuse, fuse duration is 30s
```

### Example of acceptance criteria

```markdown
### AC-001: SMS sending
- [ ] Enter the correct mobile phone number and the verification code is sent successfully
- [ ] Verification code is valid for 5 minutes
- [ ] The same mobile phone number can only be sent once in 1 minute.

### AC-002: Exception handling
- [ ] Display friendly prompts when SMS service is unavailable
- [ ] Users can try again when sending fails
- [ ] Error log is recorded correctly
```
