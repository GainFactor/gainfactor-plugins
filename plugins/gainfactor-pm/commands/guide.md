---
description: Guide, workflow guide, 流程导航。扫描项目文档与准出状态，判断当前所处阶段并推荐下一步 skill；当 Test Spec 已具备下游 handoff 时，也可推荐进入 gainfactor-pm-bot 自动化分支
argument-hint: "[项目/目录路径] [可选：补充上下文]"
---

# Guide

启动 `gainfactor-pm` 流程导航。扫描当前项目已有文档、审查结果和准出状态，回答：

- 现在主流程走到哪一步
- 哪些关键基线已经具备
- 下一步最适合运行哪个 skill / downstream workflow

## 使用方式

提供项目路径，或直接在当前仓库运行：

$ARGUMENTS

## Guide 的职责边界

- **会做**：扫描文档、识别状态、输出 Mermaid DAG、推荐下一步
- **不会做**：替你撰写文档、替你做正式评审

## Guide 覆盖的流程

### 主流程

```text
BRD -> User Journey -> PRD -> API Contract -> HLD -> Test Strategy -> LLD -> Test Spec -> Test Review -> Runbook
```

### 可选 downstream 分支

- GainFactor-PM Automation Landing：`/case-writing -> /case -> /pipeline -> /trigger -> /execution`

### 可选分支

- Prototype：仅在前端仓库或明确需要先验证交互时提示

### 横切分支

- Guardrails：仅在命中项目级触发条件时建议，不是每个 feature 的固定步骤

## 输出内容

- 项目状态摘要
- 相关流程图
- 1 到 3 个下一步建议
- 关键待确认项（如有）

如果你不确定从哪个命令开始，或者接手了一个已有部分文档的项目，请直接运行 Guide。
