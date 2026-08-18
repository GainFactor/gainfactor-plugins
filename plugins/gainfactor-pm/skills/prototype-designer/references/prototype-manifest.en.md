# Prototype Manifest template

After Phase 1.6 is completed, `_prototype-manifest.md` must be generated in the sandbox directory according to this template.

---

## Prototype Manifest

### Basic Information

| Project | Content |
|------|------|
| PRD source | [PRD file path] |
| User Journey source | [Journey file path] |
| Front-end warehouse | [Warehouse root path] |
| sandbox directory | [sandbox directory path] |
| Routing prefix | [/prototype/] |
| Creation time | YYYY-MM-DD |

### Prototype Budget

| Item | Quantity |
|------|------|
| P0 Journey |
| P1 Journey | Y (placeholder) |
| Total number of pages | N |
| Prototype budget trigger | [Not triggered / Triggered - user confirms the reduction scope] |

### Page ↔ Journey ↔ PRD Traceability Table

| # | Pages | Routes | Journey | Journey Steps | PRD Requirements | Status Overrides |
|---|------|------|---------|-------------|---------|---------|
| 1 | [Page Name] | /prototype/[Path] | [Journey Name] | [S1/S2/...] | [REQ-*] | Normal/Loading/Empty/Error/Boundary |
| 2 | ... | ... | ... | ... | ... | ... |

### Navigation relationship table

| Source page | Target page | Trigger conditions | Journey jump |
|---------|---------|---------|-------------|
| [Page A] | [Page B] | [User Action] | [Journey X S1→S2] |
| [Page B] | [Page C] | [Conditional judgment] | [Journey X→Y across Journey] |
| ... | ... | ... | ... |

### Component usage list

| Components | Source | Usage Page |
|------|------|---------|
| [Button] | The warehouse already exists (src/components/ui/Button) | Page A, Page B |
| [Form] | The warehouse already exists (src/components/Form) | Page C |
| [PROTOTYPE] AddressPicker | Sandbox New | Page C |
| ... | ... | ... |

### Mock data list

| Data file | Corresponding PRD entity | Usage page | Contains status | PRD undefined fields |
|---------|-------------|---------|---------|----------------|
| mock/products.ts | Products | Product list, product details | Normal (10 items), empty (0 items), border (100 items) | `createdAt` (required for list sorting) |
| mock/order.ts | Order | Settlement page | Normal, error (abnormal amount) | — |
| ... | ... | ... | ... | ... |

> **"PRD undefined fields" column**: records the data fields found to be needed during UI interaction but not clearly defined by PRD. These fields are the prototype's input to the downstream API Contract - helping the API Writer complete the data model. Fill in `—` to indicate no additional fields.

### Review Mode

| Item | Content |
|------|---------|
| Status | [Enabled / Reused equivalent repository capability / Disabled with reason] |
| prototypeId | [Unique value shared by all pages in this prototype] |
| Asset paths | [JS/CSS paths inside the sandbox] |
| schema | `gainfactor-pm-prototype-review/v1` |
| AI-readable exports | URL `#prototype-review-v1=` + DOM `#gainfactor-pm-review-output` + runtime |
| URL policy | [Enabled / Hash-router conflict; DOM/runtime fallback] |
| Persistence boundary | Current browser; no automatic network upload |
