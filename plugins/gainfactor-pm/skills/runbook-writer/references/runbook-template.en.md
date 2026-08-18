# Runbook Output Template

This template defines the standard structure for all Runbooks produced by runbook-writer skill.

---

# [System Name] Runbook

**Version**: [version number]
**Last updated**: [Date]
**Maintenance Team**: [Team Name]

---

## 1. System Overview

### 1.1 System architecture

**System Description**:
[Brief description of system architecture extracted from HLD]

**Service Boundary**:
- Core Services: [List]
- Dependent services (internal): [list]
- Dependent services (external): [list]

**Data Storage**:
- Database: [type, purpose]
- Cache: [type, purpose]
- Object storage: [type, purpose]

### 1.2 System dependency graph

```
[Optional: System dependency diagram]
```

### 1.3 Key configuration

| Configuration items | Location | Description |
|--------|------|------|
| [Configuration Name] | [ConfigMap/Secret/File] | [Purpose] |

---

## 2. Deployment process

### 2.1 Pre-check

**Before starting the deployment, you must confirm:**

- [ ] Dependent service health status
  ```bash
# Check command
  curl http://[dependency-service]/health
# Expected output: {"status":"ok"}
  ```

- [ ] Database connection is normal
  ```bash
# Check command
  [database-check-command]
# Expected output: [expected-output]
  ```

- [ ] Maintenance window confirmation (if required)
- Start time: [time]
- End time: [time]
- Notification channel: [Notified]

- [ ] Backup confirmation
  ```bash
# Database backup
  [backup-command]
# Verify backup
  [verify-backup-command]
  ```

### 2.2 Deployment steps

**Step 1: [Step Name]**

```bash
#Execute command
[command]
```

**Expected Output**:
```
[expected output]
```

**verify**:
```bash
# Verify command
[verification-command]
# expected results
[expected-result]
```

**If it fails**: [troubleshooting steps]

---

**Step 2: [Next Step]**

[Repeat above format]

---

### 2.3 Deployment verification

**After completing all deployment steps, perform the following verifications:**

- [ ] **Health check passed**
  ```bash
  curl http://[service]/health
# Expected: {"status":"ok", "version":"[new-version]"}
  ```

- [ ] **Core Function Verification**
  ```bash
# Function verification command
  [functional-test-command]
# expected results
  [expected-result]
  ```

- [ ] **Monitoring indicators are normal**
  - QPS: [expected-range]
- P99 delay: < [threshold]
- Error rate: < [threshold]

  ```bash
# Query monitoring indicators
  [monitoring-query]
  ```

- [ ] **No exception in the log**
  ```bash
# View recent logs
  kubectl logs -f deployment/[name] --tail=100
# Check if there is ERROR/FATAL
  ```

**Verification pass standard**:
- ✅ All inspection items passed
- ✅ Monitoring indicators are within the normal range
- ✅ No serious log errors

**If validation fails** → Perform rollback process (see Section 3)

---

## 3. Rollback process

### 3.1 Rollback trigger conditions

**Immediate rollback conditions**:
- Error rate > [threshold]% (for [duration] minutes)
- P99 delay > [threshold]ms (for [duration] minutes)
- Core functionality is unavailable
- Serious security vulnerabilities discovered

**Decision Process**:
```
Abnormal indicators detected
  ↓
Lasts longer than threshold time?
  ↓ Yes
Rollback now
```

### 3.2 Rollback steps

**⚠️ The rollback step must be executable in case the new version completely fails**

---

**Step 1: Stop new version traffic**

```bash
# Switch traffic to the old version
[traffic-switch-command]
```

**verify**:
```bash
# Confirm that the traffic has been switched
[verify-command]
# Expectation: 100% traffic to the old version
```

---

**Step 2: Roll back app version**

```bash
# Roll back to the previous version
[rollback-command]
```

**Expected Output**:
```
[expected-output]
```

**verify**:
```bash
# Confirm that the version has been rolled back
[verify-version-command]
# Expected: [old-version]
```

---

**Step 3: Rollback database migration (if any)**

```bash
# Execute migration down
[migration-rollback-command]
```

**verify**:
```bash
# Check database schema version
[check-schema-version]
# Expected: [old-schema-version]
```

---

**Step 4: Rollback configuration (if any)**

```bash
# Restore old configuration
[config-rollback-command]
```

**verify**:
```bash
# Confirm that the configuration has been restored
[verify-config-command]
```

---

### 3.3 Rollback verification

**After the rollback is complete, you must verify:**

- [ ] **Service Health**
  ```bash
  curl http://[service]/health
# Expected: {"status":"ok", "version":"[old-version]"}
  ```

- [ ] **Core functions are normal**
  ```bash
  [functional-test-command]
  ```

- [ ] **Monitoring indicator recovery**
- Error rate < [normal-threshold]%
- P99 delay < [normal-threshold]ms

- [ ] **User Impact Assessment**
- Number of users affected: [Evaluation]
- Data consistency: [check]

**Rollback success criteria**:
- ✅ All verification passed
- ✅ Indicators returned to pre-deployment levels
- ✅ No new errors or warnings

---

## 4. Monitoring and Alarming

### 4.1 Key Indicators

