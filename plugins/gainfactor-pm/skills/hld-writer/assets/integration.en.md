# HLD Template: Third Party Integration

> The following is the template content, copy it and fill it in according to the actual situation.

---

# [Third Party Service] Integrated technical design

## Meta information

| Project | Content |
|------|------|
| Associated PRD | [PRD document link] |
| Third-party services | [Service name] |
| Version | v1.0 |
| Author | [Author] |

## PRD↔HLD requirements mapping table

**Coverage of this HLD**: [Scope] (required for 1:N scenario)
**Index document**: [HLD-INDEX-xxx.md] (path) (required for 1:N scenario)

| PRD Entry | Acceptance Criteria | HLD Chapter | Status |
|----------|---------|---------|------|
| [FR-XXX] | [Acceptance Criteria] | [Corresponding Chapter] | ✓/In Progress/To Be Determined |

## 1. Integration Overview

### 1.1 Business Background
[Why you need to integrate this service]

### 1.2 Integration scope
| Capabilities | Whether to integrate | Description |
|------|---------|------|
| [Competency 1] | Yes/No | [Description] |

### 1.3 Third-party service information
| Project | Content |
|------|------|
| Service Provider | [Service Provider] |
| API version | [version] |
| Document address | [Link] |
| SLA | [SLA] |

## 2. Technical architecture

### 2.1 Integrated architecture

```mermaid
graph LR
A[Business Service] --> B[Integrated Adaptation Layer]
B --> C [Third Party API]
B --> D[(local cache)]
B --> E[(callback processing)]
```

### 2.2 Reuse inventory

| Capability requirements | Candidate solutions | Assessment conclusions | Sources |
|---------|---------|---------|------|
| Third-party integration | Existing adapter / Open source SDK / Self-developed | [Choice and reason] | [Documentation/code path] |
| [Other Capabilities] | [Alternatives] | [Selection and Reasons] | [Documentation/Code Path] |

> Description:
> - Give priority to reusing existing adapters, open source SDKs, and internal packaging. Sufficient reasons must be given for self-development.
> - **"Source" column is required**: You must indicate which document or code the candidate solution was identified from, and unfounded guessing is prohibited.

### 2.3 Adaptation layer design
[Why adaptation layer and adaptation layer responsibilities are needed]

## 3. Interface mapping

### 3.1 Call third party

| Business scenario | Third-party interface | Method | Description |
|---------|-----------|------|------|
| [Scenario 1] | [Interface] | POST | [Description] |

### 3.2 Receive callback

| Callback type | Local interface | Processing logic |
|---------|---------|---------|
| [Type 1] | POST /callback/xxx | [Logical] |

## 4. Data mapping (cross-system contract)

> Note: This section defines cross-system data contracts and falls under the category of HLD. Internal data table field design belongs to LLD.

### 4.1 Request mapping
| Local Concepts | Third-Party Fields | Conversion Rules |
|---------|-----------|---------|
| user ID | user_id | direct mapping |
| Amount | amount_cents | Yuan transfer points |

### 4.2 Response mapping
| Third-party fields | Local concepts | Conversion rules |
|-----------|---------|---------|
| [Field] | [Concept] | [Rule] |

### 4.3 Status Mapping
| Third-party status | Local status |
|-----------|---------|
| [status] | [status] |

## 5. Authentication and Security

### 5.1 Authentication method
[API Key / OAuth / Signature, etc.]

### 5.2 Key Management
[Key storage, rotation strategy]

### 5.3 Data Security
[Sensitive data processing, transmission encryption]

## 6. Reliability design

### 6.1 Timeout and retry
| Scenario | Timeout policy | Retry policy |
|------|---------|---------|
| Synchronous call | [Strategy] | [Strategy] |
| Asynchronous callback | [Strategy] | [Strategy] |

### 6.2 Circuit breaker downgrade
[Circuit breaker conditions, downgrade plan]

### 6.3 Idempotent design
[Request deduplication, callback deduplication]

### 6.4 Reconciliation mechanism
[Regular reconciliation strategy]

## 7. Exception handling

### 7.1 Error code mapping
| Third-party errors | Local error codes | Processing strategies |
|-----------|-----------|---------|
| [Error] | [Error code] | [Strategy] |

### 7.2 Abnormal scenarios
| Scene | Processing |
|------|---------|
| Third-party timeout | [method] |
| Signature failed | [method] |
| Business failure | [method] |

## 8. Testing strategy

### 8.1 Sandbox environment
| Environment | Address | Purpose |
|------|------|------|
| Sandbox | [Address] | Development Test |
| Production | [Address] | Online |

### 8.2 Mock Strategy
[Local Mock, integration testing strategy]

## 9. Monitor alarms

### 9.1 Key Indicators
- Call success rate
- average latency
- Error distribution

### 9.2 Alarm rules
| Indicators | Thresholds | Alarm levels |
|------|------|---------|
| Success rate | < X% | P1 |

### 9.3 Buried points/monitoring design (accepting PRD success indicators)

| PRD success indicators | Hiding/monitoring design |
|-------------|--------------|
| [Indicator name] | [Collection method, storage, display] |

## 10. Online plan

### 10.1 Grayscale strategy
[Grayscale ratio, grayscale conditions]

### 10.2 Rollback plan
[Rollback steps, scope of impact]
