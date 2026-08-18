---
description: Review Guardrails, 评审项目级工程规范基线
argument-hint: <Guardrails 路径>
---

# Guardrails Reviewer

启动 Guardrails 准出审查流程。除了审规则本身，还会检查这次变更的触发判定、生成模式、事实标准、下游工作流钩子与重审建议是否成立。

## 使用方式

提供 Guardrails 路径：

$ARGUMENTS

## 审查重点

- 这次是否真的该改 Guardrails（create / update / restructure / no_change）
- 规则是否有充分证据，尤其是 repository_scan_first 的事实标准
- 下游工作流钩子与阻塞建议是否完整
- 规则是否可验证、可执行、与现有规范一致

## 准出门槛

- **P0 = 0**
- **P1 = 0**
- **P2 ≤ 2**

请提供 Guardrails 文档路径开始评审。
