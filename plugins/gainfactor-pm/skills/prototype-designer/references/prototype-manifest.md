# Prototype Manifest 模板

Phase 1.6 完成后，必须按此模板在沙箱目录内生成 `_prototype-manifest.md`。

---

## Prototype Manifest

### 基本信息

| 项目 | 内容 |
|------|------|
| PRD 来源 | [PRD 文件路径] |
| User Journey 来源 | [Journey 文件路径] |
| 前端仓库 | [仓库根路径] |
| 沙箱目录 | [沙箱目录路径] |
| 路由前缀 | [/prototype/] |
| 创建时间 | YYYY-MM-DD |

### 原型预算

| 项目 | 数量 |
|------|------|
| P0 Journey | X 个 |
| P1 Journey | Y 个（占位） |
| 页面总数 | N 个 |
| 原型预算触发 | [未触发 / 已触发——用户确认缩减范围] |

### 页面 ↔ Journey ↔ PRD 追溯表

| # | 页面 | 路由 | Journey | Journey 步骤 | PRD 需求 | 状态覆盖 |
|---|------|------|---------|-------------|---------|---------|
| 1 | [页面名] | /prototype/[路径] | [Journey 名] | [S1/S2/...] | [REQ-*] | 正常/加载/空/错误/边界 |
| 2 | ... | ... | ... | ... | ... | ... |

### 导航关系表

| 来源页面 | 目标页面 | 触发条件 | Journey 跳转 |
|---------|---------|---------|-------------|
| [页面A] | [页面B] | [用户操作] | [Journey X S1→S2] |
| [页面B] | [页面C] | [条件判断] | [Journey X→Y 跨 Journey] |
| ... | ... | ... | ... |

### 组件使用清单

| 组件 | 来源 | 使用页面 |
|------|------|---------|
| [Button] | 仓库已有 (src/components/ui/Button) | 页面A, 页面B |
| [Form] | 仓库已有 (src/components/Form) | 页面C |
| [PROTOTYPE] AddressPicker | 沙箱新建 | 页面C |
| ... | ... | ... |

### Mock 数据清单

| 数据文件 | 对应 PRD 实体 | 使用页面 | 包含状态 | PRD 未定义的字段 |
|---------|-------------|---------|---------|----------------|
| mock/products.ts | 商品 | 商品列表, 商品详情 | 正常(10条), 空(0条), 边界(100条) | `createdAt`（列表排序需要） |
| mock/order.ts | 订单 | 结算页 | 正常, 错误(金额异常) | — |
| ... | ... | ... | ... | ... |

> **「PRD 未定义的字段」列**：记录 UI 交互过程中发现需要但 PRD 未明确定义的数据字段。这些字段是原型对下游 API Contract 的输入——帮助 API Writer 补全数据模型。填 `—` 表示无额外字段。

### 评审模式

| 项目 | 内容 |
|------|------|
| 启用状态 | [已启用 / 复用仓库等价能力 / 未启用及原因] |
| prototypeId | [同一原型跨页面保持一致的唯一值] |
| 资产路径 | [沙箱内 JS/CSS 路径] |
| schema | `gainfactor-pm-prototype-review/v1` |
| AI 读取出口 | URL `#prototype-review-v1=` + DOM `#gainfactor-pm-review-output` + runtime |
| URL 策略 | [启用 / hash router 冲突，降级为 DOM/runtime] |
| 持久化边界 | 当前浏览器；不主动上传网络 |
