# Delivery Summary Template

Upon completion of Phase 3.6, a delivery summary must be output according to this template.

---

## Prototype Delivery Summary

### Basic Information

| Project | Content |
|------|------|
| PRD | [path] |
| User Journey | [path] |
| sandbox directory | [path] |
| Routing prefix | [/prototype/] |
| Startup command | [Specific commands, including package manager and workspace location] |
| Entry route | [/prototype/ or /prototype/index] |

### Coverage Statistics

| Indicators | Values ​​|
|------|-----|
| P0 Journey Coverage | X / Y (Z%) |
| P1 Journey Coverage | X / Y (Z%) (placement pages count) |
| Total number of pages | N |
| State coverage rate | Covered M / Total number of state matrices T (Z%) |

### Page status override verification

| Page | Normal state | Loading state | Empty state | Error state | Boundary state |
|------|-------|-------|------|-------|-------|
| [Page 1] | ✅ | ✅ | ✅ | ✅ | N/A |
| [Page 2] | ✅ | ✅ | N/A | ✅ | ✅ |
| ... | ... | ... | ... | ... | ... |

### Component usage statistics

| Category | Quantity |
|------|------|
| Reuse warehouse components | M |
| Prototype new component [PROTOTYPE] | K pieces |

### Isolated Verification

| Check items | Results |
|--------|------|
| All new files are in the sandbox | ✅/❌ |
| Zero file changes outside the sandbox | ✅/❌ |
| Description of exception changes outside the sandbox | None / Approved: `<file path>`:`<line number>` — [Change content, such as "Add prototype-only routing entry"] |
| Prototype routing under exclusive prefix | ✅/❌ |
| Unmodified package.json | ✅/❌ |
| lint check passed | ✅/❌ |
| Type check passed (if applicable) | ✅/❌ |

### Review Mode Verification

| Check | Result |
|--------|--------|
| Review assets exist only inside the prototype sandbox | ✅/❌ |
| `prototypeId` matches the Manifest | ✅/❌ |
| schema is `gainfactor-pm-prototype-review/v1` | ✅/❌ |
| URL/DOM/runtime exports are consistent | ✅/❌/N/A (note hash-router fallback) |
| Add, delete, refresh, and cross-page restore pass | ✅/❌ |
| Zero external network upload | ✅/❌ |

### Quality check results

Record the self-inspection results and evidence according to the 5 dimensions of `references/quality-checklist.md`.

| Dimensions | Results | Summary of Evidence |
|------|------|---------|
| Accessibility | ✅/⚠️/❌ | [For example: all buttons are native `<button>`; form labels are fully associated; 2 icon buttons have been added with `aria-label`] |
| Mock data quality | ✅/⚠️/❌ | [For example: 3 entities all have normal/empty/boundary data sets; the `createdAt` field is the PRD undefined requirement discovered by the UI and has been marked in the Manifest] |
| Component discipline | ✅/⚠️/❌ | [For example: reuse 6 warehouse components; create a new `[PROTOTYPE]` TaskCard, which has been recorded in the Manifest component gap] |
| UI consistency | ✅/⚠️/N/A | [For example: the list page layout is aligned with the warehouse `/dashboard` page mode (header+filter+table); unified toast is used for feedback] / [Insufficient samples, skip] |
| UX Walkthrough | ✅/⚠️ | [For example: automatic jump after successful creation (no redundant operations); empty state with CTA; details page with return button. Found 1 suggestion see question sheet below] |

> ⚠️ Indicates that the dimension is discovered but does not block delivery. Specific issues are recorded in the "Issues Found and Suggestions" table below.

### Issues found and suggestions

| # | Issues | Discover Sources | Impact | Recommendations for Downstream |
|---|------|---------|------|------------|
| 1 | [Problem Description] | [Source: Journey/Page/Status or QA-Dimension Name] | [Impact on User Experience/Data/Architecture] | [Implications for API Contract/HLD] |
| 2 | ... | ... | ... | ... |

### Input to downstream

**For API Contract**:
- [Data requirements exposed by the prototype - which pages require what data and what structure]
- [Paging/filtering/sorting and other list requirements]
- [Real-time requirements (if WebSocket is required)]

**To HLD**:
- [State management complexity (sharing state across pages?)]
- [Caching requirements (what data needs to be cached?)]
- [Performance sensitive points (large data pages, high-frequency interactions)]

### Recommend next step

1. The team inspects the prototype and collects interactive feedback
2. Iterate the prototype based on feedback (re-execute `/gainfactor-pm:prototype-designer`)
3. After the prototype is confirmed, execute `/gainfactor-pm:api-writer` to define the interface contract
4. Execute `/gainfactor-pm:hld-writer` to start technical design