| Metrics | SLO Thresholds | Query Commands/Query |
|------|----------|----------------|
| QPS | [min-max] | `[monitoring-query]` |
| P99 delay | < [threshold]ms | `[monitoring-query]` |
| Error rate | < [threshold]% | `[monitoring-query]` |
| CPU usage | < [threshold]% | `[monitoring-query]` |
| Memory usage | < [threshold]% | `[monitoring-query]` |

### 4.2 SLO definition

**Availability SLO**:
- Target: [percentage]% uptime
- Measurement period: [period]
- Error budget: [error-budget]

**Performance SLO**:
- P99 delay: < [threshold]ms
- P95 delay: < [threshold]ms
- Error rate: < [threshold]%

### 4.3 Alarm configuration

**Critical Alert**:

1. **[Alarm name]**
- Trigger condition: [condition]
- Duration: [duration]
- Notification channel: [channel]
- Response SLA: [time]

**Warning warning**:

1. **[Alarm name]**
- Trigger condition: [condition]
- Duration: [duration]
- Notification channel: [channel]

### 4.4 Dashboard

**Main Monitoring Dashboard**:
- URL: [dashboard-url]
- Contains panels:
- QPS & Latency
- Error rate trends
- Resource usage
- Depend on service status

---

## 5. Troubleshooting

### 5.1 [Fault Scenario 1: Scenario Name]

**symptom**:
- [Observable Phenomenon 1]
- [Observable Phenomenon 2]
- Abnormal related indicators: [metric] > [threshold]

**Troubleshooting steps**:

1. **Confirm the scope of symptoms**
   ```bash
# Check the affected range
   [check-command]
   ```

2. **Check log**
   ```bash
# View error log
   kubectl logs deployment/[name] | grep ERROR
   ```

3. **Check dependent services**
   ```bash
# Check upstream service status
   [check-dependency-command]
   ```

**Root cause analysis**:
- Possible cause 1: [description]
- Verification method: [how-to-verify]
- Possible cause 2: [description]
- Verification method: [how-to-verify]

**Solution**:

**Option 1: [Description]**
```bash
#Execute command
[fix-command]
```

**Verification Fix**:
```bash
# Verify command
[verify-command]
# Expected results: [expected]
```

**If not resolved** → Try option 2 or upgrade

**Upgrade Conditions**:
- No solution after trying all solutions
- more than [time] minutes
- Expanded scope of influence

**Upgrade object**: [Team/Personnel]

---

### 5.2 [Fault Scenario 2: Scenario Name]

[Repeat above format]

---

### 5.N General troubleshooting process

```
Alarms/abnormalities found
  ↓
Identify symptoms and extent of effects
  ↓
Check monitoring indicators + logs
  ↓
Identify root causes (match known scenarios)
  ↓
Implement corresponding solutions
  ↓
Verify the fix takes effect
  ↓
Record accident report
```

---

## 6. Duty Manual

### 6.1 Responsibilities on duty

**on-call engineers are responsible for**:
- Respond to Critical alerts (SLA: [time])
- Respond to Warning alarms (SLA: [time])
- Perform planned maintenance operations
- Document incidents and solutions
- Update runbook

**Not responsible**:
- Non-emergency feature development
- Long-term architecture optimization
- Services from other teams

### 6.2 Contact information

| Role | Contact | Response Time |
|------|----------|----------|
| On-call Engineer | [contact] | 15 minutes |
| Team Lead | [contact] | 30 minutes |
| [Other Key Roles] | [contact] | [time] |

**Depends on Team**:
| Team | Service | Contact Information |
|------|------|----------|
| [Team name] | [Service name] | [contact] |

### 6.3 Upgrade path

```
Level 1: On-call Engineer
↓ Unresolved for 15 minutes
Level 2: Senior Engineer / Team Lead
↓ Unresolved for 30 minutes or P0 failure
Level 3: Engineering Manager / CTO
```

**Upgrade trigger conditions**:
- Time exceeds SLA
- Expansion of impact of failure
- Requires collaboration from other teams
- Requires architecture-level decisions

### 6.4 Accident records

**Each failure must be recorded**:
- Time: [start] - [end]
- Impact: [users/services affected]
- Root cause: [root cause]
- Solution: [what fixed it]
- Improvement measures: [prevention]

**Record location**: [incident-tracker-url]

### 6.5 Runbook Maintenance

**How ​​to report a runbook issue**:
- [Reporting Channel]
- [Responsible Person]

**Update Process**:
1. Found that the runbook is wrong or out of date
2. Create Issue/Ticket
3. Submit update PR
4. Review + Merge
5. Update version number and date

---

## Appendix

### A. Reference documentation

| Documentation | Path/URL | Description |
|------|----------|------|
| PRD | [path] | Product Requirements |
| HLD | [path] | High Level Design |
| LLD | [path] | low-level design |
| API Contract | [path] | Interface Contract |
| Guardrails | [path] | Engineering Specifications |
| Infrastructure Doc | [path] | Infrastructure |

### B. Change History

| Version | Date | Changes | Author |
|------|------|----------|------|
| 1.0.0 | [date] | Initial version | [author] |

### C. Quick check of commonly used commands

```bash
# Check service status
[command]

# View log
[command]

# Restart the service
[command]

# View monitoring
[command]
```

### D. Fault decision tree

```
Alarm trigger
  ↓
Is it a Critical alarm?
  ↓ Yes
Immediate response (15 minutes)
  ↓
Check symptom matching scenarios
  ↓
Implement corresponding solutions
  ↓
Verify fix
  ↓
record accident
```

---

**End of document**
