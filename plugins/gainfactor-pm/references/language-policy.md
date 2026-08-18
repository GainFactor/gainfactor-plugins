# gainfactor-pm Language Policy

本文件定义 `gainfactor-pm` 全插件统一适用的语言规则。所有 skills、templates、review reports、subagent prompts 都应遵循这里的约束。

## 核心规则

1. **输出语言默认跟随用户输入语言**
   - 用户主要使用中文提问或提供中文文档上下文时，默认输出中文。
   - 用户主要使用英文提问或明确要求英文时，默认输出英文。

2. **用户显式指定语言时，以用户指定为准**
   - 例如用户说“用英文输出”“英文版 PRD”，则后续所有主输出都必须跟随该语言。
   - 同一轮里如果用户同时要求“正文英文、保留中文术语表”，以用户的显式局部要求为准。

3. **不要因为 `SKILL.md` 是中文就强制输出中文**
   - `SKILL.md` 的编写语言不等于最终交付物的输出语言。
   - 模板、报告、证书、交付摘要、Mermaid 标题、表头、说明文字都应服从当前 `output_language`。

4. **`TRACEABILITY-METADATA` 始终保持英文契约**
   - 字段名、枚举值、ID、comment markers、schema/profile 名称必须保持英文。
   - 例如：`artifact.type`、`status`、`REQ-*`、`DEC-*`、`FLOW-*`、`<!-- TRACEABILITY-METADATA:BEGIN -->` 不得本地化。

## 模板与文件命名

- 中文模板保留原文件名：`foo.md`
- 英文模板使用对应文件名：`foo.en.md`
- 若未来支持其他语言，优先复用 `foo.en.md` 作为骨架，再由 skill 按用户语言生成正文

## Prompt / Subagent 传递规则

- 凡是会派发 writer / reviewer / orchestrator 子任务的 skill，都必须显式传递 `output_language`
- 上游已判定语言后，下游 prompt 不得自行回退为中文
- 若子任务产生审查报告、准出证书或交付摘要，标题、表头、说明文必须跟随 `output_language`

建议使用如下说明传递语言约束：

```text
Output language: [zh-CN / en]
Follow the user's requested output language for all human-readable content.
Keep TRACEABILITY-METADATA keys, enum values, IDs, and comment markers in English.
```

## 冲突与回退

- 当用户输入语言不明确，但上下文文档以英文为主时，优先英文
- 当用户输入语言不明确，且上下文文档以中文为主时，优先中文
- 当用户要求双语时，可输出双语摘要，但 metadata 与稳定标识仍保持英文

## 本轮范围说明

本轮只统一语言规则、补高优先级英文模板、抽 reviewer 输出模板。
交互提问模板、全量双语 `SKILL.md`、所有命令文档的国际化不在本轮范围内。
