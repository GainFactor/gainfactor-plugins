# User Persona Skill

`user-persona` 面向产品负责人和产品经理，从具体人物的现实背景、使用行为、反馈、顾虑与决策中形成用户画像，并进一步给出 `用户 × 功能优先级路线图`。

## 核心原则

- 先理解没有产品时用户如何行动，再测试产品能否改变选择。
- 虚拟 Agent 必须先通过真实性门禁；MBTI 只能辅助人物行为一致性，不能直接推导需求。
- 每个行为 Step 按情境适用地记录目标、工具或现实方法、使用方式、对象、反馈、判断、顾虑、决定和下一步。
- 工具、品牌、搜索词、地点和具体对象来自本次真实情境，不作为其他项目的标准案例。
- 每个用户画像完成、检查并写入后再处理下一个；所有画像完成后才综合需求和功能优先级。
- 直接编写最终门户 MDX，`document-publisher` 只提供表达能力、校验和发布，不二次理解普通 Markdown。

## 报告结构

正式报告只包含三个模块：

1. 产品定义与目标用户；
2. 用户画像；
3. 用户 × 功能优先级路线图。

每个用户画像包含：人物背景、典型情境、核心目标（JTBD）、关键行为与核心痛点、决策与信任关键、期望产品功能。研究过程与完整反馈保存在内部 research sidecar，不占用主报告阅读路径。

报告直接使用门户已注册的通用能力：`Profile` 组织照片、资料和人物背景，`InfoGrid` 展示紧凑字段，`StructuredSteps` 还原行为路径，`ContentPanel` 说明功能机会，`GroupedBoard` 汇总共性与特殊问题并表达用户价值优先级。组件只负责呈现，业务含义和推导规则仍由本 Skill 定义。

## 增量工作流

```text
产品上下文 → 人物设定 → 无产品盲测 → 产品命题测试
→ 目标用户选择 → 逐个用户画像 → 需求综合 → 功能优先级
→ 整体优化 → 门户发布
```

每阶段执行“完成—门禁—写入—下一阶段”。详细阶段产物和失败处理见 `references/incremental-workflow-and-gates.md`。

## 文件职责

| 文件 | 职责 |
|-|-|
| `SKILL.md` | 适用边界、主流程、门禁纪律和默认交付 |
| `references/intake-and-modes.md` | 产品上下文、研究路径和领域信息选择 |
| `references/incremental-workflow-and-gates.md` | 阶段产物、research sidecar、即时写入和阶段门禁 |
| `references/simulation-and-synthesis.md` | Agent 真实性、行为 Step、命题测试和优先级推导 |
| `references/persona-schema.md` | 单个用户画像结构和门禁 |
| `references/persona-image-generation.md` | 图片生成时机、视觉要求和项目引用 |
| `references/report-structure-and-quality.md` | 三模块报告、专业语言和文档能力选择 |
| `references/portal-presentation.md` | 模块一的首屏视图和发布校验 |

## 验证

```bash
python3 /Users/dylan/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  plugins/gainfactor-pm/skills/user-persona
```
