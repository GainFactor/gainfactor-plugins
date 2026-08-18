# Checkpoint Gates

本文件定义 `uc-interviewer` 产出的 `USER_JOURNEY` 工件如何判定 `draft / in_review / approved`。

## 状态语义

| 状态 | 含义 | 是否可直接作为 PRD 锁定基线 |
|------|------|------------------------------|
| `draft` | baseline 未确认，或仍存在 blocking issue | 否 |
| `in_review` | blocking issue 已清空，等待 stakeholder / 团队确认 | 有条件，必须先确认是否接受 |
| `approved` | 最新 BRD baseline 已确认，且 Journey checkpoint 已明确通过 | 是 |

## Blocking 条件

出现以下任一情况时，`artifact.status` 不得设为 `approved`：
- 当前 BRD 不是“最新批准基线”，或用户无法确认所用 BRD 是否正确
- BRD in-scope 项未完成 `BRD → Journey` 映射
- 任一 `P0` Journey 未完成确认
- 存在悬挂跳转、未定义入口、或无法解释的跨 Journey 循环
- 存在 `MVP` 级 edge case 仍为 `待定`
- trace-lint 未通过

## 通过条件

满足以下条件时，可将 `artifact.status` 设为 `in_review`：
- 最新 BRD baseline 已确认
- BRD in-scope 项都已映射到至少一个 Journey
- `P0` Journey 全部确认
- 无悬挂跳转
- `MVP` edge case 已写清用户可见结果和恢复方式
- trace-lint 通过

满足 `in_review` 条件，且用户/团队明确说“这版可以作为后续 PRD 基线”时，才可设为 `approved`。
